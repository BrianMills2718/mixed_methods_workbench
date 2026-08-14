"""Pass 2.5: hypothesis partition audit and deterministic decision gate.

Runs after hypothesis generation and before diagnostic testing. Checks each
rival pair for overlap, complementarity, and absorptive risk. The LLM supplies
semantic judgments; deterministic code validates coverage and decides whether
the partition may proceed to numerical testing.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from uuid import uuid4

from llm_client import render_prompt

from pt.llm import call_llm
from pt.schemas import HypothesisSpace, PartitionAudit

PROMPTS_DIR = Path(__file__).parent / "prompts"


class PartitionBlockedError(ValueError):
    """Raised when a hypothesis partition cannot enter diagnostic testing."""

    def __init__(self, audit: PartitionAudit):
        self.audit = audit
        detail = "; ".join(audit.decision_blockers) or audit.summary
        super().__init__(f"Hypothesis partition blocked before Pass 3: {detail}")


def partition_blockers(
    hypothesis_space: HypothesisSpace,
    audit: PartitionAudit,
) -> list[str]:
    """Derive fail-loud partition blockers from the typed semantic audit."""
    hypothesis_ids = [hypothesis.id for hypothesis in hypothesis_space.hypotheses]
    known_ids = set(hypothesis_ids)
    prediction_owner = {
        prediction.id: hypothesis.id
        for hypothesis in hypothesis_space.hypotheses
        for prediction in hypothesis.observable_predictions
    }
    blockers: list[str] = []

    if len(hypothesis_ids) < 2:
        blockers.append("comparative testing requires at least two declared hypotheses")
    if not audit.research_question_adequate:
        blockers.append("research question is not a singular, discriminating causal question")

    expected_pairs = {
        frozenset((hypothesis_ids[left], hypothesis_ids[right]))
        for left in range(len(hypothesis_ids))
        for right in range(left + 1, len(hypothesis_ids))
    }
    seen_pairs: set[frozenset[str]] = set()
    duplicate_pairs: set[tuple[str, str]] = set()
    unknown_ids: set[str] = set()
    self_pairs: set[str] = set()

    for pair in audit.rival_pairs:
        pair_ids = (pair.h1_id, pair.h2_id)
        unknown_ids.update(set(pair_ids) - known_ids)
        if pair.h1_id == pair.h2_id:
            self_pairs.add(pair.h1_id)
            continue

        key = frozenset(pair_ids)
        if key in seen_pairs:
            ordered_pair = sorted(pair_ids)
            duplicate_pairs.add((ordered_pair[0], ordered_pair[1]))
        seen_pairs.add(key)

        contrast_issues: list[str] = []
        contrast_keys: set[tuple[str, str]] = set()
        valid_contrast_count = 0
        for contrast in pair.prediction_contrasts:
            contrast_key = (
                contrast.h1_prediction_id,
                contrast.h2_prediction_id,
            )
            if contrast_key in contrast_keys:
                contrast_issues.append(
                    "duplicate prediction contrast "
                    f"{contrast.h1_prediction_id}<->{contrast.h2_prediction_id}"
                )
                continue
            contrast_keys.add(contrast_key)
            h1_owner = prediction_owner.get(contrast.h1_prediction_id)
            h2_owner = prediction_owner.get(contrast.h2_prediction_id)
            if h1_owner != pair.h1_id:
                contrast_issues.append(
                    f"prediction {contrast.h1_prediction_id} is owned by "
                    f"{h1_owner or 'no declared hypothesis'}, not {pair.h1_id}"
                )
            if h2_owner != pair.h2_id:
                contrast_issues.append(
                    f"prediction {contrast.h2_prediction_id} is owned by "
                    f"{h2_owner or 'no declared hypothesis'}, not {pair.h2_id}"
                )
            if h1_owner == pair.h1_id and h2_owner == pair.h2_id:
                valid_contrast_count += 1
        pair.discriminator_count = valid_contrast_count
        if contrast_issues:
            blockers.append(
                f"pair {pair.h1_id}<->{pair.h2_id}: invalid prediction contrast(s): "
                + "; ".join(contrast_issues)
            )

        concerns: list[str] = []
        if pair.discriminator_count < 1:
            if pair.overlap_concern:
                concerns.append("overlap")
            if pair.complementary_concern:
                concerns.append("complementarity")
            if pair.absorptive_concern:
                concerns.append("absorption")
            concerns.append("no valid concrete prediction contrast")
        if concerns:
            blockers.append(
                f"pair {pair.h1_id}<->{pair.h2_id}: {', '.join(concerns)}"
            )

    if unknown_ids:
        blockers.append(f"rival pairs reference unknown hypothesis ids: {sorted(unknown_ids)}")
    if self_pairs:
        blockers.append(f"self-referential rival pairs are invalid: {sorted(self_pairs)}")
    if duplicate_pairs:
        blockers.append(f"duplicate rival pairs: {sorted(duplicate_pairs)}")

    missing_pairs = expected_pairs - seen_pairs
    if missing_pairs:
        formatted = sorted("<->".join(sorted(pair)) for pair in missing_pairs)
        blockers.append(f"missing rival pairs: {formatted}")

    unknown_flagged = set(audit.hypotheses_flagged) - known_ids
    if unknown_flagged:
        blockers.append(f"audit flags unknown hypothesis ids: {sorted(unknown_flagged)}")
    nondiscriminating_ids = {
        hypothesis_id
        for pair in audit.rival_pairs
        if pair.discriminator_count < 1
        for hypothesis_id in (pair.h1_id, pair.h2_id)
    }
    flagged = sorted(
        set(audit.hypotheses_flagged) & known_ids & nondiscriminating_ids
    )
    if flagged:
        blockers.append(f"hypotheses require split, merge, or reframing: {flagged}")

    return blockers


def partition_warnings(audit: PartitionAudit) -> list[str]:
    """Report semantic risks that do not erase an operational discriminator."""
    warnings_: list[str] = []
    for pair in audit.rival_pairs:
        if pair.discriminator_count < 1:
            continue
        concerns: list[str] = []
        if pair.overlap_concern:
            concerns.append("overlap")
        if pair.complementary_concern:
            concerns.append("complementarity")
        if pair.absorptive_concern:
            concerns.append("absorption")
        if concerns:
            warnings_.append(
                f"pair {pair.h1_id}<->{pair.h2_id}: "
                f"{', '.join(concerns)} remains advisory because "
                f"{pair.discriminator_count} valid opposed prediction contrast(s) exist"
            )
    flagged = sorted(set(audit.hypotheses_flagged))
    if flagged and not any(
        pair.discriminator_count < 1
        and ({pair.h1_id, pair.h2_id} & set(flagged))
        for pair in audit.rival_pairs
    ):
        warnings_.append(
            "model flagged hypotheses despite complete pairwise discrimination: "
            f"{flagged}"
        )
    return warnings_


def require_adequate_partition(
    hypothesis_space: HypothesisSpace,
    audit: PartitionAudit,
) -> None:
    """Raise before Pass 3 unless the partition satisfies the decision contract."""
    blockers = partition_blockers(hypothesis_space, audit)
    audit.decision_blockers = blockers
    audit.decision_warnings = partition_warnings(audit)
    audit.overall_quality = "needs_review" if blockers else "adequate"
    audit.cap_applied = bool(blockers)
    if blockers:
        raise PartitionBlockedError(audit)


def run_partition(
    hypothesis_space: HypothesisSpace,
    *,
    model: str | None = None,
    trace_id: str | None = None,
) -> PartitionAudit:
    """Evaluate hypothesis partition quality before Pass 3.

    Produces semantic pair judgments, then deterministically derives the
    decision verdict and blockers. Call ``require_adequate_partition`` at the
    orchestration boundary before invoking Pass 3.
    """
    if trace_id is None:
        trace_id = uuid4().hex[:8]

    messages = render_prompt(
        PROMPTS_DIR / "pass_partition.yaml",
        hypothesis_space_json=json.dumps(hypothesis_space.model_dump(), indent=2),
    )

    kwargs: dict = {"model": model} if model else {}
    audit = call_llm(
        messages[0]["content"],
        PartitionAudit,
        task="process_tracing.partition",
        trace_id=trace_id,
        **kwargs,
    )

    blockers = partition_blockers(hypothesis_space, audit)
    audit.decision_blockers = blockers
    audit.decision_warnings = partition_warnings(audit)
    audit.overall_quality = "needs_review" if blockers else "adequate"
    audit.cap_applied = bool(blockers)
    if blockers:
        warnings.warn(
            "Hypothesis partition is blocked before diagnostic testing. "
            f"Blockers: {'; '.join(blockers)}. Summary: {audit.summary}",
            UserWarning,
            stacklevel=2,
        )

    return audit
