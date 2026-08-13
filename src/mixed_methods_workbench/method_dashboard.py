"""Typed, explainable routing for the METHOD-DASH-C1 review dashboard.

The router is deliberately a transparent planning aid. It does not make a
substantive methodological judgment, execute a method, or assign generic
confidence to candidate paths.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DashboardModel(BaseModel):
    """Reject accidental contract expansion in the local dashboard prototype."""

    model_config = ConfigDict(extra="forbid")


class AnalyticAim(StrEnum):
    """Independent intended claim families; an investigation may select several."""

    DESCRIBE = "describe"
    INTERPRET = "interpret"
    EXPLAIN = "explain"
    PREDICT = "predict"
    INTERVENTION = "intervention"
    DECIDE = "decide"


class StartingPoint(StrEnum):
    """The material or decision from which the investigation currently begins."""

    POLICY_DECISION = "policy_decision"
    LITERATURE = "literature"
    EVIDENCE = "evidence"
    PUBLISHED_THEORY = "published_theory"
    CANDIDATE_EXPLANATION = "candidate_explanation"
    STRUCTURED_DATA = "structured_data"


class ComparisonScope(StrEnum):
    """The principal comparison frame, not an exclusive study classification."""

    UNSURE = "unsure"
    WITHIN_CASE = "within_case"
    CROSS_CASE = "cross_case"
    POPULATION = "population"
    SYSTEM = "system"


class EvidenceKind(StrEnum):
    """Broad evidence forms used only to identify plausible planning paths."""

    PUBLISHED_RESEARCH = "published_research"
    DOCUMENTS = "documents"
    INTERVIEWS = "interviews"
    OBSERVATIONS = "observations"
    BOUNDED_CASE_RECORDS = "bounded_case_records"
    STRUCTURED_DATA = "structured_data"
    RELATIONAL_DATA = "relational_data"
    NO_EVIDENCE_YET = "no_evidence_yet"


class PortfolioStatus(StrEnum):
    """Observed local availability without claiming production readiness."""

    OBSERVED_ENGINE = "observed_engine"
    BOUNDED_EXAMPLE = "bounded_example"
    METHOD_PROFILE_ONLY = "method_profile_only"


class RouteReadiness(StrEnum):
    """Plain planning disposition, not an inferential confidence grade."""

    CANDIDATE = "candidate"
    COMPLEMENT = "complement"
    NEEDS_DESIGN = "needs_design"


class StudyBrief(DashboardModel):
    """Capture enough study intent to construct an explainable route set."""

    question: str = Field(min_length=12, max_length=1200)
    aims: list[AnalyticAim] = Field(min_length=1)
    starting_point: StartingPoint
    scope: ComparisonScope = ComparisonScope.UNSURE
    evidence: list[EvidenceKind] = Field(min_length=1)
    same_evidence_generated_explanation: bool = False

    @model_validator(mode="after")
    def reject_duplicate_selections(self) -> StudyBrief:
        """Keep the requested aims and evidence set inspectable and deterministic."""
        if len(self.aims) != len(set(self.aims)):
            raise ValueError("aims must not contain duplicates")
        if len(self.evidence) != len(set(self.evidence)):
            raise ValueError("evidence must not contain duplicates")
        if EvidenceKind.NO_EVIDENCE_YET in self.evidence and len(self.evidence) > 1:
            raise ValueError("no_evidence_yet cannot be combined with available evidence")
        return self


class WorkflowStage(DashboardModel):
    """Describe one navigable policy-research stage without requiring it."""

    stage_id: str
    order: int = Field(ge=1)
    label: str
    plain_question: str
    purpose: str
    typical_outputs: list[str]
    return_paths: list[str]


class MethodProfile(DashboardModel):
    """Describe a method family well enough for routing and honest review."""

    method_id: str
    label: str
    method_kinds: list[str]
    summary: str
    aims: list[AnalyticAim]
    scopes: list[ComparisonScope]
    evidence: list[EvidenceKind]
    source_of_leverage: str
    can_establish: list[str]
    cannot_establish: list[str]
    requirements: list[str]
    stage_ids: list[str]
    workflow_shape: str
    portfolio_status: PortfolioStatus
    portfolio_note: str


class StudyExample(DashboardModel):
    """Provide one concrete starting brief for dashboard review."""

    example_id: str
    label: str
    description: str
    brief: StudyBrief


class ChoiceOption(DashboardModel):
    """Explain one study-brief choice without requiring methodology knowledge."""

    value: str
    label: str
    description: str
    help_text: str


class ArchitectureStressTest(DashboardModel):
    """Rank one future vertical by architectural learning rather than novelty."""

    rank: int = Field(ge=1)
    stress_test_id: str
    label: str
    why_selected: str
    architecture_boundaries: list[str]
    falsifiable_assumptions: list[str]
    authentic_visible_output: str
    effort: str
    prerequisites: list[str]
    stop_rule: str
    current_recommendation: str


class MethodRoute(DashboardModel):
    """Explain why one method appears and what remains unresolved."""

    method: MethodProfile
    readiness: RouteReadiness
    why_it_appears: list[str]
    missing_requirements: list[str]


class StageProjection(DashboardModel):
    """Project relevant routes onto one optional stage of the study graph."""

    stage: WorkflowStage
    method_ids: list[str]
    relevance: str


class RoutePlan(DashboardModel):
    """Return a bounded study map without selecting a universally best method."""

    brief: StudyBrief
    framing_summary: str
    routes: list[MethodRoute]
    workflow: list[StageProjection]
    missing_design_information: list[str]
    warnings: list[str]
    non_claims: list[str]


class DashboardCatalog(DashboardModel):
    """Expose the complete reviewed content used by the local dashboard."""

    schema_version: str
    artifact_status: str
    aims: list[AnalyticAim]
    starting_points: list[StartingPoint]
    scopes: list[ComparisonScope]
    evidence_kinds: list[EvidenceKind]
    stages: list[WorkflowStage]
    methods: list[MethodProfile]
    examples: list[StudyExample]
    aim_options: list[ChoiceOption]
    starting_point_options: list[ChoiceOption]
    scope_options: list[ChoiceOption]
    evidence_options: list[ChoiceOption]
    architecture_stress_tests: list[ArchitectureStressTest]
    stress_test_selection_criteria: list[str]
    capability_tiers: dict[str, list[str]]
    method_coverage_limits: list[str]


AIM_OPTIONS = (
    ChoiceOption(
        value=AnalyticAim.DESCRIBE,
        label="Describe what is happening",
        description="Identify people, events, patterns, differences, or change.",
        help_text="Example: Which neighborhoods face the most heat exposure, and how has that changed over time?",
    ),
    ChoiceOption(
        value=AnalyticAim.INTERPRET,
        label="Understand what it means to people",
        description="Examine how people experience, understand, frame, or give meaning to something.",
        help_text="Example: What does ‘fair access’ mean to residents, service providers, and officials? This asks about meaning, not what caused an outcome.",
    ),
    ChoiceOption(
        value=AnalyticAim.EXPLAIN,
        label="Explain why or how it happened",
        description="Identify causes, mechanisms, processes, or competing explanations.",
        help_text="Example: Why did a public program fail despite having formal organizational support?",
    ),
    ChoiceOption(
        value=AnalyticAim.PREDICT,
        label="Estimate what may happen next",
        description="Forecast a future or currently unobserved outcome.",
        help_text="Example: Which neighborhoods are most likely to experience dangerous heat next summer? A prediction need not explain why.",
    ),
    ChoiceOption(
        value=AnalyticAim.INTERVENTION,
        label="Estimate what an action would change",
        description="Compare what would happen with an action against a relevant alternative.",
        help_text="Example: How much would cooling centers reduce heat-related illness compared with current policy? This asks about the action’s effect, not only what will happen.",
    ),
    ChoiceOption(
        value=AnalyticAim.DECIDE,
        label="Choose what to do",
        description="Compare feasible options using evidence, goals, values, trade-offs, and constraints.",
        help_text="Example: Which heat-risk strategy should the city adopt given costs, uncertainty, unequal effects, and implementation limits?",
    ),
)


STARTING_POINT_OPTIONS = (
    ChoiceOption(
        value=StartingPoint.POLICY_DECISION,
        label="I need to support a decision or action",
        description="A choice, recommendation, or practical response is organizing the work.",
        help_text="Example: A city must choose a heat-risk strategy. The decision—not a particular dataset or method—is organizing the work.",
    ),
    ChoiceOption(
        value=StartingPoint.LITERATURE,
        label="I want to start by reviewing what is already known",
        description="Finding and synthesizing prior research is the first analytical task.",
        help_text="Choose this when searching, comparing, or synthesizing prior studies could itself answer the question or reveal what should be studied next.",
    ),
    ChoiceOption(
        value=StartingPoint.EVIDENCE,
        label="I want to explore source material without a settled explanation",
        description="Patterns, meanings, or possible explanations need to emerge from the material.",
        help_text="Example: You have interview transcripts and records and want to discover patterns, meanings, or possible explanations from them.",
    ),
    ChoiceOption(
        value=StartingPoint.PUBLISHED_THEORY,
        label="I want to use or examine a published theory",
        description="An established account will guide what you look for or appraise.",
        help_text="Example: You want to use a published theory to decide what to look for in a new case. The theory guides the work but is not evidence by itself.",
    ),
    ChoiceOption(
        value=StartingPoint.CANDIDATE_EXPLANATION,
        label="I want to challenge a possible explanation",
        description="You already have a tentative answer for why or how something happened.",
        help_text="Example: Interviews suggest that administrative burden discouraged disclosure, and you now want to challenge that explanation against alternatives.",
    ),
    ChoiceOption(
        value=StartingPoint.STRUCTURED_DATA,
        label="I want to analyze measured or structured observations",
        description="The work begins from comparable measurements, records, or linked observations.",
        help_text="Example: You have neighborhood temperatures, demographics, service use, and dates in tables or relational data.",
    ),
)


SCOPE_OPTIONS = (
    ChoiceOption(
        value=ComparisonScope.UNSURE,
        label="I am not sure yet",
        description="Show paths that would help clarify the study design.",
        help_text="This is a valid answer. The study map will show which decisions depend on choosing one case, several cases, many observations, or a modeled system.",
    ),
    ChoiceOption(
        value=ComparisonScope.WITHIN_CASE,
        label="One specific case or episode",
        description="Study what happened within one bounded place, project, event, or period.",
        help_text="Example: Reconstruct why one public program failed during a particular implementation episode.",
    ),
    ChoiceOption(
        value=ComparisonScope.CROSS_CASE,
        label="Several cases",
        description="Compare cases to understand similarities, differences, or combinations.",
        help_text="Example: Compare six cities to understand why some implemented a policy successfully and others did not.",
    ),
    ChoiceOption(
        value=ComparisonScope.POPULATION,
        label="Many people, organizations, or observations",
        description="Estimate a pattern, relationship, or effect across a larger group.",
        help_text="Example: Estimate how a policy relates to outcomes across all eligible households, schools, or municipalities.",
    ),
    ChoiceOption(
        value=ComparisonScope.SYSTEM,
        label="A whole system or modeled scenario",
        description="Study interacting parts, possible futures, or policy options as a system.",
        help_text="Example: Compare citywide heat-policy packages under several climate and implementation scenarios.",
    ),
)


EVIDENCE_OPTIONS = (
    ChoiceOption(
        value=EvidenceKind.PUBLISHED_RESEARCH,
        label="Published research",
        description="Journal articles, books, evidence reviews, or research reports.",
        help_text="Select this for sources that report prior research, whether or not you have assembled a formal review corpus yet.",
    ),
    ChoiceOption(
        value=EvidenceKind.DOCUMENTS,
        label="Documents",
        description="Policies, memos, reports, correspondence, media, or archival material.",
        help_text="Example: meeting minutes, implementation guidance, internal memoranda, public reports, or emails.",
    ),
    ChoiceOption(
        value=EvidenceKind.INTERVIEWS,
        label="Interviews or focus groups",
        description="Recorded accounts from participants, experts, officials, or affected people.",
        help_text="These sources can support description, interpretation, and explanation, but what they establish depends on sampling, timing, and the question asked.",
    ),
    ChoiceOption(
        value=EvidenceKind.OBSERVATIONS,
        label="Direct observations",
        description="Field notes or records of behavior, settings, events, or processes.",
        help_text="Example: observations of meetings, service delivery, work routines, or interactions in the field.",
    ),
    ChoiceOption(
        value=EvidenceKind.BOUNDED_CASE_RECORDS,
        label="Records from one specific case",
        description="Time-linked records that can reconstruct what happened in a bounded case.",
        help_text="Example: dated decisions, messages, drafts, logs, and contemporaneous records from one project or event.",
    ),
    ChoiceOption(
        value=EvidenceKind.STRUCTURED_DATA,
        label="Tables or measurements",
        description="Rows, columns, variables, dates, scores, counts, or other measured observations.",
        help_text="Example: survey responses, administrative records, experimental outcomes, indicators, or time series.",
    ),
    ChoiceOption(
        value=EvidenceKind.RELATIONAL_DATA,
        label="Network or relationship data",
        description="Records of connections, interactions, flows, or membership.",
        help_text="Example: who communicated with whom, reposted what, belongs to which group, or supplied which organization.",
    ),
    ChoiceOption(
        value=EvidenceKind.NO_EVIDENCE_YET,
        label="No material yet",
        description="The question exists, but evidence still needs to be found or collected.",
        help_text="The dashboard can still identify possible approaches and the material they would require. Do not select this with another evidence type.",
    ),
)


_AIM_PLAIN = {option.value: option.label.lower() for option in AIM_OPTIONS}
_STARTING_PLAIN = {
    option.value: option.label.removeprefix("I want to ").removeprefix("I need to ")
    for option in STARTING_POINT_OPTIONS
}
_SCOPE_PLAIN = {option.value: option.label.lower() for option in SCOPE_OPTIONS}
_EVIDENCE_PLAIN = {option.value: option.label.lower() for option in EVIDENCE_OPTIONS}


STAGES = (
    WorkflowStage(
        stage_id="frame",
        order=1,
        label="Frame the question and decision",
        plain_question="What do we need to learn or decide—and for whom?",
        purpose="Separate intended claims, decision authority, affected people, scope, and constraints.",
        typical_outputs=["question set", "decision frame", "scope and units", "initial alternatives"],
        return_paths=["reframe after evidence gaps", "split one study into several claim-specific paths"],
    ),
    WorkflowStage(
        stage_id="review",
        order=2,
        label="Orient and synthesize prior knowledge",
        plain_question="What is already known, disputed, missing, or transferable?",
        purpose="Search, select, appraise, and synthesize prior research at a depth suited to the decision.",
        typical_outputs=["review corpus", "evidence map", "synthesis", "research gaps"],
        return_paths=["broaden or narrow the question", "update the search", "commission primary research"],
    ),
    WorkflowStage(
        stage_id="design",
        order=3,
        label="Design the investigation",
        plain_question="Which comparison and evidence could warrant each intended claim?",
        purpose="Choose cases, units, measures, timing, acquisition, exposure controls, and methods.",
        typical_outputs=["study protocol", "case or sample plan", "measurement plan", "evidence request"],
        return_paths=["change method when assumptions fail", "seek a different case or source"],
    ),
    WorkflowStage(
        stage_id="analyze",
        order=4,
        label="Analyze with method-owned rules",
        plain_question="What does each method show within its own warrant?",
        purpose="Execute qualitative, causal, predictive, configurational, relational, or simulation methods without flattening them.",
        typical_outputs=["method-native results", "diagnostics", "uncertainty", "challenge findings"],
        return_paths=["recode or re-estimate", "test rivals", "acquire missing evidence", "revise the model"],
    ),
    WorkflowStage(
        stage_id="integrate",
        order=5,
        label="Integrate without erasing disagreement",
        plain_question="How do the results converge, diverge, qualify, or remain silent?",
        purpose="Connect bounded claims, sources, methods, and alternatives while preserving their distinct meanings.",
        typical_outputs=["joint display", "cross-method links", "bounded synthesis", "unresolved conflicts"],
        return_paths=["return to a method-native result", "add a complementary design"],
    ),
    WorkflowStage(
        stage_id="appraise",
        order=6,
        label="Appraise options and decide",
        plain_question="What should be done given consequences, values, constraints, and uncertainty?",
        purpose="Compare feasible options using evidence, objectives, values, distribution, risk, and implementation realities.",
        typical_outputs=["option appraisal", "trade-offs", "recommendation", "decision record"],
        return_paths=["generate another option", "seek evidence on a decisive uncertainty"],
    ),
    WorkflowStage(
        stage_id="learn",
        order=7,
        label="Implement, monitor, evaluate, and learn",
        plain_question="What happened after action, and what should change next?",
        purpose="Track implementation, outcomes, harms, adaptation, and new questions as reusable evidence.",
        typical_outputs=["monitoring record", "process evaluation", "outcome evaluation", "revised decision"],
        return_paths=["adapt implementation", "reopen the decision", "start a new investigation"],
    ),
)


METHODS = (
    MethodProfile(
        method_id="evidence_synthesis",
        label="Evidence synthesis",
        method_kinds=["investigation workflow", "review design"],
        summary="Systematically find, select, appraise, and synthesize prior research at a depth suited to the question.",
        aims=list(AnalyticAim),
        scopes=list(ComparisonScope),
        evidence=[EvidenceKind.PUBLISHED_RESEARCH],
        source_of_leverage="An explicit review question, reproducible discovery and selection, study-level appraisal, and a synthesis suited to the included evidence.",
        can_establish=["what has been studied", "where findings converge or differ", "important evidence limitations and gaps"],
        cannot_establish=["more than the included designs warrant", "a pooled effect when studies are not commensurable"],
        requirements=["review purpose and type", "eligibility boundaries", "search and appraisal strategy"],
        stage_ids=["frame", "review", "design", "integrate"],
        workflow_shape="staged with iterative search, screening, and synthesis",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general review execution engine has been verified in the workbench.",
    ),
    MethodProfile(
        method_id="thematic_analysis",
        label="Thematic analysis",
        method_kinds=["qualitative analytical method"],
        summary="Develop a reviewed account of patterned meaning across a qualitative corpus.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.INTERPRET],
        scopes=[ComparisonScope.WITHIN_CASE, ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION],
        evidence=[EvidenceKind.DOCUMENTS, EvidenceKind.INTERVIEWS, EvidenceKind.OBSERVATIONS],
        source_of_leverage="Systematic corpus engagement, explicit coding and theme development, reflexivity, and evidence-supported interpretation.",
        can_establish=["patterns of meaning", "variation and exceptions", "an inspectable interpretation of the corpus"],
        cannot_establish=["population prevalence from mentions", "causal effects merely because participants describe causation"],
        requirements=["bounded corpus", "qualitative question", "declared analytic variant and review approach"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="iterative familiarization, coding, theme development, review, and writing",
        portfolio_status=PortfolioStatus.OBSERVED_ENGINE,
        portfolio_note="Qualitative Coding owns implemented coding, evidence, comparison, and review capabilities.",
    ),
    MethodProfile(
        method_id="grounded_theory",
        label="Grounded theory",
        method_kinds=["qualitative methodology", "theory-development workflow"],
        summary="Develop an empirically grounded account through coding, constant comparison, memoing, category development, and targeted evidence seeking.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.INTERPRET, AnalyticAim.EXPLAIN],
        scopes=[ComparisonScope.WITHIN_CASE, ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION],
        evidence=[EvidenceKind.DOCUMENTS, EvidenceKind.INTERVIEWS, EvidenceKind.OBSERVATIONS],
        source_of_leverage="Constant comparison, memoing, iterative category development, variation seeking, and theoretical sampling where the chosen variant requires it.",
        can_establish=["grounded categories and variation", "a bounded explanatory or process account", "evidence gaps for further sampling"],
        cannot_establish=["statistical generalizability", "independent confirmation from the same theory-generating corpus"],
        requirements=["declared grounded-theory variant", "comparison across incidents or cases", "memo and category lineage"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="cyclic evidence, coding, comparison, memoing, category integration, and further sampling",
        portfolio_status=PortfolioStatus.OBSERVED_ENGINE,
        portfolio_note="Qualitative Coding has a fixed-corpus grounded-theory path; fixed-corpus adequacy is not theoretical saturation.",
    ),
    MethodProfile(
        method_id="process_tracing",
        label="Process Tracing",
        method_kinds=["within-case qualitative causal-inference method"],
        summary="Compare rival causal processes for one bounded outcome using theory-linked, temporally ordered, diagnostically appraised evidence.",
        aims=[AnalyticAim.EXPLAIN],
        scopes=[ComparisonScope.WITHIN_CASE],
        evidence=[EvidenceKind.BOUNDED_CASE_RECORDS, EvidenceKind.DOCUMENTS, EvidenceKind.INTERVIEWS, EvidenceKind.OBSERVATIONS],
        source_of_leverage="Observable implications under rival mechanisms, temporal within-case evidence, source appraisal, diagnostic contrasts, and absence tests.",
        can_establish=["which proposed process better explains a bounded outcome", "which mechanism links are observed, challenged, or missing"],
        cannot_establish=["a population average treatment effect", "numerical structural relations across units"],
        requirements=["named bounded case and outcome", "plausible rival explanations", "case-specific records with temporal and diagnostic potential"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="iterative rivals, predictions, source acquisition, diagnostic testing, and qualification",
        portfolio_status=PortfolioStatus.OBSERVED_ENGINE,
        portfolio_note="Process Tracing owns a current method-specific engine and versioned export.",
    ),
    MethodProfile(
        method_id="comparative_case",
        label="Comparative case study",
        method_kinds=["research strategy", "comparative design"],
        summary="Combine intensive within-case analysis with disciplined comparison across strategically selected cases.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.INTERPRET, AnalyticAim.EXPLAIN],
        scopes=[ComparisonScope.CROSS_CASE],
        evidence=[EvidenceKind.DOCUMENTS, EvidenceKind.INTERVIEWS, EvidenceKind.OBSERVATIONS, EvidenceKind.BOUNDED_CASE_RECORDS],
        source_of_leverage="Explicit case selection, comparable questions, deep within-case evidence, and cross-case contrast.",
        can_establish=["how processes and contexts vary across cases", "scope conditions and revised explanations"],
        cannot_establish=["an average population effect without a separate design", "comparability merely from shared labels"],
        requirements=["case universe and selection logic", "comparable constructs or questions", "within-case evidence"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="nested within-case analysis and cross-case comparison with returns to both",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general comparative-case execution path has been verified in the workbench.",
    ),
    MethodProfile(
        method_id="qca",
        label="Qualitative Comparative Analysis",
        method_kinds=["cross-case set-theoretic method"],
        summary="Analyze necessary or sufficient conditions and combinations across a calibrated case population.",
        aims=[AnalyticAim.EXPLAIN, AnalyticAim.INTERVENTION],
        scopes=[ComparisonScope.CROSS_CASE],
        evidence=[EvidenceKind.STRUCTURED_DATA, EvidenceKind.BOUNDED_CASE_RECORDS],
        source_of_leverage="Theoretically justified set calibration, truth-table comparison, minimization, and case-based resolution of contradictions and limited diversity.",
        can_establish=["necessary or sufficient set relations", "configurations associated with an outcome"],
        cannot_establish=["a temporal mechanism inside a case", "an average marginal effect"],
        requirements=["defined case population", "calibrated conditions and outcome", "theory-guided treatment of remainders"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="iterative concepts, calibration, truth table, solutions, robustness, and return to cases",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No current QCA engine or authentic workbench vertical has been verified.",
    ),
    MethodProfile(
        method_id="causal_effects",
        label="Experimental or quasi-experimental causal effects",
        method_kinds=["research design", "causal estimation family"],
        summary="Estimate a defined intervention or exposure effect using random assignment or a defensible observational identification strategy.",
        aims=[AnalyticAim.INTERVENTION],
        scopes=[ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION],
        evidence=[EvidenceKind.STRUCTURED_DATA, EvidenceKind.OBSERVATIONS],
        source_of_leverage="A declared estimand plus random assignment or a design-specific identification strategy and its diagnostics.",
        can_establish=["a bounded causal effect under stated assumptions", "uncertainty around the estimate"],
        cannot_establish=["mechanism from effect estimation alone", "transportability to unstudied settings without additional assumptions"],
        requirements=["treatment, outcome, population, contrast, and period", "assignment or identification design", "suitable outcome data"],
        stage_ids=["design", "analyze", "integrate", "learn"],
        workflow_shape="design, measurement, diagnosis, estimation, falsification or sensitivity, and qualification",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general causal-effect engine is integrated into the workbench.",
    ),
    MethodProfile(
        method_id="causal_models",
        label="Causal diagrams and structural causal models",
        method_kinds=["formal representation", "causal inference framework"],
        summary="Make causal assumptions explicit and determine whether an intervention or counterfactual query is identifiable from a proposed structure and data.",
        aims=[AnalyticAim.EXPLAIN, AnalyticAim.INTERVENTION],
        scopes=[ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION, ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.STRUCTURED_DATA, EvidenceKind.PUBLISHED_RESEARCH, EvidenceKind.OBSERVATIONS],
        source_of_leverage="Explicit causal assumptions plus graphical or structural identification rules and an appropriate design/data relationship.",
        can_establish=["whether a causal query is identified under the model", "adjustment or estimation implications"],
        cannot_establish=["that the assumed graph is true", "an effect from a diagram without appropriate evidence"],
        requirements=["defined causal query", "substantively justified variables and structure", "data suitable for the identified estimand"],
        stage_ids=["frame", "design", "analyze"],
        workflow_shape="iterative domain knowledge, graph, identification, data, diagnosis, and revision",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general causal-modeling engine has been verified in this workbench.",
    ),
    MethodProfile(
        method_id="measurement_sem",
        label="Measurement modeling and SEM",
        method_kinds=["measurement model", "latent-variable statistical model"],
        summary="Operationalize latent constructs and estimate specified measurement and structural relations in a population model.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.EXPLAIN, AnalyticAim.PREDICT],
        scopes=[ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION],
        evidence=[EvidenceKind.STRUCTURED_DATA],
        source_of_leverage="A specified and identified measurement/structural model, observed indicators, and fit, validity, and sensitivity diagnostics.",
        can_establish=["measurement structure under a specified model", "estimated structural relations and model fit"],
        cannot_establish=["causal direction from fit alone", "valid indicators from qualitative code counts alone"],
        requirements=["defined constructs", "designed or justified indicators", "adequate structured observations and model identification"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="iterative construct definition, measurement, estimation, criticism, and transparent revision",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general measurement/SEM workflow has been verified.",
    ),
    MethodProfile(
        method_id="forecasting",
        label="Forecasting and predictive modeling",
        method_kinds=["predictive design", "modeling family"],
        summary="Estimate future or unobserved outcomes under a declared information, horizon, and evaluation regime.",
        aims=[AnalyticAim.PREDICT],
        scopes=[ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION, ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.STRUCTURED_DATA, EvidenceKind.RELATIONAL_DATA],
        source_of_leverage="Time-respecting or external evaluation, meaningful baselines, proper metrics, calibrated uncertainty, and monitoring for shift.",
        can_establish=["out-of-sample predictive performance in the evaluated regime", "forecast probabilities or intervals when calibrated"],
        cannot_establish=["causal explanation from accuracy", "stable performance after unexamined distribution shift"],
        requirements=["target and forecast horizon", "representative training and separated evaluation data", "metric or scoring rule"],
        stage_ids=["design", "analyze", "learn"],
        workflow_shape="cyclic fit, backtest, calibrate, monitor, and update with protected evaluation",
        portfolio_status=PortfolioStatus.BOUNDED_EXAMPLE,
        portfolio_note="Theory Forge has a bounded CPT/Choices13k predictive comparison; no general workbench prediction path is integrated.",
    ),
    MethodProfile(
        method_id="simulation",
        label="Simulation experiment",
        method_kinds=["executable model", "generated-evidence method"],
        summary="Explore system behavior and compare mechanisms, scenarios, or interventions inside an explicit executable model.",
        aims=[AnalyticAim.EXPLAIN, AnalyticAim.PREDICT, AnalyticAim.INTERVENTION, AnalyticAim.DECIDE],
        scopes=[ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.PUBLISHED_RESEARCH, EvidenceKind.STRUCTURED_DATA, EvidenceKind.NO_EVIDENCE_YET],
        source_of_leverage="Explicit assumptions and mechanisms, controlled configuration contrasts, retained repeated runs, verification, and sensitivity analysis.",
        can_establish=["what the specified model produces under alternatives", "vulnerabilities and sensitivities inside the modeled system"],
        cannot_establish=["that simulated effects occur in reality", "mechanism validity from plausible narrative alone"],
        requirements=["system boundary and purpose", "mechanism and assumption specification", "experiment and sensitivity design"],
        stage_ids=["design", "analyze", "appraise", "learn"],
        workflow_shape="iterative author, verify, calibrate or justify, experiment, compare, and revise",
        portfolio_status=PortfolioStatus.OBSERVED_ENGINE,
        portfolio_note="Cybernetic Influence retains simulation capabilities while Concordia is the adopted future outer foundation; workbench integration is absent.",
    ),
    MethodProfile(
        method_id="policy_appraisal",
        label="Policy appraisal and decision analysis",
        method_kinds=["decision-oriented workflow"],
        summary="Compare feasible options using evidence, objectives, values, constraints, distributional consequences, uncertainty, and implementation realities.",
        aims=[AnalyticAim.DECIDE],
        scopes=list(ComparisonScope),
        evidence=list(EvidenceKind),
        source_of_leverage="Explicit decision frame, feasible options, consequence evidence, accountable criteria and values, trade-off analysis, and decision authority.",
        can_establish=["which option is preferred under declared objectives and assumptions", "where trade-offs and decisive uncertainties lie"],
        cannot_establish=["a uniquely correct recommendation without normative inputs", "empirical facts merely by scoring options"],
        requirements=["named decision maker or authority", "feasible alternatives", "objectives, criteria, values, constraints, and consequence evidence"],
        stage_ids=["frame", "review", "design", "integrate", "appraise", "learn"],
        workflow_shape="branching and cyclic problem, evidence, options, appraisal, decision, implementation, and evaluation",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No integrated options-to-decision workbench vertical has been verified.",
    ),
    MethodProfile(
        method_id="robust_decision",
        label="Robust Decision Making",
        method_kinds=["decision making under deep uncertainty"],
        summary="Use many plausible futures to discover vulnerabilities and compare strategies that remain acceptable rather than optimizing one forecast.",
        aims=[AnalyticAim.PREDICT, AnalyticAim.INTERVENTION, AnalyticAim.DECIDE],
        scopes=[ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.PUBLISHED_RESEARCH, EvidenceKind.STRUCTURED_DATA, EvidenceKind.NO_EVIDENCE_YET],
        source_of_leverage="Large ensembles as case generators, vulnerability discovery, scenario comparison, iterative strategy design, and trade-off analysis.",
        can_establish=["where candidate strategies fail across represented futures", "which strategies are robust under declared criteria"],
        cannot_establish=["which future is most probable", "that the uncertainty space is complete"],
        requirements=["decision frame and candidate strategies", "uncertainty dimensions and outcome criteria", "model or scenario generator"],
        stage_ids=["frame", "design", "analyze", "appraise", "learn"],
        workflow_shape="iterative strategies, futures, vulnerability discovery, trade-offs, adaptation, and monitoring",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No RDM execution path is integrated into the workbench.",
    ),
    MethodProfile(
        method_id="network_analysis",
        label="Network analysis",
        method_kinds=["relational representation", "analytical-method family"],
        summary="Describe or model relational structure, positions, communities, diffusion, and network change under explicit boundary and tie rules.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.EXPLAIN, AnalyticAim.PREDICT],
        scopes=[ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION, ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.RELATIONAL_DATA],
        source_of_leverage="Explicit entity, relation, and boundary construction plus suitable network measures, models, comparisons, and missingness sensitivity.",
        can_establish=["relational structure and positions", "network patterns or model results under the specified construction"],
        cannot_establish=["causal influence from connectivity alone", "a natural network boundary without a boundary rule"],
        requirements=["node and tie semantics", "network boundary and time", "missingness and comparison strategy"],
        stage_ids=["design", "analyze", "integrate"],
        workflow_shape="iterative data construction, representation, analysis, sensitivity, and interpretation",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general network-analysis engine is integrated into the workbench.",
    ),
    MethodProfile(
        method_id="program_evaluation",
        label="Program and implementation evaluation",
        method_kinds=["evaluation workflow", "design family"],
        summary="Assess implementation, processes, outcomes, impacts, value, or learning needs using designs matched to the evaluation question.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.INTERPRET, AnalyticAim.EXPLAIN, AnalyticAim.INTERVENTION, AnalyticAim.DECIDE],
        scopes=[ComparisonScope.WITHIN_CASE, ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION, ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.DOCUMENTS, EvidenceKind.INTERVIEWS, EvidenceKind.OBSERVATIONS, EvidenceKind.BOUNDED_CASE_RECORDS, EvidenceKind.STRUCTURED_DATA],
        source_of_leverage="A program theory and question-specific design linking implementation, outcomes, comparisons, context, and intended use.",
        can_establish=["implementation fidelity and variation", "outcomes or impacts when the chosen design warrants them", "actionable lessons for adaptation"],
        cannot_establish=["causal impact from an outcome trend without identification", "value for money without costs and a comparison"],
        requirements=["program theory or logic", "evaluation purpose and users", "question-specific indicators, cases, comparison, and timing"],
        stage_ids=["frame", "review", "design", "analyze", "integrate", "appraise", "learn"],
        workflow_shape="formative and summative loops across design, implementation, monitoring, evaluation, and adaptation",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="No general program-evaluation workflow is integrated into the workbench.",
    ),
    MethodProfile(
        method_id="legal_institutional",
        label="Legal and institutional analysis",
        method_kinds=["interpretive domain analysis", "policy constraint analysis"],
        summary="Interpret laws, authorities, institutional rules, responsibilities, and implementation constraints that shape the feasible option set.",
        aims=[AnalyticAim.DESCRIBE, AnalyticAim.INTERPRET, AnalyticAim.EXPLAIN, AnalyticAim.DECIDE],
        scopes=[ComparisonScope.WITHIN_CASE, ComparisonScope.CROSS_CASE, ComparisonScope.POPULATION, ComparisonScope.SYSTEM],
        evidence=[EvidenceKind.PUBLISHED_RESEARCH, EvidenceKind.DOCUMENTS, EvidenceKind.BOUNDED_CASE_RECORDS],
        source_of_leverage="Authoritative texts, jurisdiction and temporal validity, disciplined interpretation, institutional comparison, and domain-expert review.",
        can_establish=["applicable authorities and institutional constraints", "differences across jurisdictions or organizational arrangements"],
        cannot_establish=["legal advice from an automated profile", "empirical consequences without additional analysis"],
        requirements=["jurisdiction and effective period", "authoritative source hierarchy", "qualified interpretation and review"],
        stage_ids=["frame", "review", "design", "integrate", "appraise"],
        workflow_shape="iterative question, authority retrieval, interpretation, comparison, application, and review",
        portfolio_status=PortfolioStatus.METHOD_PROFILE_ONLY,
        portfolio_note="This profile remains shallow; no legal/institutional engine is integrated.",
    ),
)


EXAMPLES = (
    StudyExample(
        example_id="city_heat_policy",
        label="Choose a city heat-risk strategy",
        description="A multi-aim policy study spanning existing evidence, unequal exposure, future conditions, interventions, and trade-offs.",
        brief=StudyBrief(
            question="Which package of heat-risk interventions should a city adopt, given unequal neighborhood exposure, uncertain future temperatures, implementation constraints, and competing stakeholder priorities?",
            aims=[AnalyticAim.DESCRIBE, AnalyticAim.PREDICT, AnalyticAim.INTERVENTION, AnalyticAim.DECIDE],
            starting_point=StartingPoint.POLICY_DECISION,
            scope=ComparisonScope.SYSTEM,
            evidence=[EvidenceKind.PUBLISHED_RESEARCH, EvidenceKind.STRUCTURED_DATA, EvidenceKind.RELATIONAL_DATA],
        ),
    ),
    StudyExample(
        example_id="program_failure",
        label="Explain one program failure",
        description="A bounded within-case explanation requiring rivals and contemporaneous records.",
        brief=StudyBrief(
            question="Why did one public program fail during a specific implementation episode despite formal organizational support?",
            aims=[AnalyticAim.DESCRIBE, AnalyticAim.EXPLAIN],
            starting_point=StartingPoint.CANDIDATE_EXPLANATION,
            scope=ComparisonScope.WITHIN_CASE,
            evidence=[EvidenceKind.BOUNDED_CASE_RECORDS, EvidenceKind.DOCUMENTS, EvidenceKind.INTERVIEWS],
        ),
    ),
    StudyExample(
        example_id="remote_work_review",
        label="Map evidence on remote-work policy",
        description="A literature-first investigation that may stop at synthesis or motivate a later primary study.",
        brief=StudyBrief(
            question="What is already known about remote-work policies, for whom, in which settings, and with what evidence limitations?",
            aims=[AnalyticAim.DESCRIBE, AnalyticAim.INTERPRET],
            starting_point=StartingPoint.LITERATURE,
            scope=ComparisonScope.POPULATION,
            evidence=[EvidenceKind.PUBLISHED_RESEARCH],
        ),
    ),
)


ARCHITECTURE_STRESS_TESTS = (
    ArchitectureStressTest(
        rank=1,
        stress_test_id="policy_options_to_decision",
        label="Policy options to a reviewable decision",
        why_selected="It exercises the largest uncovered part of the Evidence-to-Action promise: empirical claims must combine with objectives, values, constraints, distribution, implementation, and uncertainty without becoming one generic score.",
        architecture_boundaries=[
            "evidence synthesis to decision framing",
            "method-native findings to consequence estimates",
            "empirical uncertainty versus normative value judgment",
            "options, trade-offs, recommendation, and monitoring lineage",
        ],
        falsifiable_assumptions=[
            "A thin bounded-claim and derivation seam can connect empirical results to an appraisal without standardizing their internal uncertainty.",
            "Decision criteria and value judgments can remain explicit enough that a reviewer can identify what changed the recommendation.",
            "The workflow can return for missing evidence or revised options without requiring one universal pipeline state machine.",
        ],
        authentic_visible_output="A named policy choice with at least three feasible options, source-linked consequence claims, explicit criteria and affected groups, uncertainty and trade-off views, a reviewable recommendation, and a monitoring/evaluation return path.",
        effort="medium-high: one bounded policy case, evidence packet, appraisal operator, and review UI; no new general method engine required if existing evidence is adequate",
        prerequisites=[
            "a consequential but reversible policy case with decision authority and affected parties",
            "at least one empirical result or credible evidence synthesis",
            "reviewed objectives, criteria, constraints, and feasible options",
        ],
        stop_rule="Stop or redesign if the vertical can only rank invented options, hides values inside weights, or needs a universal evidence/confidence model to proceed.",
        current_recommendation="Recommended next architecture stress test after this dashboard review because it reaches the missing action boundary and pressures both method modularity and product value.",
    ),
    ArchitectureStressTest(
        rank=2,
        stress_test_id="review_to_new_primary_study",
        label="Evidence synthesis to a new primary-study design",
        why_selected="It tests the common think-tank starting path that the current Open Science example does not cover: prior literature becomes a structured gap, then a claim-specific primary research design.",
        architecture_boundaries=[
            "search and screening provenance",
            "study-level appraisal and synthesis",
            "evidence gap to question and design",
            "published evidence identity versus newly collected evidence",
        ],
        falsifiable_assumptions=[
            "A review result can become a design input through typed claims and gaps without converting studies into one universal evidence object.",
            "The router can distinguish a review that is the final study from one that justifies new evidence acquisition.",
            "Eligibility and appraisal semantics can remain owned by the review profile while later methods consume bounded outputs.",
        ],
        authentic_visible_output="A reproducible small review or evidence map whose strongest actionable gap becomes a reviewed protocol for one named primary study, with every transition inspectable.",
        effort="medium: requires a bounded literature corpus and one downstream protocol; broad review automation is unnecessary",
        prerequisites=[
            "a tightly scoped policy or research question",
            "searchable source universe and review type",
            "an identified actor willing to judge whether the gap warrants new research",
        ],
        stop_rule="Stop if the selected question cannot distinguish a genuine evidence gap from a search failure or if the proposed primary study is not changed by the synthesis.",
        current_recommendation="Strong second stress test, especially if a real policy decision case is not yet available.",
    ),
    ArchitectureStressTest(
        rank=3,
        stress_test_id="qual_to_measurement",
        label="Qualitative construct to held-out measurement",
        why_selected="It tests whether interpreted qualitative concepts can inform a quantitative instrument without turning code counts into measurements or flattening reviewed meaning.",
        architecture_boundaries=[
            "qualitative category to construct definition",
            "construct to indicator and annotation specification",
            "discovery/evaluation exposure separation",
            "qualitative and quantitative results to joint display",
        ],
        falsifiable_assumptions=[
            "A purpose-specific operationalization can preserve the qualitative construct's scope and counterexamples.",
            "A held-out measurement stage can add information not already encoded by the discovery corpus.",
            "Convergence and divergence can be represented without one cross-method confidence score.",
        ],
        authentic_visible_output="One reviewed qualitative construct becomes a measurement specification, is applied to held-out text, and returns a joint display of distribution, representative passages, errors, divergence, and bounded meta-inference.",
        effort="high: needs a suitable construct, held-out text, annotation or measurement work, quantitative analysis, and dual-method review",
        prerequisites=[
            "a stable reviewed construct with explicit scope and negative cases",
            "held-out text from an appropriate target population",
            "a feasible transparent instrument and reviewer",
        ],
        stop_rule="Stop if the construct cannot be operationalized without semantic loss, the held-out set is exposed, or the numeric result merely recounts the original coding.",
        current_recommendation="High-value genuine mixed-method test, but not the cheapest next move.",
    ),
    ArchitectureStressTest(
        rank=4,
        stress_test_id="empirical_to_simulation",
        label="Empirical explanation to controlled simulation",
        why_selected="It challenges the boundary between observed evidence and generated evidence while testing theory-to-mechanism transformation, configuration identity, and intervention comparison.",
        architecture_boundaries=[
            "empirical claims to model assumptions",
            "theory or mechanism to executable transitions",
            "observed versus simulated evidence",
            "matched-run comparison and sensitivity lineage",
        ],
        falsifiable_assumptions=[
            "Model assumptions can be traced to evidence or explicit judgment without claiming empirical confirmation.",
            "A method-neutral retained evidence bundle can support several theory projections while the simulator owns transitions.",
            "Scenario comparisons can return model-bounded findings without becoming real-world effect estimates.",
        ],
        authentic_visible_output="A source-grounded scenario with explicit assumptions and mechanisms, retained matched runs under one intervention contrast, sensitivity results, and a clear separation between empirical basis and generated model behavior.",
        effort="high: the general Concordia-first simulation foundation and parity boundary remain active elsewhere",
        prerequisites=[
            "a stable simulator execution seam",
            "a bounded empirical mechanism or policy scenario",
            "reviewed mapping from empirical claims to model assumptions and interventions",
        ],
        stop_rule="Stop before integration if general simulator parity is unavailable, or if the scenario cannot expose which empirical facts and judgments produced its mechanisms.",
        current_recommendation="Defer until the adopted Concordia foundation can support the authentic vertical without duplicate simulation infrastructure.",
    ),
    ArchitectureStressTest(
        rank=5,
        stress_test_id="prediction_to_monitoring",
        label="Prediction to monitored decision use",
        why_selected="Prediction is a major analytical aim, but a useful stress test must include target/horizon, protected evaluation, calibration, decision use, and monitoring rather than merely display a model comparison.",
        architecture_boundaries=[
            "features and derivations to forecast",
            "training versus held-out exposure",
            "predictive uncertainty versus causal or decision claims",
            "forecast to action threshold and monitoring feedback",
        ],
        falsifiable_assumptions=[
            "The common exposure and derivation mechanics are sufficient to preserve a leakage-safe predictive path.",
            "Predictive uncertainty can remain method-owned while a decision layer consumes explicit probabilities or intervals.",
            "Monitoring can return drift and errors as new evidence without overwriting historical results.",
        ],
        authentic_visible_output="A named forecast with horizon, benchmark, protected evaluation, calibration/error view, explicit action use, and one monitoring update that preserves the original prediction revision.",
        effort="medium-high: a bounded CPT/Choices13k comparison exists, but a real recurring forecast and user decision do not",
        prerequisites=[
            "a recurring prediction target with meaningful action or review",
            "time-respecting or external evaluation data",
            "baseline, scoring rule, and monitoring owner",
        ],
        stop_rule="Stop if the candidate is only an offline model comparison, has no protected evaluation, or no actor would change a decision based on the output.",
        current_recommendation="Retain as a candidate, not the default next stage; select it when a real recurring forecast decision is available.",
    ),
)


_TEXT_EVIDENCE = {
    EvidenceKind.DOCUMENTS,
    EvidenceKind.INTERVIEWS,
    EvidenceKind.OBSERVATIONS,
    EvidenceKind.BOUNDED_CASE_RECORDS,
}


def _requirements_for(method: MethodProfile, brief: StudyBrief) -> list[str]:
    """Return visible missing prerequisites rather than silently inventing them."""
    missing: list[str] = []
    evidence = set(brief.evidence)
    if method.method_id == "evidence_synthesis" and EvidenceKind.PUBLISHED_RESEARCH not in evidence:
        missing.append("Define and retrieve a reviewable published-research corpus.")
    if method.method_id == "process_tracing":
        if brief.scope != ComparisonScope.WITHIN_CASE:
            missing.append("Select one named bounded case and outcome.")
        if EvidenceKind.BOUNDED_CASE_RECORDS not in evidence:
            missing.append("Acquire case-specific records with temporal and diagnostic potential.")
    if method.method_id in {"comparative_case", "qca"} and brief.scope != ComparisonScope.CROSS_CASE:
        missing.append("Define a cross-case population and selection logic.")
    if method.method_id == "qca" and EvidenceKind.STRUCTURED_DATA not in evidence:
        missing.append("Calibrate case conditions and outcomes as sets.")
    if method.method_id in {"causal_effects", "measurement_sem", "forecasting"} and EvidenceKind.STRUCTURED_DATA not in evidence:
        missing.append("Obtain structured observations suitable for this design.")
    if method.method_id == "network_analysis" and EvidenceKind.RELATIONAL_DATA not in evidence:
        missing.append("Define and obtain relational entities, ties, boundaries, and time.")
    if method.method_id in {"simulation", "robust_decision"} and brief.scope != ComparisonScope.SYSTEM:
        missing.append("Define a system boundary, mechanisms, and scenario space.")
    if method.method_id in {"policy_appraisal", "robust_decision"} and AnalyticAim.DECIDE in brief.aims:
        missing.append("Name the decision authority, feasible options, objectives, criteria, and constraints.")
    if method.method_id == "legal_institutional":
        missing.append("Name the jurisdiction, effective period, and authoritative source hierarchy.")
    if brief.scope == ComparisonScope.UNSURE and method.method_id not in {"evidence_synthesis", "policy_appraisal"}:
        missing.append("Clarify whether the claim concerns one case, several cases, a population, or a modeled system.")
    return missing


def _candidate_reason(method: MethodProfile, brief: StudyBrief) -> list[str]:
    """Explain overlap using ordinary language and no opaque score."""
    reasons: list[str] = []
    matched_aims = [_AIM_PLAIN[aim] for aim in brief.aims if aim in method.aims]
    if matched_aims:
        reasons.append(f"Helps you {', '.join(matched_aims)}.")
    if brief.scope in method.scopes:
        reasons.append(f"Can be used when studying {_SCOPE_PLAIN[brief.scope]}.")
    matched_evidence = [_EVIDENCE_PLAIN[kind] for kind in brief.evidence if kind in method.evidence]
    if matched_evidence:
        reasons.append(f"Can use material you already have: {', '.join(matched_evidence)}.")
    if method.method_id == "evidence_synthesis" and brief.starting_point in {
        StartingPoint.LITERATURE,
        StartingPoint.POLICY_DECISION,
        StartingPoint.PUBLISHED_THEORY,
    }:
        reasons.append("Reviewing what is already known is useful in your current situation.")
    if method.method_id == "policy_appraisal" and brief.starting_point == StartingPoint.POLICY_DECISION:
        reasons.append("Your work needs to support a decision, not only analyze evidence.")
    if method.method_id == "grounded_theory" and brief.starting_point == StartingPoint.EVIDENCE:
        reasons.append("You can develop concepts and possible explanations from the source material through comparison.")
    if method.method_id == "process_tracing" and brief.starting_point in {
        StartingPoint.CANDIDATE_EXPLANATION,
        StartingPoint.PUBLISHED_THEORY,
    }:
        reasons.append("A prior explanation can be translated into rival processes and observable implications.")
    return reasons


def _include_method(method: MethodProfile, brief: StudyBrief) -> bool:
    """Select plausible routes conservatively while retaining useful complements."""
    aims = set(brief.aims)
    evidence = set(brief.evidence)
    if method.method_id == "evidence_synthesis":
        return brief.starting_point in {
            StartingPoint.LITERATURE,
            StartingPoint.POLICY_DECISION,
            StartingPoint.PUBLISHED_THEORY,
        } or EvidenceKind.PUBLISHED_RESEARCH in evidence
    if method.method_id == "policy_appraisal":
        return AnalyticAim.DECIDE in aims or brief.starting_point == StartingPoint.POLICY_DECISION
    if method.method_id == "program_evaluation":
        return bool(aims & {AnalyticAim.INTERVENTION, AnalyticAim.DECIDE})
    if method.method_id == "legal_institutional":
        return brief.starting_point == StartingPoint.POLICY_DECISION and AnalyticAim.DECIDE in aims
    if not aims.intersection(method.aims):
        return False
    if method.method_id in {"thematic_analysis", "grounded_theory"}:
        return bool(evidence & _TEXT_EVIDENCE) or brief.starting_point == StartingPoint.EVIDENCE
    if method.method_id == "process_tracing":
        return AnalyticAim.EXPLAIN in aims and brief.scope in {
            ComparisonScope.WITHIN_CASE,
            ComparisonScope.UNSURE,
        }
    if method.method_id in {"comparative_case", "qca"}:
        return brief.scope in {ComparisonScope.CROSS_CASE, ComparisonScope.UNSURE}
    if method.method_id == "causal_effects":
        return AnalyticAim.INTERVENTION in aims and brief.scope in {
            ComparisonScope.CROSS_CASE,
            ComparisonScope.POPULATION,
            ComparisonScope.UNSURE,
        }
    if method.method_id == "causal_models":
        return bool(aims & {AnalyticAim.EXPLAIN, AnalyticAim.INTERVENTION})
    if method.method_id == "measurement_sem":
        return EvidenceKind.STRUCTURED_DATA in evidence and bool(
            aims & {AnalyticAim.DESCRIBE, AnalyticAim.EXPLAIN, AnalyticAim.PREDICT}
        )
    if method.method_id == "forecasting":
        return AnalyticAim.PREDICT in aims
    if method.method_id in {"simulation", "robust_decision"}:
        return brief.scope in {ComparisonScope.SYSTEM, ComparisonScope.UNSURE} and bool(
            aims & set(method.aims)
        )
    if method.method_id == "network_analysis":
        return EvidenceKind.RELATIONAL_DATA in evidence
    return True


def _route_priority(route: MethodRoute, brief: StudyBrief) -> tuple[int, int, str]:
    """Order routes for readability without exposing a pseudo-scientific score."""
    direct_aims = len(set(route.method.aims) & set(brief.aims))
    readiness_order = {
        RouteReadiness.CANDIDATE: 0,
        RouteReadiness.COMPLEMENT: 1,
        RouteReadiness.NEEDS_DESIGN: 2,
    }
    return (readiness_order[route.readiness], -direct_aims, route.method.label)


def route_study(brief: StudyBrief) -> RoutePlan:
    """Construct a transparent multi-method study map from a reviewed brief."""
    routes: list[MethodRoute] = []
    for method in METHODS:
        if not _include_method(method, brief):
            continue
        missing = _requirements_for(method, brief)
        if missing:
            readiness = RouteReadiness.NEEDS_DESIGN
        elif method.method_id in {"evidence_synthesis", "legal_institutional", "causal_models"}:
            readiness = RouteReadiness.COMPLEMENT
        else:
            readiness = RouteReadiness.CANDIDATE
        routes.append(
            MethodRoute(
                method=method,
                readiness=readiness,
                why_it_appears=_candidate_reason(method, brief),
                missing_requirements=missing,
            )
        )
    routes.sort(key=lambda route: _route_priority(route, brief))

    missing_design: list[str] = []
    if brief.scope == ComparisonScope.UNSURE:
        missing_design.append("Clarify whether you will study one case, compare several cases, analyze many observations, or model a system.")
    if EvidenceKind.NO_EVIDENCE_YET in brief.evidence:
        missing_design.append("Design an evidence-acquisition strategy before treating any route as executable.")
    if AnalyticAim.INTERVENTION in brief.aims:
        missing_design.append("Define the intervention or exposure, comparator, outcome, population/system, and time period.")
    if AnalyticAim.PREDICT in brief.aims:
        missing_design.append("Define the prediction target, horizon, evaluation split, baseline, and error or scoring rule.")
    if AnalyticAim.DECIDE in brief.aims:
        missing_design.append("Name the decision authority, affected parties, feasible alternatives, objectives, values, constraints, and timing.")

    warnings = [
        "Candidate paths are planning aids. Method selection still requires substantive and domain review."
    ]
    if brief.same_evidence_generated_explanation:
        warnings.append(
            "The same evidence helped generate the explanation. Continue for exploratory appraisal, but label the exposure and do not present the result as independent confirmation."
        )

    selected_ids = {route.method.method_id for route in routes}
    stage_lookup = {stage.stage_id: stage for stage in STAGES}
    stage_methods: dict[str, list[str]] = {stage.stage_id: [] for stage in STAGES}
    for route in routes:
        for stage_id in route.method.stage_ids:
            stage_methods[stage_id].append(route.method.method_id)

    workflow: list[StageProjection] = []
    for stage in STAGES:
        method_ids = stage_methods[stage.stage_id]
        if method_ids or stage.stage_id in {"frame", "design", "integrate"}:
            relevance = (
                f"{len(method_ids)} candidate method path(s) contribute here."
                if method_ids
                else "This coordination stage remains relevant even when no method profile owns it."
            )
            workflow.append(
                StageProjection(
                    stage=stage_lookup[stage.stage_id],
                    method_ids=[method_id for method_id in method_ids if method_id in selected_ids],
                    relevance=relevance,
                )
            )

    aim_words = "; ".join(_AIM_PLAIN[aim] for aim in brief.aims)
    study_scope = (
        "you have not yet decided whether to focus on one case, several cases, many observations, or a system"
        if brief.scope == ComparisonScope.UNSURE
        else f"you plan to study {_SCOPE_PLAIN[brief.scope]}"
    )
    framing_summary = (
        f"You want to {aim_words}. Your starting task is to "
        f"{_STARTING_PLAIN[brief.starting_point]}. {study_scope.capitalize()}."
    )
    return RoutePlan(
        brief=brief,
        framing_summary=framing_summary,
        routes=routes,
        workflow=workflow,
        missing_design_information=list(dict.fromkeys(missing_design)),
        warnings=warnings,
        non_claims=[
            "This map does not choose one universally best method for you.",
            "This map does not perform the research or establish an answer to your question.",
            "Statements about available software describe what has been inspected locally, not what is ready for production use.",
        ],
    )


def dashboard_catalog() -> DashboardCatalog:
    """Return the exact catalog rendered by the browser and available to agents."""
    return DashboardCatalog(
        schema_version="method_dashboard.v2",
        artifact_status="local_review_prototype",
        aims=list(AnalyticAim),
        starting_points=list(StartingPoint),
        scopes=list(ComparisonScope),
        evidence_kinds=list(EvidenceKind),
        stages=list(STAGES),
        methods=list(METHODS),
        examples=list(EXAMPLES),
        aim_options=list(AIM_OPTIONS),
        starting_point_options=list(STARTING_POINT_OPTIONS),
        scope_options=list(SCOPE_OPTIONS),
        evidence_options=list(EVIDENCE_OPTIONS),
        architecture_stress_tests=list(ARCHITECTURE_STRESS_TESTS),
        stress_test_selection_criteria=[
            "Pressure a materially different inferential or decision boundary, not merely another dataset.",
            "Produce a useful researcher-visible result even if no abstraction is promoted.",
            "Use authentic evidence, model execution, or accountable decision inputs at the boundary being tested.",
            "Expose whether candidate shared mechanics survive without flattening method-owned semantics.",
            "Fit a bounded slice whose failure can redirect the architecture before large integration work.",
            "Prefer current producer capabilities and named users over speculative infrastructure.",
        ],
        capability_tiers={
            "thin_shared_mechanics": [
                "artifact and source identity",
                "derivation and configuration",
                "run and method declaration",
                "review events",
                "exposure relations",
                "typed scope references",
                "bounded claim envelopes",
            ],
            "method_parameterized_actions": [
                "question formulation",
                "search and evidence admission",
                "case or sample selection",
                "coding and classification",
                "comparison",
                "measurement",
                "alternative generation",
                "challenge and sensitivity",
                "targeted evidence acquisition",
                "synthesis and presentation",
            ],
            "method_owned_semantics": [
                "grounded-theory category development",
                "Process Tracing diagnosticity",
                "QCA calibration and necessity/sufficiency",
                "causal estimands and identification",
                "SEM measurement and fit",
                "forecast evaluation and calibration",
                "simulation mechanisms and transitions",
                "decision objectives and value judgments",
            ],
        },
        method_coverage_limits=[
            "The 16 profiles are a representative first set, not a complete methodology ontology.",
            "Review variants, evaluation variants, participatory methods, futures, spatial methods, and computational methods need deeper profiles.",
            "The Open Science example covers qualitative-to-explanation work but must not control the general architecture.",
            "A profile can support planning without a corresponding integrated software engine.",
        ],
    )
