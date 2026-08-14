"""Orchestrator: runs all passes sequentially."""

from __future__ import annotations

import hashlib
import json
import os
import time
from contextlib import nullcontext
from typing import Callable, ContextManager
from uuid import uuid4

from pt.apply_refinement import apply_refinement
from pt.bayesian import run_bayesian_policy_analysis
from pt.llm import DEFAULT_MODEL, with_llm_run_config
from pt.pass_absence import run_absence
from pt.pass_absence_audit import (
    apply_accepted_source_silence,
    run_source_silence_audit,
)
from pt.pass_critic import run_critic
from pt.pass_central_claim_review import run_central_claim_review
from pt.pass_discriminator_audit import (
    build_effective_testing,
    DiscriminatorAuditBlockedError,
    discriminator_repair_context,
    require_discriminator_audit_integrity,
    run_discriminator_audit,
    testing_sha256,
)
from pt.pass_extract import run_extract
from pt.pass_hypothesize import (
    build_hypothesis_generation_view,
    refinement_evidence_delta,
    require_generation_view_integrity,
    require_hypothesis_exposure_integrity,
    run_hypothesize,
    validate_hypothesis_provenance,
)
from pt.pass_mechanism import require_mechanism_trace_integrity, run_mechanism_trace
from pt.pass_mechanism_audit import (
    MechanismAuditBlockedError,
    apply_mechanism_critique,
    build_mechanism_repair_context,
    material_mechanism_findings,
    merge_mechanism_repair_contexts,
    mechanism_trace_sha256,
    require_mechanism_audit_integrity,
    require_mechanism_critique_integrity,
    run_mechanism_critic,
)
from pt.pass_mechanism_patch import (
    apply_mechanism_stage_description_patch,
    run_mechanism_stage_description_patch,
    run_mechanism_stage_description_patch_critic,
    stage_description_patch_target_ids,
)
from pt.pass_mechanism_graph_patch import (
    apply_mechanism_graph_patch,
    graph_patch_targets,
    run_mechanism_graph_patch,
    run_mechanism_graph_patch_critic,
)
from pt.pass_diagnostic import compute_diagnostic_matrix
from pt.pass_partition import PartitionBlockedError, require_adequate_partition, run_partition
from pt.pass_partition_repair import run_partition_repair
from pt.pass_refine import run_refine
from pt.pass_synthesize import run_synthesize
from pt.pass_test import (
    require_evidence_exclusion_integrity,
    require_prediction_lineage_integrity,
    run_test,
)
from pt.schemas import (
    AbsenceResult,
    BayesianResult,
    CentralClaimEntailmentReview,
    CriticDelta,
    CriticResult,
    DiscriminatorAuditAttempt,
    DiscriminatorAuditResolution,
    DiagnosticMatrix,
    EvidenceExclusionReason,
    ExtractionResult,
    HypothesisSpace,
    HypothesisGenerationView,
    InferenceDesign,
    InferenceStatus,
    LLMClientRuntimeBinding,
    MechanismTraceResult,
    MechanismAuditAttempt,
    MechanismGraphPatch,
    MechanismStageDescriptionPatch,
    MechanismAuditResolution,
    MechanismRepairContext,
    PartitionAudit,
    PartitionAttempt,
    PartitionResolution,
    PriorSpecification,
    ProcessTracingResult,
    RefinementStatus,
    RefinementResult,
    SegmentedSourceSummary,
    TestingResult,
    InferenceMode,
)
from pt.source_coverage import build_source_coverage
from pt.source_packet import SourcePacket, require_stable_source_ids
from pt.segmented_source import SegmentedSourceBundleV1


def _source_text_sha256(text: str) -> str:
    """Hash the exact source text used for the analysis."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_from_result_source(text: str, from_result: ProcessTracingResult) -> str:
    """Return current source hash or raise when cached analysis provenance differs."""
    current_hash = _source_text_sha256(text)
    cached_hash = from_result.source_text_sha256
    if cached_hash is None:
        raise ValueError(
            "--from-result file has no source_text_sha256 provenance; regenerate "
            "the result with the current code before refining from it"
        )
    if cached_hash != current_hash:
        raise ValueError(
            "--from-result source_text_sha256 does not match the input text "
            f"(result={cached_hash}, input={current_hash})"
        )
    return current_hash


def _default_review(hypothesis_space: HypothesisSpace, output_dir: str | None) -> HypothesisSpace:
    """Interactive hypothesis review: display hypotheses, let user edit JSON."""
    print("\n" + "=" * 60)
    print("HYPOTHESIS REVIEW CHECKPOINT")
    print("=" * 60)
    print(f"\nResearch question: {hypothesis_space.research_question}\n")

    for h in hypothesis_space.hypotheses:
        print(f"  {h.id}: [{h.source}] {h.description}")
        print(f"       Mechanism: {h.causal_mechanism}")
        print(f"       Predictions: {len(h.observable_predictions)}")
        print()

    # Write hypotheses JSON for editing
    hyp_path = os.path.join(output_dir, "hypotheses.json") if output_dir else "hypotheses.json"
    with open(hyp_path, "w", encoding="utf-8") as f:
        json.dump(hypothesis_space.model_dump(), f, indent=2)
    print(f"Hypotheses written to: {hyp_path}")
    print("Edit the file to merge/split/modify hypotheses, then press Enter.")
    print("Or press Enter without editing to continue as-is.")
    print("=" * 60)

    input("\nPress Enter to continue...")

    # Reload (user may have edited)
    with open(hyp_path, "r", encoding="utf-8") as f:
        edited = json.load(f)
    edited_space = HypothesisSpace.model_validate(edited)

    if len(edited_space.hypotheses) != len(hypothesis_space.hypotheses):
        print(f"  Hypotheses changed: {len(hypothesis_space.hypotheses)} → {len(edited_space.hypotheses)}")
    else:
        print("  Hypotheses unchanged.")

    return edited_space


def _default_partition_review(
    hypothesis_space: HypothesisSpace,
    partition_audit: PartitionAudit,
    output_dir: str | None,
) -> HypothesisSpace:
    """Interactive partition review: display partition concerns, let user edit hypotheses."""
    print("\n" + "=" * 60)
    print("PARTITION AUDIT REVIEW CHECKPOINT")
    print("=" * 60)
    print(f"\nPartition quality: {partition_audit.overall_quality.upper()}")
    print(f"Summary: {partition_audit.summary}")

    if partition_audit.hypotheses_flagged:
        print(f"\nFlagged hypotheses: {', '.join(partition_audit.hypotheses_flagged)}")

    print("\nProblem pairs:")
    any_flagged = False
    for pair in partition_audit.rival_pairs:
        concerns = []
        if pair.overlap_concern:
            concerns.append("OVERLAP")
        if pair.complementary_concern:
            concerns.append("COMPLEMENTARY")
        if pair.absorptive_concern:
            concerns.append("ABSORPTIVE")
        if pair.discriminator_count < 1:
            concerns.append("NO-DISCRIMINATORS")
        if not concerns:
            continue
        any_flagged = True
        print(f"  {pair.h1_id} <-> {pair.h2_id}: [{', '.join(concerns)}] (discriminators: {pair.discriminator_count})")
        if pair.concern_detail:
            print(f"    {pair.concern_detail}")
    if not any_flagged:
        print("  (no individual pair problems — overall quality set by LLM judgment)")

    print("\nRemediation:")
    print("  OVERLAP: add NOT-X predictions to discriminate or merge")
    print("  COMPLEMENTARY: merge into one hypothesis with both mechanisms")
    print("  ABSORPTIVE: split the broad hypothesis or add exclusive predictions")
    print("  NO-DISCRIMINATORS: add predictions where H1 expects X but H2 expects NOT-X")

    hyp_path = os.path.join(output_dir, "hypotheses.json") if output_dir else "hypotheses.json"
    with open(hyp_path, "w", encoding="utf-8") as f:
        json.dump(hypothesis_space.model_dump(), f, indent=2)
    print(f"\nHypotheses written to: {hyp_path}")
    print("Edit the file to fix partition concerns, then press Enter.")
    print("Or press Enter without editing to continue as-is.")
    print("=" * 60)

    input("\nPress Enter to continue...")

    with open(hyp_path, "r", encoding="utf-8") as f:
        edited = json.load(f)
    edited_space = HypothesisSpace.model_validate(edited)

    if len(edited_space.hypotheses) != len(hypothesis_space.hypotheses):
        print(f"  Hypotheses changed: {len(hypothesis_space.hypotheses)} -> {len(edited_space.hypotheses)}")
    else:
        print("  Hypotheses unchanged.")

    return edited_space


def _default_refine_review(refinement: RefinementResult, output_dir: str | None) -> RefinementResult:
    """Interactive refinement review: display delta summary, let user edit JSON."""
    print("\n" + "=" * 60)
    print("REFINEMENT REVIEW CHECKPOINT")
    print("=" * 60)

    print(f"\n  New evidence:       {len(refinement.new_evidence)}")
    print(f"  Reinterpretations:  {len(refinement.reinterpreted_evidence)}")
    print(f"  New causal edges:   {len(refinement.new_causal_edges)}")
    print(f"  Spurious removals:  {len(refinement.spurious_extractions)}")
    print(f"  Hypothesis refine:  {len(refinement.hypothesis_refinements)}")
    print(f"  Missing mechanisms: {len(refinement.missing_mechanisms)}")

    for ne in refinement.new_evidence:
        print(f"    + {ne.id}: {ne.description[:60]}")
    for se in refinement.spurious_extractions:
        print(f"    - {se.item_id} ({se.item_type}): {se.reason[:60]}")
    for hr in refinement.hypothesis_refinements:
        print(f"    ~ {hr.hypothesis_id} [{hr.refinement_type}]: {hr.description[:60]}")

    ref_path = os.path.join(output_dir, "refinement.json") if output_dir else "refinement.json"
    with open(ref_path, "w", encoding="utf-8") as f:
        json.dump(refinement.model_dump(), f, indent=2)
    print(f"\nRefinement written to: {ref_path}")
    print("Edit the file to modify the refinement delta, then press Enter.")
    print("Or press Enter without editing to continue as-is.")
    print("=" * 60)

    input("\nPress Enter to continue...")

    with open(ref_path, "r", encoding="utf-8") as f:
        edited = json.load(f)
    return RefinementResult.model_validate(edited)


def _write_partition_artifacts(
    output_dir: str | None,
    resolution: PartitionResolution,
) -> None:
    """Persist the latest audit and full repair history when an output dir exists."""
    if output_dir is None:
        return
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "partition.json"), "w", encoding="utf-8") as f:
        json.dump(resolution.final_audit.model_dump(), f, indent=2)
    with open(
        os.path.join(output_dir, "partition_resolution.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(resolution.model_dump(), f, indent=2)


def _resolve_partition(
    extraction: ExtractionResult,
    hypothesis_space: HypothesisSpace,
    *,
    generation_view: HypothesisGenerationView | None = None,
    model: str | None = None,
    repair_model: str | None = None,
    trace_id: str,
    output_dir: str | None = None,
    verbose: bool = True,
    partition_review: bool = False,
    partition_review_fn: Callable[
        [HypothesisSpace, PartitionAudit, str | None], HypothesisSpace
    ] | None = None,
    repair_attempts: int = 2,
    initial_action: str = "initial_audit",
) -> tuple[HypothesisSpace, PartitionAudit, PartitionResolution]:
    """Audit, repair, and re-audit a hypothesis partition before Pass 3."""
    if repair_attempts < 0:
        raise ValueError("partition repair attempts must be >= 0")
    if generation_view is None:
        generation_view = build_hypothesis_generation_view(
            extraction,
            InferenceDesign(mode="exploratory_full_corpus"),
        )

    attempts: list[PartitionAttempt] = []
    action = initial_action
    automated_repairs = 0
    manual_review_used = False

    while True:
        validate_hypothesis_provenance(
            extraction,
            hypothesis_space,
            generation_view,
        )
        require_hypothesis_exposure_integrity(
            extraction,
            hypothesis_space,
            generation_view,
        )
        audit_trace_id = f"{trace_id}-partition-audit-{len(attempts) + 1}"
        audit = run_partition(hypothesis_space, model=model, trace_id=audit_trace_id)
        attempt = PartitionAttempt(
            attempt=len(attempts) + 1,
            action=action,
            hypothesis_space=hypothesis_space.model_copy(deep=True),
            audit=audit,
        )
        attempts.append(attempt)

        try:
            require_adequate_partition(hypothesis_space, audit)
        except PartitionBlockedError:
            resolution = PartitionResolution(
                status="repairing",
                attempts=attempts,
                final_audit=audit,
            )
            _write_partition_artifacts(output_dir, resolution)

            if partition_review and not manual_review_used:
                review_fn = partition_review_fn or _default_partition_review
                hypothesis_space = review_fn(hypothesis_space, audit, output_dir)
                manual_review_used = True
                action = "manual_review"
                continue

            if automated_repairs < repair_attempts:
                automated_repairs += 1
                if verbose:
                    print(
                        "  Partition blocked; running automated repair "
                        f"{automated_repairs}/{repair_attempts}..."
                    )
                hypothesis_space = run_partition_repair(
                    extraction,
                    hypothesis_space,
                    audit,
                    generation_view=generation_view,
                    model=repair_model or model,
                    trace_id=f"{trace_id}-partition-repair-{automated_repairs}",
                )
                action = f"automated_repair_{automated_repairs}"
                continue

            resolution.status = "blocked"
            _write_partition_artifacts(output_dir, resolution)
            raise PartitionBlockedError(audit)

        resolution = PartitionResolution(
            status="accepted",
            attempts=attempts,
            final_audit=audit,
        )
        _write_partition_artifacts(output_dir, resolution)
        return hypothesis_space, audit, resolution


def _combine_partition_resolutions(
    earlier: PartitionResolution | None,
    later: PartitionResolution,
) -> PartitionResolution:
    """Append a re-audit history while keeping attempt numbers monotonic."""
    all_attempts = [] if earlier is None else list(earlier.attempts)
    all_attempts.extend(later.attempts)
    renumbered = [
        attempt.model_copy(update={"attempt": index})
        for index, attempt in enumerate(all_attempts, start=1)
    ]
    return PartitionResolution(
        status=later.status,
        attempts=renumbered,
        final_audit=later.final_audit,
    )


def _write_discriminator_audit_artifacts(
    output_dir: str | None,
    resolution: DiscriminatorAuditResolution,
) -> None:
    """Persist the latest semantic audit and its complete repair history."""

    if output_dir is None:
        return
    os.makedirs(output_dir, exist_ok=True)
    with open(
        os.path.join(output_dir, "discriminator_audit.json"),
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(resolution.final_audit.model_dump(mode="json"), handle, indent=2)
    with open(
        os.path.join(output_dir, "discriminator_audit_resolution.json"),
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(resolution.model_dump(mode="json"), handle, indent=2)


def _combine_discriminator_audit_resolutions(
    earlier: DiscriminatorAuditResolution | None,
    later: DiscriminatorAuditResolution,
) -> DiscriminatorAuditResolution:
    """Append semantic-audit history while keeping attempt numbers monotonic."""

    all_attempts = [] if earlier is None else list(earlier.attempts)
    all_attempts.extend(later.attempts)
    renumbered = [
        attempt.model_copy(update={"attempt": index})
        for index, attempt in enumerate(all_attempts, start=1)
    ]
    return DiscriminatorAuditResolution(
        status=later.status,
        attempts=renumbered,
        final_audit=later.final_audit,
        effective_testing=later.effective_testing,
    )


def _resolve_discriminator_audit(
    extraction: ExtractionResult,
    hypothesis_space: HypothesisSpace,
    partition_audit: PartitionAudit,
    initial_testing: TestingResult,
    *,
    inference_mode: InferenceMode = "theory_first",
    analyst_model: str | None,
    audit_model: str | None,
    trace_id: str,
    prior_evidence_ids: list[str],
    post_selection_evidence_ids: list[str] | None = None,
    post_selection_reason: EvidenceExclusionReason = "post_selection_refinement",
    critic_context: str | None = None,
    source_scope_context: str | None = None,
    repair_attempts: int = 0,
    terminal_enforcement_attempts: int = 1,
    output_dir: str | None = None,
    verbose: bool = True,
    pass_label: str = "",
) -> tuple[TestingResult, DiscriminatorAuditResolution]:
    """Audit, re-elicit, and re-audit all semantic discriminator claims."""

    if repair_attempts < 0:
        raise ValueError("discriminator audit repair attempts must be >= 0")
    if terminal_enforcement_attempts < 0:
        raise ValueError("terminal discriminator enforcement attempts must be >= 0")
    testing = initial_testing
    attempts: list[DiscriminatorAuditAttempt] = []
    re_elicitations = 0
    action = "initial_semantic_audit"
    prefix = f"{pass_label} " if pass_label else ""

    while True:
        if verbose:
            print(
                f"{prefix}Pass 3a: Independent exact-quote discriminator audit..."
            )
        audit = run_discriminator_audit(
            extraction,
            hypothesis_space,
            partition_audit,
            testing,
            inference_mode=inference_mode,
            model=audit_model,
            trace_id=f"{trace_id}-discriminator-audit-{len(attempts) + 1}",
            source_scope_context=source_scope_context,
        )
        attempt = DiscriminatorAuditAttempt(
            attempt=len(attempts) + 1,
            action=action,
            testing_sha256=testing_sha256(testing),
            audit=audit,
        )
        attempts.append(attempt)
        resolution = DiscriminatorAuditResolution(
            status="repairing" if audit.decision_blockers else "accepted",
            attempts=attempts,
            final_audit=audit,
        )
        _write_discriminator_audit_artifacts(output_dir, resolution)
        if not audit.decision_blockers:
            effective_testing, _ = build_effective_testing(testing, audit)
            resolution = resolution.model_copy(
                update={"effective_testing": effective_testing}
            )
            _write_discriminator_audit_artifacts(output_dir, resolution)
            require_discriminator_audit_integrity(
                resolution,
                extraction,
                hypothesis_space,
                partition_audit,
                testing,
                inference_mode=inference_mode,
            )
            if verbose:
                print(
                    f"  Accepted {audit.accepted_count}/{len(audit.candidates)} "
                    "proposed discriminators"
                )
            return effective_testing, resolution

        if re_elicitations >= repair_attempts:
            if terminal_enforcement_attempts > 0:
                effective_testing, enforced_evidence_ids = build_effective_testing(
                    testing,
                    audit,
                )
                accepted_resolution = DiscriminatorAuditResolution(
                    status="accepted",
                    attempts=attempts,
                    final_audit=audit,
                    effective_testing=effective_testing,
                )
                _write_discriminator_audit_artifacts(
                    output_dir,
                    accepted_resolution,
                )
                require_discriminator_audit_integrity(
                    accepted_resolution,
                    extraction,
                    hypothesis_space,
                    partition_audit,
                    testing,
                    inference_mode=inference_mode,
                )
                if verbose:
                    print(
                        "  Generative re-elicitation disabled or exhausted; semantic "
                        f"projection neutralized rejected comparisons in "
                        f"{len(enforced_evidence_ids)} effective row(s); raw vectors retained"
                    )
                return effective_testing, accepted_resolution
            blocked = resolution.model_copy(update={"status": "blocked"})
            _write_discriminator_audit_artifacts(output_dir, blocked)
            raise DiscriminatorAuditBlockedError(blocked)

        re_elicitations += 1
        if verbose:
            print(
                f"  Rejected {audit.rejected_count}/{len(audit.candidates)}; "
                f"re-eliciting Pass 3 ({re_elicitations}/{repair_attempts})..."
            )
        testing = run_test(
            extraction,
            hypothesis_space,
            partition_audit,
            model=analyst_model,
            trace_id=f"{trace_id}-discriminator-reelicit-{re_elicitations}",
            critic_context=critic_context,
            discriminator_audit_context=discriminator_repair_context(audit),
            prior_evidence_ids=prior_evidence_ids,
            post_selection_evidence_ids=post_selection_evidence_ids,
            post_selection_reason=post_selection_reason,
            source_scope_context=source_scope_context,
        )
        action = f"pass3_reelicitation_{re_elicitations}"


def _resolve_prior_specification(
    extraction: ExtractionResult,
    hypothesis_space: HypothesisSpace,
    specification: PriorSpecification | None,
) -> PriorSpecification:
    """Bind an explicit prior to the accepted hypothesis and evidence contracts."""
    hypothesis_ids = [hypothesis.id for hypothesis in hypothesis_space.hypotheses]
    evidence_ids = [evidence.id for evidence in extraction.evidence]
    if specification is not None and not isinstance(specification, PriorSpecification):
        raise TypeError(
            "prior_specification must be a PriorSpecification; bare hypothesis-weight "
            "mappings do not declare method or evidence provenance"
        )
    if specification is None or specification.method == "uniform":
        return PriorSpecification.uniform(hypothesis_ids).validate_for(
            hypothesis_ids,
            evidence_ids,
        )
    return specification.validate_for(hypothesis_ids, evidence_ids)


def _validate_inference_design(
    design: InferenceDesign,
    extraction: ExtractionResult,
    source_packet: SourcePacket | None,
    theories: str | None,
) -> HypothesisGenerationView:
    """Bind the declared exposure design to actual source and evidence lineage."""

    if design.mode == "theory_first" and not (theories and theories.strip()):
        raise ValueError("theory_first inference requires non-empty theories material")
    if design.mode == "theory_first":
        assert theories is not None
        expected_theory_hash = hashlib.sha256(theories.encode("utf-8")).hexdigest()
        if design.theory_material_sha256 != expected_theory_hash:
            raise ValueError(
                "theory_first inference design is not bound to the exact supplied "
                "theory material"
            )
    if design.mode == "discovery_evaluation_split":
        if source_packet is None:
            raise ValueError(
                "discovery_evaluation_split requires a source packet with stable source ids"
            )
        packet_ids = {
            source.source_id.strip()
            for source in source_packet.source_candidates
            if source.source_id and source.source_id.strip()
        }
        declared_ids = set(design.discovery_source_ids) | set(
            design.evaluation_source_ids
        )
        if declared_ids != packet_ids:
            raise ValueError(
                "split inference roles must cover every packet source exactly: "
                f"missing={sorted(packet_ids - declared_ids)}, "
                f"unknown={sorted(declared_ids - packet_ids)}"
            )
        unassigned = [item.id for item in extraction.evidence if not item.source_id]
        unknown = {
            item.id: item.source_id
            for item in extraction.evidence
            if item.source_id and item.source_id not in packet_ids
        }
        if unassigned or unknown:
            raise ValueError(
                "split inference requires complete evidence-to-source lineage: "
                f"unassigned={sorted(unassigned)}, unknown={unknown}"
            )
        represented_ids = {item.source_id for item in extraction.evidence}
        missing_discovery = set(design.discovery_source_ids) - represented_ids
        missing_evaluation = set(design.evaluation_source_ids) - represented_ids
        if missing_discovery or missing_evaluation:
            raise ValueError(
                "split inference requires extracted evidence in both source roles: "
                f"discovery_without_evidence={sorted(missing_discovery)}, "
                f"evaluation_without_evidence={sorted(missing_evaluation)}"
            )
    return build_hypothesis_generation_view(extraction, design)


def _initial_inference_status(design: InferenceDesign) -> InferenceStatus:
    if design.mode == "theory_first":
        if design.theory_evidence_relationship != "independent":
            return "exploratory_post_selection"
        return "confirmatory_eligible_theory_first"
    if design.mode == "discovery_evaluation_split":
        return "confirmatory_eligible_discovery_evaluation_split"
    return "exploratory_post_selection"


def _theory_reuse_evidence_ids(
    design: InferenceDesign,
    extraction: ExtractionResult,
) -> list[str]:
    """Return evidence that cannot independently update a reused case theory."""

    if (
        design.mode == "theory_first"
        and design.theory_evidence_relationship != "independent"
    ):
        return [item.id for item in extraction.evidence]
    return []


def _theory_first_extraction_focus(
    hypothesis_space: HypothesisSpace,
) -> str:
    """Project frozen pre-corpus rivals into a bounded extraction specification."""

    return json.dumps(
        {
            "research_question": hypothesis_space.research_question,
            "rivals": [
                {
                    "hypothesis_id": hypothesis.id,
                    "description": hypothesis.description,
                    "causal_mechanism": hypothesis.causal_mechanism,
                    "observable_predictions": [
                        {
                            "prediction_id": prediction.id,
                            "description": prediction.description,
                        }
                        for prediction in hypothesis.observable_predictions
                    ],
                }
                for hypothesis in hypothesis_space.hypotheses
            ],
            "extraction_rule": (
                "Extract every distinct source-grounded observation needed to test "
                "these frozen predictions, connect their temporal or causal stages, "
                "represent a concrete rival alternative, or interpret trace production. "
                "Do not inventory unrelated routine proceedings or repeated rhetoric."
            ),
        },
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    )


def _bind_inference_design(
    design: InferenceDesign,
    theories: str | None,
) -> InferenceDesign:
    """Bind an input design to the exact theory material supplied for this run."""

    theory_material_sha256 = (
        hashlib.sha256(theories.encode("utf-8")).hexdigest()
        if theories and theories.strip()
        else None
    )
    return design.model_copy(
        update={"theory_material_sha256": theory_material_sha256}
    )


def _write_mechanism_audit_artifacts(
    output_dir: str | None,
    trace: MechanismTraceResult,
    resolution: MechanismAuditResolution,
) -> None:
    """Persist the final mechanism and complete independent-audit lineage."""

    if output_dir is None:
        return
    os.makedirs(output_dir, exist_ok=True)
    with open(
        os.path.join(output_dir, "mechanism_trace.json"),
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(trace.model_dump(mode="json"), handle, indent=2)
    with open(
        os.path.join(output_dir, "mechanism_audit_resolution.json"),
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(resolution.model_dump(mode="json"), handle, indent=2)


def _write_mechanism_attempt_artifact(
    output_dir: str | None,
    *,
    attempt_number: int,
    candidate: MechanismTraceResult,
    audit_attempt: MechanismAuditAttempt | None = None,
) -> None:
    """Checkpoint each successful stage before a later LLM boundary can fail."""

    if output_dir is None:
        return
    os.makedirs(output_dir, exist_ok=True)
    candidate_path = os.path.join(
        output_dir,
        f"mechanism_candidate_attempt_{attempt_number}.json",
    )
    with open(candidate_path, "w", encoding="utf-8") as handle:
        json.dump(candidate.model_dump(mode="json"), handle, indent=2)
    if audit_attempt is None:
        return
    audit_path = os.path.join(
        output_dir,
        f"mechanism_audit_attempt_{attempt_number}.json",
    )
    with open(audit_path, "w", encoding="utf-8") as handle:
        json.dump(audit_attempt.model_dump(mode="json"), handle, indent=2)


def _write_mechanism_stage_patch_artifact(
    output_dir: str | None,
    patch: MechanismStageDescriptionPatch,
) -> None:
    """Retain the exact semantic patch before its independent audit."""

    if output_dir is None:
        return
    os.makedirs(output_dir, exist_ok=True)
    patch_path = os.path.join(output_dir, "mechanism_stage_description_patch.json")
    with open(patch_path, "w", encoding="utf-8") as handle:
        json.dump(patch.model_dump(mode="json"), handle, indent=2)


def _write_mechanism_graph_patch_artifact(
    output_dir: str | None,
    patch: MechanismGraphPatch,
) -> None:
    """Retain the exact bounded graph patch before independent re-audit."""

    if output_dir is None:
        return
    os.makedirs(output_dir, exist_ok=True)
    patch_path = os.path.join(output_dir, "mechanism_graph_patch.json")
    with open(patch_path, "w", encoding="utf-8") as handle:
        json.dump(patch.model_dump(mode="json"), handle, indent=2)


def _resolve_mechanism_audit(
    candidate: MechanismTraceResult,
    extraction: ExtractionResult,
    hypothesis_space: HypothesisSpace,
    partition_audit: PartitionAudit,
    testing: TestingResult,
    discriminator_resolution: DiscriminatorAuditResolution,
    *,
    analyst_model: str | None,
    audit_model: str | None,
    trace_id: str,
    repair_attempts: int = 1,
    output_dir: str | None = None,
    verbose: bool = True,
    pass_label: str = "",
    source_scope_context: str | None = None,
    initial_repair_context: MechanismRepairContext | None = None,
    audit_num_retries: int | None = None,
    audit_validation_repair_attempts: int | None = None,
    analyst_num_retries: int | None = None,
    phase_context_factory: Callable[[str], ContextManager[None]] | None = None,
) -> tuple[MechanismTraceResult, MechanismAuditResolution]:
    """Audit a candidate DAG, repair material omissions, and bind final acceptance."""

    if repair_attempts < 0:
        raise ValueError("mechanism audit repair attempts must be >= 0")
    attempts: list[MechanismAuditAttempt] = []
    initial_repair_context = initial_repair_context or MechanismRepairContext(
        constraints=[]
    )
    current = candidate
    prefix = f"{pass_label} " if pass_label else ""

    def phase_context(phase: str) -> ContextManager[None]:
        if phase_context_factory is None:
            return nullcontext()
        return phase_context_factory(phase)

    while True:
        attempt_number = len(attempts) + 1
        _write_mechanism_attempt_artifact(
            output_dir,
            attempt_number=attempt_number,
            candidate=current,
        )
        if verbose:
            print(f"{prefix}Pass 4.6: Independent mechanism edge audit...")
        audit_repair_context = merge_mechanism_repair_contexts(
            initial_repair_context,
            build_mechanism_repair_context(attempts),
        )
        with phase_context("mechanism_audit"):
            critique = run_mechanism_critic(
                current,
                extraction,
                hypothesis_space,
                partition_audit,
                testing,
                discriminator_resolution,
                model=audit_model,
                trace_id=f"{trace_id}-mechanism-audit-{len(attempts) + 1}",
                source_scope_context=source_scope_context,
                repair_context=audit_repair_context,
                num_retries=audit_num_retries,
                validation_repair_attempts=audit_validation_repair_attempts,
                validation_artifact_dir=output_dir,
            )
        require_mechanism_critique_integrity(
            critique,
            current,
            extraction,
            hypothesis_space,
            audit_repair_context,
        )
        audit_attempt = MechanismAuditAttempt(
            attempt=len(attempts) + 1,
            action=(
                "initial_audit"
                if not attempts
                else "omission_repair_audit"
            ),
            reviewer_model=audit_model or DEFAULT_MODEL,
            candidate_mechanism_trace=current.model_copy(deep=True),
            candidate_mechanism_trace_sha256=mechanism_trace_sha256(current),
            critique=critique,
        )
        attempts.append(audit_attempt)
        _write_mechanism_attempt_artifact(
            output_dir,
            attempt_number=attempt_number,
            candidate=current,
            audit_attempt=audit_attempt,
        )
        material = material_mechanism_findings(critique)
        repair_context = merge_mechanism_repair_contexts(
            initial_repair_context,
            build_mechanism_repair_context(attempts),
        )
        if material:
            try:
                graph_patch_targets(critique)
                graph_patch_eligible = True
            except ValueError:
                graph_patch_eligible = False
            try:
                stage_description_patch_target_ids(critique)
                description_patch_eligible = True
            except ValueError:
                description_patch_eligible = False

            if graph_patch_eligible:
                source_critique = critique
                if verbose:
                    print(
                        "  Applying one hash-bound graph patch "
                        f"({', '.join(material)})"
                    )
                with phase_context("mechanism"):
                    graph_patch = run_mechanism_graph_patch(
                        current,
                        source_critique,
                        extraction,
                        hypothesis_space,
                        model=analyst_model,
                        trace_id=f"{trace_id}-mechanism-graph-patch",
                        repair_context=repair_context,
                        source_scope_context=source_scope_context,
                        num_retries=analyst_num_retries,
                    )
                _write_mechanism_graph_patch_artifact(output_dir, graph_patch)
                patched = apply_mechanism_graph_patch(
                    current,
                    source_critique,
                    graph_patch,
                )
                require_mechanism_trace_integrity(
                    patched,
                    extraction,
                    hypothesis_space,
                )
                patch_attempt_number = len(attempts) + 1
                _write_mechanism_attempt_artifact(
                    output_dir,
                    attempt_number=patch_attempt_number,
                    candidate=patched,
                )
                with phase_context("mechanism_audit"):
                    _graph_focused_critique, critique = run_mechanism_graph_patch_critic(
                        patched,
                        source_critique,
                        graph_patch,
                        extraction,
                        hypothesis_space,
                        model=audit_model,
                        trace_id=f"{trace_id}-mechanism-graph-patch-audit",
                        repair_context=repair_context,
                        source_scope_context=source_scope_context,
                        num_retries=audit_num_retries,
                    )
                audit_attempt = MechanismAuditAttempt(
                    attempt=patch_attempt_number,
                    action="graph_patch_audit",
                    reviewer_model=audit_model or DEFAULT_MODEL,
                    candidate_mechanism_trace=patched.model_copy(deep=True),
                    candidate_mechanism_trace_sha256=mechanism_trace_sha256(patched),
                    critique=critique,
                    graph_patch=graph_patch,
                )
                attempts.append(audit_attempt)
                _write_mechanism_attempt_artifact(
                    output_dir,
                    attempt_number=patch_attempt_number,
                    candidate=patched,
                    audit_attempt=audit_attempt,
                )
                current = patched
                material = material_mechanism_findings(critique)
                audit_repair_context = repair_context
                repair_context = merge_mechanism_repair_contexts(
                    initial_repair_context,
                    build_mechanism_repair_context(attempts),
                )
                if material:
                    blocked = MechanismAuditResolution(
                        status="blocked",
                        attempts=attempts,
                        repair_constraints=repair_context.constraints,
                        corrections=[],
                        final_mechanism_trace_sha256=mechanism_trace_sha256(current),
                        final_critique=critique,
                    )
                    _write_mechanism_audit_artifacts(output_dir, current, blocked)
                    raise MechanismAuditBlockedError(
                        "material findings remain after the bounded graph patch: "
                        + ", ".join(material)
                    )
            elif description_patch_eligible:
                source_critique = critique
                if verbose:
                    print(
                        "  Applying one hash-bound "
                        f"stage-description patch ({', '.join(material)})"
                    )
                with phase_context("mechanism"):
                    stage_patch = run_mechanism_stage_description_patch(
                        current,
                        source_critique,
                        extraction,
                        hypothesis_space,
                        model=analyst_model,
                        trace_id=f"{trace_id}-mechanism-stage-patch",
                        repair_context=repair_context,
                        source_scope_context=source_scope_context,
                        num_retries=analyst_num_retries,
                    )
                _write_mechanism_stage_patch_artifact(output_dir, stage_patch)
                patched = apply_mechanism_stage_description_patch(
                    current,
                    source_critique,
                    stage_patch,
                )
                require_mechanism_trace_integrity(
                    patched,
                    extraction,
                    hypothesis_space,
                )
                patch_attempt_number = len(attempts) + 1
                _write_mechanism_attempt_artifact(
                    output_dir,
                    attempt_number=patch_attempt_number,
                    candidate=patched,
                )
                with phase_context("mechanism_audit"):
                    _stage_focused_critique, critique = (
                        run_mechanism_stage_description_patch_critic(
                            patched,
                            source_critique,
                            stage_patch,
                            extraction,
                            hypothesis_space,
                            model=audit_model,
                            trace_id=f"{trace_id}-mechanism-stage-patch-audit",
                            repair_context=repair_context,
                            source_scope_context=source_scope_context,
                            num_retries=audit_num_retries,
                        )
                    )
                audit_attempt = MechanismAuditAttempt(
                    attempt=patch_attempt_number,
                    action="stage_description_patch_audit",
                    reviewer_model=audit_model or DEFAULT_MODEL,
                    candidate_mechanism_trace=patched.model_copy(deep=True),
                    candidate_mechanism_trace_sha256=mechanism_trace_sha256(
                        patched
                    ),
                    critique=critique,
                    stage_description_patch=stage_patch,
                )
                attempts.append(audit_attempt)
                _write_mechanism_attempt_artifact(
                    output_dir,
                    attempt_number=patch_attempt_number,
                    candidate=patched,
                    audit_attempt=audit_attempt,
                )
                current = patched
                material = material_mechanism_findings(critique)
                audit_repair_context = repair_context
                repair_context = merge_mechanism_repair_contexts(
                    initial_repair_context,
                    build_mechanism_repair_context(attempts),
                )
                if material:
                    blocked = MechanismAuditResolution(
                        status="blocked",
                        attempts=attempts,
                        repair_constraints=repair_context.constraints,
                        corrections=[],
                        final_mechanism_trace_sha256=mechanism_trace_sha256(current),
                        final_critique=critique,
                    )
                    _write_mechanism_audit_artifacts(output_dir, current, blocked)
                    raise MechanismAuditBlockedError(
                        "material stage findings remain after the bounded "
                        "description patch: "
                        + ", ".join(material)
                    )
            else:
                if len(attempts) > repair_attempts:
                    blocked = MechanismAuditResolution(
                        status="blocked",
                        attempts=attempts,
                        repair_constraints=repair_context.constraints,
                        corrections=[],
                        final_mechanism_trace_sha256=mechanism_trace_sha256(current),
                        final_critique=critique,
                    )
                    _write_mechanism_audit_artifacts(output_dir, current, blocked)
                    raise MechanismAuditBlockedError(
                        "material mechanism findings remain after bounded repair: "
                        + ", ".join(material)
                    )
                if verbose:
                    print(
                        "  Material mechanism omission: replacing the complete DAG "
                        f"({', '.join(material)})"
                    )
                with phase_context("mechanism"):
                    current = run_mechanism_trace(
                        extraction,
                        hypothesis_space,
                        partition_audit,
                        testing,
                        discriminator_resolution,
                        model=analyst_model,
                        trace_id=f"{trace_id}-mechanism-repair-{len(attempts)}",
                        critic_context=repair_context.model_dump_json(indent=2),
                        source_scope_context=source_scope_context,
                        num_retries=analyst_num_retries,
                        validation_repair_attempts=1,
                        validation_artifact_dir=output_dir,
                    )
                continue

        final_trace, corrections = apply_mechanism_critique(
            current,
            critique,
            extraction,
            hypothesis_space,
            audit_repair_context,
        )
        require_mechanism_trace_integrity(
            final_trace,
            extraction,
            hypothesis_space,
        )
        resolution = MechanismAuditResolution(
            status="accepted",
            attempts=attempts,
            repair_constraints=repair_context.constraints,
            corrections=corrections,
            final_mechanism_trace_sha256=mechanism_trace_sha256(final_trace),
            final_critique=critique,
        )
        require_mechanism_audit_integrity(
            resolution,
            final_trace,
            extraction,
            hypothesis_space,
            initial_repair_context,
        )
        _write_mechanism_audit_artifacts(output_dir, final_trace, resolution)
        if verbose:
            print(
                f"  Mechanism audit accepted after {len(attempts)} attempt(s); "
                f"{len(corrections)} edge(s) weakened"
            )
        return final_trace, resolution


def _run_core_passes(
    extraction: ExtractionResult,
    hypothesis_space: HypothesisSpace,
    partition_audit: PartitionAudit,
    *,
    inference_mode: InferenceMode = "theory_first",
    model: str | None = None,
    verbose: bool = True,
    pass_label: str = "",
    trace_id: str | None = None,
    prior_specification: PriorSpecification | None = None,
    post_selection_evidence_ids: list[str] | None = None,
    post_selection_reason: EvidenceExclusionReason = "post_selection_refinement",
    critic_context: str | None = None,
    source_scope_context: str | None = None,
    source_ids: list[str] | None = None,
    discriminator_audit_model: str | None = None,
    discriminator_audit_attempts: int = 0,
    mechanism_audit_model: str | None = None,
    mechanism_audit_attempts: int = 1,
    output_dir: str | None = None,
) -> tuple[
    TestingResult,
    TestingResult,
    DiscriminatorAuditResolution,
    AbsenceResult,
    BayesianResult,
    DiagnosticMatrix,
    MechanismTraceResult,
    MechanismAuditResolution,
]:
    """Run testing, audit, absence, update, diagnostics, and mechanism passes.

    Returns typed core artifacts without synthesis.
    critic_context: optional critic summary to inject into Pass 3 re-elicitation.
    """
    prefix = f"{pass_label} " if pass_label else ""
    prior_specification = _resolve_prior_specification(
        extraction,
        hypothesis_space,
        prior_specification,
    )

    if verbose:
        ctx_note = " [with critic context]" if critic_context else ""
        print(f"{prefix}Pass 3: Diagnostic testing ({len(hypothesis_space.hypotheses)} hypotheses){ctx_note}...")
    raw_testing = run_test(
        extraction,
        hypothesis_space,
        partition_audit,
        model=model,
        trace_id=trace_id,
        critic_context=critic_context,
        prior_evidence_ids=prior_specification.evidence_ids,
        post_selection_evidence_ids=post_selection_evidence_ids,
        post_selection_reason=post_selection_reason,
        source_scope_context=source_scope_context,
    )
    if verbose:
        print(f"  {len(raw_testing.evidence_likelihoods)} evidence likelihood vectors "
              f"across {len(hypothesis_space.hypotheses)} hypotheses")

    testing, discriminator_audit_resolution = _resolve_discriminator_audit(
        extraction,
        hypothesis_space,
        partition_audit,
        raw_testing,
        inference_mode=inference_mode,
        analyst_model=model,
        audit_model=discriminator_audit_model or model,
        trace_id=trace_id or uuid4().hex[:8],
        prior_evidence_ids=prior_specification.evidence_ids,
        post_selection_evidence_ids=post_selection_evidence_ids,
        post_selection_reason=post_selection_reason,
        critic_context=critic_context,
        source_scope_context=source_scope_context,
        repair_attempts=discriminator_audit_attempts,
        output_dir=output_dir,
        verbose=verbose,
        pass_label=pass_label,
    )

    if verbose:
        print(f"{prefix}Pass 3b: Evaluating absence of evidence...")
    absence = run_absence(
        extraction,
        hypothesis_space,
        testing,
        model=model,
        trace_id=trace_id,
        source_scope_context=source_scope_context,
    )
    if verbose:
        n_abs = len(absence.evaluations)
        n_damaging = sum(1 for a in absence.evaluations if a.severity == "damaging")
        print(f"  {n_abs} absence findings ({n_damaging} damaging)")

    bayesian_testing = testing
    confirmatory_absence = (
        inference_mode in {"theory_first", "discovery_evaluation_split"}
        and not post_selection_evidence_ids
        and bool(source_ids)
        and bool(absence.source_silence_likelihoods)
    )
    if confirmatory_absence:
        if verbose:
            print(f"{prefix}Pass 3c: Independent source-silence audit...")
        absence_audit = run_source_silence_audit(
            absence,
            testing=testing,
            extraction=extraction,
            source_scope_context=source_scope_context or "",
            inference_mode=inference_mode,
            hypothesis_ids=[item.id for item in hypothesis_space.hypotheses],
            source_ids=source_ids or [],
            model=discriminator_audit_model or model,
            trace_id=f"{trace_id or uuid4().hex[:8]}-absence-audit",
        )
        bayesian_testing = apply_accepted_source_silence(
            testing,
            extraction,
            absence,
            absence_audit,
        )
        absence = absence.model_copy(
            update={
                "source_silence_audit_resolution": absence_audit,
                "absence_adjusted_testing": bayesian_testing,
            },
            deep=True,
        )
        if output_dir:
            with open(
                os.path.join(output_dir, "absence_audit_resolution.json"),
                "w",
                encoding="utf-8",
            ) as handle:
                json.dump(absence_audit.model_dump(), handle, indent=2)
            with open(
                os.path.join(output_dir, "absence_adjusted_testing.json"),
                "w",
                encoding="utf-8",
            ) as handle:
                json.dump(bayesian_testing.model_dump(), handle, indent=2)

    if verbose:
        print(f"{prefix}Bayesian updating...")
    if confirmatory_absence:
        no_absence_bayesian = run_bayesian_policy_analysis(
            testing,
            [h.id for h in hypothesis_space.hypotheses],
            priors=prior_specification.weights,
            include_residual=True,
            evidence_types={ev.id: ev.evidence_type for ev in extraction.evidence},
        )
        absence = absence.model_copy(
            update={"no_absence_bayesian": no_absence_bayesian},
            deep=True,
        )
    bayesian = run_bayesian_policy_analysis(
        bayesian_testing,
        [h.id for h in hypothesis_space.hypotheses],
        priors=prior_specification.weights,
        include_residual=True,
        evidence_types={ev.id: ev.evidence_type for ev in extraction.evidence},
    )
    if verbose:
        top = bayesian.ranking[0] if bayesian.ranking else "none"
        top_post = next(
            (p.final_posterior for p in bayesian.posteriors if p.hypothesis_id == top), 0
        )
        print(f"  Top hypothesis: {top} (support: {top_post:.3f})")

    interpretive_ids = {ev.id for ev in extraction.evidence if ev.evidence_type == "interpretive"}
    diagnostic_matrix = compute_diagnostic_matrix(
        testing,
        hypothesis_space,
        partition_audit,
        interpretive_ids,
    )
    if verbose:
        n_pairs = len(diagnostic_matrix.rival_pair_diagnostics)
        n_capped = len(diagnostic_matrix.pairs_without_discriminators)
        cap_note = f" [{n_capped} pairs capped — no discriminators]" if n_capped else ""
        print(f"  Diagnostic matrix: {n_pairs} rival pairs{cap_note}")

    if verbose:
        print(f"{prefix}Temporal mechanism assessment...")
    mechanism_trace = run_mechanism_trace(
        extraction,
        hypothesis_space,
        partition_audit,
        testing,
        discriminator_audit_resolution,
        model=model,
        trace_id=f"{trace_id or uuid4().hex[:8]}-mechanism",
        source_scope_context=source_scope_context,
    )
    mechanism_trace, mechanism_audit_resolution = _resolve_mechanism_audit(
        mechanism_trace,
        extraction,
        hypothesis_space,
        partition_audit,
        testing,
        discriminator_audit_resolution,
        analyst_model=model,
        audit_model=mechanism_audit_model or model,
        trace_id=trace_id or uuid4().hex[:8],
        repair_attempts=mechanism_audit_attempts,
        output_dir=output_dir,
        verbose=verbose,
        pass_label=pass_label,
        source_scope_context=source_scope_context,
    )
    if verbose:
        print(
            f"  Mechanism DAG: {len(mechanism_trace.stages)} stages, "
            f"{len(mechanism_trace.edges)} forward edges"
        )

    return (
        raw_testing,
        testing,
        discriminator_audit_resolution,
        absence,
        bayesian,
        diagnostic_matrix,
        mechanism_trace,
        mechanism_audit_resolution,
    )


def _run_passes_3_plus(
    extraction: ExtractionResult,
    hypothesis_space: HypothesisSpace,
    partition_audit: PartitionAudit,
    text: str,
    *,
    inference_mode: InferenceMode = "theory_first",
    model: str | None = None,
    verbose: bool = True,
    pass_label: str = "",
    trace_id: str | None = None,
    prior_specification: PriorSpecification | None = None,
    post_selection_evidence_ids: list[str] | None = None,
    post_selection_reason: EvidenceExclusionReason = "post_selection_refinement",
    source_scope_context: str | None = None,
    source_ids: list[str] | None = None,
    discriminator_audit_model: str | None = None,
    discriminator_audit_attempts: int = 0,
    mechanism_audit_model: str | None = None,
    mechanism_audit_attempts: int = 1,
    output_dir: str | None = None,
) -> tuple:
    """Run passes 3 through 4.6, then synthesize in Pass 5."""
    prefix = f"{pass_label} " if pass_label else ""

    (
        raw_testing,
        testing,
        discriminator_audit_resolution,
        absence,
        bayesian,
        diagnostic_matrix,
        mechanism_trace,
        mechanism_audit_resolution,
    ) = _run_core_passes(
        extraction, hypothesis_space, partition_audit,
        inference_mode=inference_mode,
        model=model,
        verbose=verbose,
        pass_label=pass_label,
        trace_id=trace_id,
        prior_specification=prior_specification,
        post_selection_evidence_ids=post_selection_evidence_ids,
        post_selection_reason=post_selection_reason,
        source_scope_context=source_scope_context,
        source_ids=source_ids,
        discriminator_audit_model=discriminator_audit_model,
        discriminator_audit_attempts=discriminator_audit_attempts,
        mechanism_audit_model=mechanism_audit_model,
        mechanism_audit_attempts=mechanism_audit_attempts,
        output_dir=output_dir,
    )

    if verbose:
        print(f"{prefix}Pass 5: Synthesizing analysis...")
    synthesis = run_synthesize(
        extraction,
        hypothesis_space,
        testing,
        bayesian,
        absence,
        diagnostic_matrix,
        partition_audit,
        mechanism_trace,
        model=model,
        trace_id=trace_id,
        source_scope_context=source_scope_context,
    )
    if verbose:
        print(f"  Narrative: {len(synthesis.analytical_narrative)} chars")

    return (
        raw_testing,
        testing,
        discriminator_audit_resolution,
        absence,
        bayesian,
        synthesis,
        diagnostic_matrix,
        mechanism_trace,
        mechanism_audit_resolution,
    )


def _compute_critic_delta(
    base_bayesian: BayesianResult,
    critic_bayesian: BayesianResult,
    critic_result: CriticResult,
) -> list[CriticDelta]:
    """Compute per-hypothesis posterior change between base and critic runs."""
    base_map = {p.hypothesis_id: p for p in base_bayesian.posteriors}
    critic_map = {p.hypothesis_id: p for p in critic_bayesian.posteriors}

    deltas = []
    all_hyp_ids = sorted(set(base_map) | set(critic_map))
    for hyp_id in all_hyp_ids:
        base_p = base_map.get(hyp_id)
        critic_p = critic_map.get(hyp_id)
        post_base = base_p.final_posterior if base_p else 0.0
        post_critic = critic_p.final_posterior if critic_p else 0.0

        # Top-driver change: IDs in one set but not the other
        base_drivers = set(base_p.top_drivers) if base_p else set()
        critic_drivers = set(critic_p.top_drivers) if critic_p else set()
        driver_changes = (
            [f"added:{eid}" for eid in sorted(critic_drivers - base_drivers)]
            + [f"removed:{eid}" for eid in sorted(base_drivers - critic_drivers)]
        )

        # Count critic findings that target this hypothesis or its evidence top-drivers.
        # causal_edge findings are graph-level and not attributed to a specific hypothesis.
        hyp_finding_count = sum(
            1 for f in critic_result.findings
            if (
                (f.target_type == "hypothesis" and f.target == hyp_id)
                or (f.target_type == "evidence" and f.target in (base_drivers | critic_drivers))
            )
        )

        deltas.append(CriticDelta(
            hypothesis_id=hyp_id,
            posterior_base=round(post_base, 6),
            posterior_critic=round(post_critic, 6),
            delta=round(post_critic - post_base, 6),
            top_driver_change=driver_changes,
            critic_findings_count=hyp_finding_count,
        ))
    return deltas


@with_llm_run_config
def run_pipeline(
    text: str,
    *,
    model: str | None = None,
    extraction_model: str | None = None,
    verbose: bool = True,
    review: bool = False,
    review_fn: Callable[[HypothesisSpace, str | None], HypothesisSpace] | None = None,
    partition_review: bool = False,
    partition_review_fn: Callable[[HypothesisSpace, PartitionAudit, str | None], HypothesisSpace] | None = None,
    partition_repair_attempts: int = 2,
    partition_repair_model: str | None = None,
    grounding_repair_model: str | None = None,
    prediction_audit_model: str | None = None,
    prediction_audit_attempts: int = 0,
    mechanism_audit_model: str | None = None,
    mechanism_audit_attempts: int = 1,
    output_dir: str | None = None,
    theories: str | None = None,
    frozen_hypothesis_space: HypothesisSpace | None = None,
    research_question: str | None = None,
    refine: bool = False,
    from_result: ProcessTracingResult | None = None,
    source_packet: SourcePacket | None = None,
    source_packet_path: str | None = None,
    segmented_source: SegmentedSourceBundleV1 | None = None,
    trace_id: str | None = None,
    prior_specification: PriorSpecification | None = None,
    inference_design: InferenceDesign | None = None,
    max_budget: float | None = None,
    budget_scope_trace_id: str | None = None,
    reasoning_effort: str | None = None,
    model_justification: str | None = None,
    llm_client_runtime: LLMClientRuntimeBinding | None = None,
    llm_timeout: int | None = None,
    resume_source_trace_id: str | None = None,
    resume_target_trace_id: str | None = None,
    resume_ledger_path: str | None = None,
    critic: bool = False,
    critic_model: str | None = None,
    central_claim_review: bool = False,
    central_claim_review_workers: int = 1,
) -> ProcessTracingResult:
    """Run the full process tracing pipeline.

    Pass 1: Extract → Pass 2: Hypothesize → [Review] → Pass 3: Test →
    3a: Independent discriminator audit → 3b: Absence → Bayes → 3.6 →
    [Pass 3.7: Critic] → 4.5: Mechanism DAG → 4.6: Independent mechanism
    audit → Pass 5: Synthesize
    With --refine: → Pass 6: Refine → [Review] → Apply → Re-run passes 3-5

    Args:
        review: If True, pause after hypothesis generation (and after refinement) for user review.
        extraction_model: Optional model used only for Pass 1 inventory,
            consolidation, edge production, and default quote-anchor repair.
            Defaults to the analyst model.
        reasoning_effort: Explicit shared-client reasoning policy inherited by
            every LLM call in the run.
        budget_scope_trace_id: Optional shared aggregate admission scope. Use
            one stable value across related pipeline invocations to enforce a
            single budget cap without collapsing their analytical trace IDs.
        central_claim_review_workers: Independent final-prose targets to review
            concurrently. Shared aggregate budget scopes currently require one
            worker because their admission mode is sequential.
        model_justification: Durable route-selection rationale inherited by
            every LLM call in the run.
        llm_client_runtime: Validated imported shared-client provenance retained
            in new result artifacts.
        llm_timeout: Positive shared-client hard deadline in seconds for each
            structured call.
        review_fn: Custom review function. Defaults to interactive CLI review.
        partition_review: If True, pause after Pass 2.5 partition audit when quality is
            needs_review; presents problem pairs and remediation, lets user edit hypotheses.
        partition_review_fn: Custom partition review function. Defaults to interactive CLI review.
        partition_repair_attempts: Maximum automated partition rewrites after audit/review.
        partition_repair_model: Optional stronger or independent model used only to rewrite
            blocked partitions. The analyst model still re-audits every rewrite.
        grounding_repair_model: Optional model used only to copy exact quote anchors for
            otherwise retained extraction/refinement claims whose first anchor did not resolve.
        prediction_audit_model: Optional model for the independent exact-quote semantic
            audit. Defaults to partition_repair_model, then critic_model, then the analyst.
        prediction_audit_attempts: Maximum Pass 3 re-elicitations after semantic rejection.
        mechanism_audit_model: Optional model for the independent stage/edge
            mechanism audit. Defaults through the other reviewer models to the analyst.
        mechanism_audit_attempts: Maximum full-DAG replacements after a material
            omission. Conservative edge weakening does not consume this budget.
        output_dir: Directory for writing review files.
        theories: Optional plain-text theoretical frameworks for hypothesis generation.
        frozen_hypothesis_space: Optional exact pre-corpus hypothesis space. It
            bypasses hypothesis generation but not extraction, partition audit,
            testing, mechanism tracing, or synthesis.
        research_question: Optional researcher-pinned research question. Pins the outcome to
            explain (reproducible across runs); when None the LLM selects it.
        refine: If True, run analytical refinement after initial pipeline, then re-run passes 3+.
        from_result: Reuse passes 1-5 from an integrity-valid existing result. Implies refine.
        source_packet: Optional source-packet contract that pins source scope,
            observability assumptions, and the research question before inference.
        segmented_source: Optional validated producer-owned source partition
            used only to bound Pass 1 and retain source lineage.
        prior_specification: Typed prior weights plus any corpus or external inputs used
            to construct them. Defaults to a provenance-free uniform prior.
        critic: If True, run structural critic (Pass 3.7) after diagnostic matrix and before
            synthesis. Writes result_base.json, result_critic.json, and critic_delta.json to
            output_dir. Re-elicits Pass 3 when high-severity findings are present.
    """
    if central_claim_review_workers > 1 and budget_scope_trace_id is not None:
        raise ValueError(
            "concurrent central-claim review cannot use a sequential shared budget scope"
        )
    t0 = time.time()
    supplied_inference_design = inference_design is not None
    inference_design = inference_design or InferenceDesign(
        mode="exploratory_full_corpus"
    )
    inference_design = _bind_inference_design(inference_design, theories)
    hypothesis_generation_view: HypothesisGenerationView | None = None
    inference_status = _initial_inference_status(inference_design)
    post_selection_evidence_ids: list[str] = []
    post_selection_reason: EvidenceExclusionReason = (
        "same_case_theory_reuse"
        if inference_design.mode == "theory_first"
        and inference_design.theory_evidence_relationship != "independent"
        else "post_selection_refinement"
    )
    if critic and refine:
        raise ValueError(
            "--critic and --refine cannot be used together. "
            "critic_delta.json is computed against the pre-refine bayesian result; "
            "if refinement then overwrites it, the delta becomes inconsistent with result.json. "
            "Run --critic alone to get the ablation pair, or --refine alone for analytical refinement."
        )

    if trace_id is None:
        trace_id = uuid4().hex[:8]
    if prediction_audit_attempts < 0:
        raise ValueError("prediction audit attempts must be >= 0")
    if mechanism_audit_attempts < 0:
        raise ValueError("mechanism audit attempts must be >= 0")
    resolved_prediction_audit_model = (
        prediction_audit_model or partition_repair_model or critic_model or model
    )
    resolved_mechanism_audit_model = (
        mechanism_audit_model
        or prediction_audit_model
        or critic_model
        or partition_repair_model
        or model
    )
    source_text_sha256 = _source_text_sha256(text)
    segmented_source_summary: SegmentedSourceSummary | None
    if segmented_source is not None:
        reconstructed_source = "".join(
            atom.exact_text for atom in segmented_source.source_document.atoms
        )
        if reconstructed_source != text:
            raise ValueError(
                "segmented source atoms do not reconstruct the exact pipeline input"
            )
        segmented_source_summary = SegmentedSourceSummary(
            producer_revision=segmented_source.producer_revision,
            source_document_id=segmented_source.source_document.source_document_id,
            source_digest=segmented_source.source_document.source_digest,
            source_content_sha256=(
                segmented_source.source_document.source_content_sha256
            ),
            segmentation_plan_id=segmented_source.segmentation_plan.plan_id,
            segmentation_plan_digest=segmented_source.segmentation_plan.plan_digest,
            atom_count=len(segmented_source.source_document.atoms),
            work_unit_count=len(segmented_source.work_units),
            maximum_work_unit_characters=max(
                len(unit.exact_text) for unit in segmented_source.work_units
            ),
        )
    else:
        segmented_source_summary = (
            from_result.segmented_source if from_result is not None else None
        )

    if frozen_hypothesis_space is not None and from_result is not None:
        raise ValueError("frozen hypotheses cannot be combined with --from-result")
    if frozen_hypothesis_space is not None:
        if inference_design.mode != "theory_first":
            raise ValueError("frozen hypotheses require a theory_first inference design")
        if review or partition_review or refine:
            raise ValueError(
                "frozen hypotheses cannot be combined with hypothesis review, "
                "partition review, or refinement"
            )
        if partition_repair_attempts != 0:
            raise ValueError("frozen hypotheses require partition_repair_attempts=0")
        if research_question != frozen_hypothesis_space.research_question:
            raise ValueError("frozen hypotheses target a different research question")
        empty_extraction = ExtractionResult(
            summary="No corpus evidence exposed during frozen hypothesis formulation."
        )
        require_hypothesis_exposure_integrity(
            empty_extraction,
            frozen_hypothesis_space,
            build_hypothesis_generation_view(empty_extraction, inference_design),
        )

    if from_result is not None and source_packet is not None:
        raise ValueError(
            "--source-packet cannot be combined with --from-result because "
            "--from-result reuses an existing hypothesis space"
        )
    if from_result is not None and segmented_source is not None:
        raise ValueError(
            "--segmented-source cannot be combined with --from-result because "
            "--from-result reuses an existing extraction"
        )
    if from_result is not None and prior_specification is not None:
        raise ValueError(
            "--from-result reuses its stored prior specification; a new prior requires "
            "a fresh run from source"
        )
    if from_result is not None and supplied_inference_design:
        raise ValueError(
            "--from-result reuses its stored inference design; a new design requires "
            "a fresh run from source"
        )

    source_packet_ids: list[str] = []
    if source_packet is not None:
        source_packet_ids = require_stable_source_ids(source_packet)
        packet_rq = source_packet.research_question.strip()
        pinned_rq = research_question.strip() if research_question else None
        if pinned_rq and pinned_rq != packet_rq:
            raise ValueError(
                "--research-question conflicts with source_packet.research_question "
                f"(research_question={pinned_rq!r}, source_packet={packet_rq!r})"
            )
        research_question = packet_rq
        if verbose:
            print(
                f"Source packet: {source_packet.case_name} "
                f"({len(source_packet.source_candidates)} sources, "
                f"{len(source_packet.known_gaps)} known gaps)"
            )

    source_packet_summary = (
        source_packet.to_summary(source_packet_path)
        if source_packet is not None
        else from_result.source_packet if from_result is not None else None
    )
    source_scope_context = (
        source_packet.to_prompt_context()
        if source_packet is not None
        else json.dumps(source_packet_summary.model_dump(), indent=2)
        if source_packet_summary is not None
        else None
    )
    source_coverage = from_result.source_coverage if from_result is not None else None
    if from_result is not None and source_packet_summary is not None:
        if not from_result.extraction.source_spans:
            raise ValueError(
                "--from-result has source-packet metadata but no retained source-span "
                "catalog; rerun from source before refinement"
            )
        if source_coverage is None or not source_coverage.items:
            raise ValueError(
                "--from-result has source-packet metadata but no source coverage; "
                "rerun from source before refinement"
            )
        source_packet_ids = [item.source_id.strip() for item in source_coverage.items]
        if any(not source_id for source_id in source_packet_ids):
            raise ValueError("--from-result source coverage contains a blank source_id")
        if len(source_packet_ids) != len(set(source_packet_ids)):
            raise ValueError("--from-result source coverage contains duplicate source_ids")
        known_source_ids = set(source_packet_ids)
        missing_source_ids = [
            evidence.id for evidence in from_result.extraction.evidence if not evidence.source_id
        ]
        unknown_source_ids = {
            evidence.id: evidence.source_id
            for evidence in from_result.extraction.evidence
            if evidence.source_id and evidence.source_id not in known_source_ids
        }
        if missing_source_ids or unknown_source_ids:
            raise ValueError(
                "--from-result source-packet evidence lineage is incomplete: "
                f"missing={sorted(missing_source_ids)}, unknown={unknown_source_ids}"
            )

    # Input validation — catch garbage/trivial input before burning 9+ LLM calls
    if from_result is None:
        word_count = len(text.split())
        if word_count < 300:
            raise ValueError(
                f"Input text too short ({word_count} words). "
                f"Process tracing requires at least 300 words of substantive text "
                f"to extract meaningful evidence and hypotheses."
            )

    partition_audit: PartitionAudit | None = None
    partition_resolution: PartitionResolution | None = None
    discriminator_audit_resolution: DiscriminatorAuditResolution | None = None

    if from_result is not None:
        refine = True
        source_text_sha256 = _validate_from_result_source(text, from_result)
        extraction = from_result.extraction
        hypothesis_space = from_result.hypothesis_space
        if (
            from_result.inference_design is None
            or from_result.hypothesis_generation_view is None
            or from_result.inference_status == "legacy_unclassified"
        ):
            raise ValueError(
                "--from-result has no valid inference-exposure lineage; rerun from source"
            )
        inference_design = from_result.inference_design
        post_selection_reason = (
            "same_case_theory_reuse"
            if inference_design.mode == "theory_first"
            and inference_design.theory_evidence_relationship != "independent"
            else "post_selection_refinement"
        )
        hypothesis_generation_view = from_result.hypothesis_generation_view
        inference_status = from_result.inference_status
        post_selection_evidence_ids = list(from_result.post_selection_evidence_ids)
        validate_hypothesis_provenance(
            extraction,
            hypothesis_space,
            hypothesis_generation_view,
        )
        require_hypothesis_exposure_integrity(
            extraction,
            hypothesis_space,
            hypothesis_generation_view,
        )
        added_ids, removed_ids = refinement_evidence_delta(from_result.refinement)
        require_generation_view_integrity(
            extraction,
            inference_design,
            hypothesis_generation_view,
            added_evidence_ids=added_ids,
            removed_evidence_ids=removed_ids,
        )
        if from_result.prior_specification is None:
            raise ValueError(
                "--from-result has no prior provenance; rerun from source before refinement"
            )
        prior_specification = _resolve_prior_specification(
            extraction,
            hypothesis_space,
            from_result.prior_specification,
        )
        require_evidence_exclusion_integrity(
            from_result.testing,
            hypothesis_space,
            prior_specification.evidence_ids,
            post_selection_evidence_ids,
            {item.id for item in extraction.evidence},
            post_selection_reason,
        )
        partition_audit = from_result.partition_audit
        if partition_audit is None:
            raise ValueError(
                "--from-result has no partition audit; rerun from source before refinement"
            )
        require_adequate_partition(hypothesis_space, partition_audit)
        require_prediction_lineage_integrity(
            from_result.testing,
            hypothesis_space,
            partition_audit,
            excluded_evidence_ids={
                exclusion.evidence_id
                for exclusion in from_result.testing.evidence_exclusions
            },
        )
        discriminator_audit_resolution = require_discriminator_audit_integrity(
            from_result.discriminator_audit_resolution,
            extraction,
            hypothesis_space,
            partition_audit,
            from_result.testing,
            inference_mode=inference_design.mode,
        )
        if from_result.mechanism_trace is None:
            raise ValueError(
                "--from-result has no temporal mechanism trace; rerun from source"
            )
        mechanism_audit_resolution = require_mechanism_audit_integrity(
            from_result.mechanism_audit_resolution,
            from_result.mechanism_trace,
            extraction,
            hypothesis_space,
        )
        partition_resolution = from_result.partition_resolution or PartitionResolution(
            status="accepted",
            attempts=[
                PartitionAttempt(
                    attempt=1,
                    action="loaded_result_audit",
                    hypothesis_space=hypothesis_space.model_copy(deep=True),
                    audit=partition_audit,
                )
            ],
            final_audit=partition_audit,
        )
        if verbose:
            print(f"Loaded from existing result: {len(extraction.evidence)} evidence, "
                  f"{len(hypothesis_space.hypotheses)} hypotheses")
    else:
        pre_corpus_hypothesis_space: HypothesisSpace | None = None
        extraction_focus_context: str | None = None
        if inference_design.mode == "theory_first":
            if verbose:
                print(
                    "Pass 2/4: Freezing theory-first hypothesis space "
                    "before corpus extraction..."
                )
            if frozen_hypothesis_space is not None:
                pre_corpus_hypothesis_space = frozen_hypothesis_space.model_copy(
                    deep=True
                )
            else:
                empty_extraction = ExtractionResult(
                    summary="No corpus evidence exposed during theory-first formulation."
                )
                pre_corpus_hypothesis_space = run_hypothesize(
                    empty_extraction,
                    model=model,
                    theories=theories,
                    research_question=research_question,
                    generation_view=build_hypothesis_generation_view(
                        empty_extraction,
                        inference_design,
                    ),
                    trace_id=f"{trace_id}-pre-corpus-hypotheses",
                )
            extraction_focus_context = _theory_first_extraction_focus(
                pre_corpus_hypothesis_space
            )
        if verbose:
            print("Pass 1/4: Extracting causal graph...")
        extraction = run_extract(
            text,
            model=extraction_model or model,
            repair_model=grounding_repair_model,
            analysis_focus_context=extraction_focus_context,
            source_packet_context=source_packet.to_prompt_context() if source_packet else None,
            source_packet_ids=source_packet_ids,
            source_packet_markers=(
                {
                    source.source_id.strip(): list(source.text_markers)
                    for source in source_packet.source_candidates
                    if source.source_id and source.source_id.strip()
                }
                if source_packet is not None
                else None
            ),
            segmented_source=segmented_source,
            trace_id=trace_id,
        )
        if verbose:
            print(f"  Extracted {len(extraction.events)} events, {len(extraction.evidence)} evidence, "
                  f"{len(extraction.hypotheses_in_text)} hypotheses")

        hypothesis_generation_view = _validate_inference_design(
            inference_design,
            extraction,
            source_packet,
            theories,
        )
        post_selection_evidence_ids = _theory_reuse_evidence_ids(
            inference_design,
            extraction,
        )

        if pre_corpus_hypothesis_space is not None:
            hypothesis_space = pre_corpus_hypothesis_space
            require_hypothesis_exposure_integrity(
                extraction,
                hypothesis_space,
                hypothesis_generation_view,
            )
        else:
            if verbose:
                extra = " (with user theories)" if theories else ""
                print(f"Pass 2/4: Building hypothesis space{extra}...")
            hypothesis_space = run_hypothesize(
                extraction, model=model, theories=theories,
                research_question=research_question,
                source_packet_context=(
                    source_packet.to_prompt_context()
                    if source_packet is not None
                    and inference_design.mode == "exploratory_full_corpus"
                    else None
                ),
                generation_view=hypothesis_generation_view,
                trace_id=trace_id,
            )
        if verbose:
            print(f"  {len(hypothesis_space.hypotheses)} hypotheses "
                  f"(text + rivals), research question: {hypothesis_space.research_question[:80]}...")

        # Optional human review checkpoint
        if review:
            fn = review_fn or _default_review
            hypothesis_space = fn(hypothesis_space, output_dir)
            inference_status = "exploratory_post_selection"

        if verbose:
            print("Pass 2.5: Hypothesis partition audit and decision gate...")
        hypothesis_space, partition_audit, partition_resolution = _resolve_partition(
            extraction,
            hypothesis_space,
            generation_view=hypothesis_generation_view,
            model=model,
            repair_model=partition_repair_model,
            trace_id=trace_id,
            output_dir=output_dir,
            verbose=verbose,
            partition_review=partition_review,
            partition_review_fn=partition_review_fn,
            repair_attempts=partition_repair_attempts,
        )
        if verbose:
            quality = partition_audit.overall_quality
            n_pairs = len(partition_audit.rival_pairs)
            warning_count = len(partition_audit.decision_warnings)
            print(
                f"  {n_pairs} rival pairs, quality={quality}"
                f"{', '+str(warning_count)+' advisory warning(s)' if warning_count else ''}; "
                f"accepted after {len(partition_resolution.attempts)} audit(s)"
            )
        if any(
            attempt.action == "manual_review"
            for attempt in partition_resolution.attempts
        ):
            inference_status = "exploratory_post_selection"

        prior_specification = _resolve_prior_specification(
            extraction,
            hypothesis_space,
            prior_specification,
        )

    if partition_audit is None:
        raise RuntimeError("accepted partition audit missing before diagnostic testing")

    if source_packet is not None:
        source_coverage = build_source_coverage(source_packet, text, extraction)
    source_opportunity_ids = [
        item.source_id
        for item in source_coverage.items
        if item.covered_in_input
    ] if source_coverage is not None else []

    # Run passes 3-4 (initial)
    critic_result: CriticResult | None = None

    if from_result is not None:
        raw_testing = from_result.testing
        if discriminator_audit_resolution is None:
            raise RuntimeError("validated discriminator audit resolution is missing")
        testing = (
            from_result.effective_testing
            or discriminator_audit_resolution.effective_testing
            or raw_testing
        )
        absence = from_result.absence
        bayesian = from_result.bayesian
        synthesis = from_result.synthesis
        diagnostic_matrix = from_result.diagnostic_matrix
        mechanism_trace = from_result.mechanism_trace
        if verbose:
            print("Reusing loaded testing, update, absence, and synthesis before refinement.")
    elif critic:
        # Run core passes (3, 3b, Bayesian, 3.6) without synthesis first
        if verbose:
            print("Pass 3/4: Running core passes (critic mode — synthesis deferred)...")
        (
            raw_testing,
            testing,
            discriminator_audit_resolution,
            absence,
            bayesian,
            diagnostic_matrix,
            mechanism_trace,
            mechanism_audit_resolution,
        ) = _run_core_passes(
            extraction, hypothesis_space, partition_audit,
            inference_mode=inference_design.mode,
            model=model,
            verbose=verbose,
            trace_id=trace_id,
            prior_specification=prior_specification,
            post_selection_evidence_ids=post_selection_evidence_ids,
            post_selection_reason=post_selection_reason,
            source_scope_context=source_scope_context,
            source_ids=source_opportunity_ids,
            discriminator_audit_model=resolved_prediction_audit_model,
            discriminator_audit_attempts=prediction_audit_attempts,
            mechanism_audit_model=resolved_mechanism_audit_model,
            mechanism_audit_attempts=mechanism_audit_attempts,
            output_dir=output_dir,
        )

        # Run synthesis for the base snapshot (needed for result_base.json audit)
        if verbose:
            print("Pass 4 (base): Synthesizing for base snapshot...")
        synthesis_base = run_synthesize(
            extraction, hypothesis_space, testing, bayesian, absence, diagnostic_matrix,
            partition_audit,
            mechanism_trace,
            model=model, trace_id=f"{trace_id}-base",
            source_scope_context=source_scope_context,
        )

        # Write result_base.json
        if output_dir:
            base_result = ProcessTracingResult(
                llm_client_runtime=llm_client_runtime,
                llm_timeout_seconds=llm_timeout,
                source_text_sha256=source_text_sha256,
                segmented_source=segmented_source_summary,
                extraction=extraction,
                hypothesis_space=hypothesis_space,
                prior_specification=prior_specification,
                partition_audit=partition_audit,
                partition_resolution=partition_resolution,
                discriminator_audit_resolution=discriminator_audit_resolution,
                diagnostic_matrix=diagnostic_matrix,
                testing=raw_testing,
                effective_testing=testing,
                mechanism_trace=mechanism_trace,
                mechanism_audit_resolution=mechanism_audit_resolution,
                absence=absence,
                bayesian=bayesian,
                synthesis=synthesis_base,
                source_packet=source_packet_summary,
            )
            base_path = os.path.join(output_dir, "result_base.json")
            with open(base_path, "w", encoding="utf-8") as f:
                json.dump(base_result.model_dump(), f, indent=2)
            if verbose:
                print(f"  Base snapshot: {base_path}")

        # Run structural critic (Pass 3.7)
        if verbose:
            print("Pass 3.7: Structural critic review...")
        critic_result = run_critic(
            extraction, hypothesis_space, testing, diagnostic_matrix, absence,
            model=critic_model or model, trace_id=f"{trace_id}-critic",
        )
        base_bayesian = bayesian  # save for delta computation

        # Re-elicit Pass 3 if high-severity findings were found
        if critic_result.re_elicitation_needed:
            if verbose:
                print("  Re-eliciting Pass 3 with critic context...")
            (
                raw_testing,
                testing,
                critic_discriminator_resolution,
                absence,
                bayesian,
                diagnostic_matrix,
                mechanism_trace,
                critic_mechanism_audit_resolution,
            ) = _run_core_passes(
                extraction, hypothesis_space, partition_audit,
                inference_mode=inference_design.mode,
                model=model, verbose=verbose, pass_label="[Critic re-elicit]",
                trace_id=f"{trace_id}-reelicit",
                prior_specification=prior_specification,
                post_selection_evidence_ids=post_selection_evidence_ids,
                post_selection_reason=post_selection_reason,
                critic_context=critic_result.summary,
                source_scope_context=source_scope_context,
                source_ids=source_opportunity_ids,
                discriminator_audit_model=resolved_prediction_audit_model,
                discriminator_audit_attempts=prediction_audit_attempts,
                mechanism_audit_model=resolved_mechanism_audit_model,
                mechanism_audit_attempts=mechanism_audit_attempts,
                output_dir=output_dir,
            )
            mechanism_audit_resolution = critic_mechanism_audit_resolution
            discriminator_audit_resolution = (
                _combine_discriminator_audit_resolutions(
                    discriminator_audit_resolution,
                    critic_discriminator_resolution,
                )
            )
            _write_discriminator_audit_artifacts(
                output_dir,
                discriminator_audit_resolution,
            )

        # Final synthesis: only re-run if inputs changed via re-elicitation.
        # When re_elicitation_needed=False, testing/bayesian/absence are unchanged
        # so synthesis_base is identical — reuse it to avoid a redundant LLM call.
        if critic_result.re_elicitation_needed:
            if verbose:
                print("Pass 4 (critic): Final synthesis...")
            synthesis = run_synthesize(
                extraction, hypothesis_space, testing, bayesian, absence, diagnostic_matrix,
                partition_audit,
                mechanism_trace,
                model=model, trace_id=f"{trace_id}-critic-synth",
                source_scope_context=source_scope_context,
            )
            if verbose:
                print(f"  Narrative: {len(synthesis.analytical_narrative)} chars")
        else:
            if verbose:
                print("Pass 4 (critic): Reusing base synthesis (no re-elicitation).")
            synthesis = synthesis_base

        # Compute and write critic delta
        if output_dir:
            deltas = _compute_critic_delta(base_bayesian, bayesian, critic_result)
            delta_path = os.path.join(output_dir, "critic_delta.json")
            with open(delta_path, "w", encoding="utf-8") as f:
                json.dump([d.model_dump() for d in deltas], f, indent=2)
            if verbose:
                n_moved = sum(1 for d in deltas if abs(d.delta) > 0.001)
                print(f"  Critic delta: {delta_path} ({n_moved}/{len(deltas)} hypotheses moved)")

        # result.json (the canonical output written at the bottom) IS the post-critic result.
        # result_critic.json would be identical — skip it. The ablation pair is:
        #   result_base.json  (pre-critic) vs  result.json  (post-critic).

    else:
        # Standard flow: no critic
        (
            raw_testing,
            testing,
            discriminator_audit_resolution,
            absence,
            bayesian,
            synthesis,
            diagnostic_matrix,
            mechanism_trace,
            mechanism_audit_resolution,
        ) = _run_passes_3_plus(
            extraction, hypothesis_space, partition_audit, text,
            inference_mode=inference_design.mode,
            model=model, verbose=verbose, trace_id=trace_id,
            prior_specification=prior_specification,
            post_selection_evidence_ids=post_selection_evidence_ids,
            post_selection_reason=post_selection_reason,
            source_scope_context=source_scope_context,
            source_ids=source_opportunity_ids,
            discriminator_audit_model=resolved_prediction_audit_model,
            discriminator_audit_attempts=prediction_audit_attempts,
            mechanism_audit_model=resolved_mechanism_audit_model,
            mechanism_audit_attempts=mechanism_audit_attempts,
            output_dir=output_dir,
        )
    refinement_result = None
    refinement_status: RefinementStatus = "not_requested"
    is_refined = False

    if refine:
        if verbose:
            print("\nPass 5: Analytical refinement (second reading)...")
        refinement_result = run_refine(
            text,
            extraction,
            hypothesis_space,
            bayesian,
            absence,
            synthesis,
            model=model,
            repair_model=grounding_repair_model,
            source_packet_ids=source_packet_ids,
            trace_id=trace_id,
        )
        if verbose:
            n_new = len(refinement_result.new_evidence)
            n_reint = len(refinement_result.reinterpreted_evidence)
            n_spur = len(refinement_result.spurious_extractions)
            n_refine = len(refinement_result.hypothesis_refinements)
            print(f"  {n_new} new evidence, {n_reint} reinterpretations, "
                  f"{n_spur} removals, {n_refine} hypothesis refinements")

        # Write refinement.json audit file before applying
        if output_dir:
            ref_path = os.path.join(output_dir, "refinement.json")
            with open(ref_path, "w", encoding="utf-8") as f:
                json.dump(refinement_result.model_dump(), f, indent=2)
            if verbose:
                print(f"  Refinement audit: {ref_path}")

        # Optional review of refinement delta
        if review:
            refinement_result = _default_refine_review(refinement_result, output_dir)

        if not refinement_result.has_material_changes():
            refinement_status = "no_changes"
            if verbose:
                print(
                    "No material refinement changes; preserving the existing "
                    "testing, update, absence, and synthesis artifacts."
                )
        else:
            refinement_status = "applied"
            is_refined = True
            inference_status = "exploratory_post_selection"
            if verbose:
                print("Applying refinement delta...")
            extraction, hypothesis_space = apply_refinement(
                extraction, hypothesis_space, refinement_result, verbose=verbose,
            )
            post_selection_evidence_ids = [item.id for item in extraction.evidence]

            hypotheses_changed = any(
                item.refinement_type != "merge_suggestion"
                for item in refinement_result.hypothesis_refinements
            )
            if hypotheses_changed:
                if verbose:
                    print("Re-auditing the refined hypothesis partition...")
                hypothesis_space, partition_audit, refined_resolution = _resolve_partition(
                    extraction,
                    hypothesis_space,
                    generation_view=hypothesis_generation_view,
                    model=model,
                    repair_model=partition_repair_model,
                    trace_id=f"{trace_id}-refined",
                    output_dir=output_dir,
                    verbose=verbose,
                    partition_review=partition_review,
                    partition_review_fn=partition_review_fn,
                    repair_attempts=partition_repair_attempts,
                    initial_action="refinement_reaudit",
                )
                partition_resolution = _combine_partition_resolutions(
                    partition_resolution,
                    refined_resolution,
                )
                _write_partition_artifacts(output_dir, partition_resolution)

            prior_specification = _resolve_prior_specification(
                extraction,
                hypothesis_space,
                prior_specification,
            )

            if verbose:
                print("\nRe-running passes 3-4 with refined data...")
            (
                raw_testing,
                testing,
                refined_discriminator_resolution,
                absence,
                bayesian,
                synthesis,
                diagnostic_matrix,
                mechanism_trace,
                mechanism_audit_resolution,
            ) = _run_passes_3_plus(
                extraction, hypothesis_space, partition_audit, text,
                inference_mode=inference_design.mode,
                model=model, verbose=verbose,
                pass_label="[Refined]",
                trace_id=trace_id,
                prior_specification=prior_specification,
                post_selection_evidence_ids=post_selection_evidence_ids,
                post_selection_reason=post_selection_reason,
                source_scope_context=source_scope_context,
                source_ids=source_opportunity_ids,
                discriminator_audit_model=resolved_prediction_audit_model,
                discriminator_audit_attempts=prediction_audit_attempts,
                mechanism_audit_model=resolved_mechanism_audit_model,
                mechanism_audit_attempts=mechanism_audit_attempts,
                output_dir=output_dir,
            )
            discriminator_audit_resolution = (
                _combine_discriminator_audit_resolutions(
                    discriminator_audit_resolution,
                    refined_discriminator_resolution,
                )
            )
            _write_discriminator_audit_artifacts(
                output_dir,
                discriminator_audit_resolution,
            )

    if source_packet is not None:
        source_coverage = build_source_coverage(source_packet, text, extraction)
        if verbose:
            print(
                "Source coverage: "
                f"{source_coverage.sources_with_evidence}/{source_coverage.source_count} "
                "packet sources represented in extracted evidence"
            )

    if hypothesis_generation_view is None:
        raise ValueError("pipeline completed without hypothesis-generation exposure")
    added_ids, removed_ids = refinement_evidence_delta(refinement_result)
    require_generation_view_integrity(
        extraction,
        inference_design,
        hypothesis_generation_view,
        added_evidence_ids=added_ids,
        removed_evidence_ids=removed_ids,
    )

    elapsed = time.time() - t0
    if verbose:
        print(f"\nPipeline complete in {elapsed:.1f}s")

    central_claim_review_result: CentralClaimEntailmentReview | None = None
    if central_claim_review:
        if mechanism_trace is None:
            raise ValueError("pipeline completed without a mechanism trace for central-claim review")
        if verbose:
            print("Pass 5.1: Reviewing central final claims against source evidence...")
        central_claim_review_result = run_central_claim_review(
            extraction,
            mechanism_trace,
            synthesis,
            hypothesis_space=hypothesis_space,
            absence=absence,
            model=model,
            trace_id=f"{trace_id or uuid4().hex[:8]}-central-claim-review",
            output_dir=output_dir,
            testing=testing,
            bayesian=bayesian,
            diagnostic_matrix=diagnostic_matrix,
            discriminator_audit_resolution=discriminator_audit_resolution,
            workers=central_claim_review_workers,
        )
        if output_dir is not None:
            with open(
                os.path.join(output_dir, "central_claim_review.json"),
                "w",
                encoding="utf-8",
            ) as handle:
                json.dump(central_claim_review_result.model_dump(mode="json"), handle, indent=2)
    result = ProcessTracingResult(
        llm_client_runtime=llm_client_runtime,
        llm_timeout_seconds=llm_timeout,
        source_text_sha256=source_text_sha256,
        segmented_source=segmented_source_summary,
        extraction=extraction,
        hypothesis_space=hypothesis_space,
        inference_design=inference_design,
        hypothesis_generation_view=hypothesis_generation_view,
        inference_status=inference_status,
        post_selection_evidence_ids=post_selection_evidence_ids,
        prior_specification=prior_specification,
        partition_audit=partition_audit,
        partition_resolution=partition_resolution,
        discriminator_audit_resolution=discriminator_audit_resolution,
        diagnostic_matrix=diagnostic_matrix,
        testing=raw_testing,
        effective_testing=testing,
        mechanism_trace=mechanism_trace,
        mechanism_audit_resolution=mechanism_audit_resolution,
        absence=absence,
        bayesian=bayesian,
        synthesis=synthesis,
        central_claim_review=central_claim_review_result,
        source_packet=source_packet_summary,
        source_coverage=source_coverage,
        refinement=refinement_result,
        is_refined=is_refined,
        refinement_status=refinement_status,
        critic=critic_result,
    )
    if (
        central_claim_review_result is not None
        and central_claim_review_result.status != "accepted"
    ):
        if output_dir is not None:
            with open(
                os.path.join(output_dir, "result_blocked_prepublication.json"),
                "w",
                encoding="utf-8",
            ) as handle:
                json.dump(result.model_dump(mode="json"), handle, indent=2)
        raise ValueError(
            "central claim review blocked publication: "
            + central_claim_review_result.overall_assessment
        )
    return result
