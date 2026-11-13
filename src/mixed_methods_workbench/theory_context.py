"""Read the preserved KGAS example without claiming scholarly validation.

Implements: kgas-theory-context/preserve-pinned-theory-context,
    kgas-theory-context/preserve-epistemic-limits,
    kgas-theory-context/calculate-the-declared-rule-with-explicit-inputs,
    kgas-source-appraisal/bind-an-attributable-source-appraisal,
    kgas-source-appraisal/preserve-the-distinction-between-review-and-validation

Requirement text (generated):
    kgas-theory-context/preserve-pinned-theory-context: The consumer SHALL validate the captured
        KGAS artifact's digest and supported major version, retain original fields, confine file
        reads to the declared input root, and expose exact artifact references for the consumed
        constructs and procedures.
    kgas-theory-context/preserve-epistemic-limits: The review SHALL distinguish artifact provenance
        from scholarly verification, theory context from empirical evidence, required observations
        from observed results, and declared operations from implemented operations.
    kgas-theory-context/calculate-the-declared-rule-with-explicit-inputs: The consumer SHALL
        calculate the declared geometric mean only from explicit finite inputs in the interval zero
        to one, retain the inputs and rule reference, and distinguish the arithmetic result from
        measured attributes or validated theory.
    kgas-source-appraisal/bind-an-attributable-source-appraisal: The consumer SHALL accept an
        optional versioned appraisal as a separate record, verify its digest and target artifact
        digest, and resolve each addressed artifact pointer to the recorded value. Claims SHALL
        retain reviewer attribution, disposition, source identity and printed-page references.
    kgas-source-appraisal/preserve-the-distinction-between-review-and-validation: The review SHALL
        distinguish an attributable comparison with one scholarly source from empirical theory
        validation. The original KGAS rule and artifact SHALL remain available with their historical
        identity. Any comparison inputs SHALL be labelled illustrative rather than observed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
from datetime import date


class TheoryArtifactReference(BaseModel):
    model_config = ConfigDict(extra='forbid')
    schema_version: Literal['1.0']
    repository: str
    revision: str = Field(pattern=r'^[0-9a-f]{40}$')
    source_path: str
    file: str
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


class KGASProperty(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str
    description: str


class KGASConstruct(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str
    description: str
    properties: list[KGASProperty] = []


class KGASOntology(BaseModel):
    model_config = ConfigDict(extra='allow')
    entities: list[KGASConstruct]
    relationships: list[KGASConstruct]


class KGASOperation(BaseModel):
    model_config = ConfigDict(extra='allow')
    step_id: str
    method: str
    inputs: list[str]


class KGASExecution(BaseModel):
    model_config = ConfigDict(extra='allow')
    analysis_steps: list[KGASOperation]


class KGASTheoryView(BaseModel):
    model_config = ConfigDict(extra='allow')
    version: str
    theory_id: str
    theory_name: str
    ontology: KGASOntology
    execution: KGASExecution
    validation: dict[str, Any]
    metadata: dict[str, Any]


Score = Annotated[float, Field(strict=True, ge=0, le=1, allow_inf_nan=False)]


class SalienceInputs(BaseModel):
    model_config = ConfigDict(extra='forbid')
    legitimacy: Score
    urgency: Score
    power: Score


class SourceReviewReference(BaseModel):
    model_config = ConfigDict(extra='forbid')
    file: str
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


class ScholarlySource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: HttpUrl
    doi: str = Field(min_length=1)
    printed_pages: list[Annotated[int, Field(strict=True, gt=0)]] = Field(min_length=1)


class SourceAppraisalClaim(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(min_length=1)
    artifact_pointer: str
    artifact_value: Any
    disposition: Literal['supported', 'qualified', 'contradicted', 'not_established']
    rationale: str = Field(min_length=1)
    source_id: str
    pages: list[Annotated[int, Field(strict=True, gt=0)]] = Field(min_length=1)


class SourceCounterexample(BaseModel):
    model_config = ConfigDict(extra='forbid')
    inputs: SalienceInputs
    comparator_inputs: SalienceInputs | None = None
    source_id: str
    pages: list[Annotated[int, Field(strict=True, gt=0)]] = Field(min_length=1)
    source_statement: str = Field(min_length=1)


class TheorySourceReview(BaseModel):
    model_config = ConfigDict(extra='forbid')
    schema_version: Literal['1.0']
    record_type: Literal['theory_source_review']
    artifact_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    reviewed_at: str
    reviewer: str = Field(min_length=1)
    sources: list[ScholarlySource] = Field(min_length=1)
    claims: list[SourceAppraisalClaim] = Field(min_length=1)
    counterexample: SourceCounterexample

    @field_validator('reviewed_at')
    @classmethod
    def valid_date(cls, value: str) -> str:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError('reviewed_at must be YYYY-MM-DD')
        return value


def _pointer_value(raw: Any, pointer: str) -> Any:
    if pointer == '':
        return raw
    if not pointer.startswith('/'):
        raise ValueError('artifact pointer must be a JSON Pointer')
    try:
        for part in pointer.split('/')[1:]:
            key = part.replace('~1', '/').replace('~0', '~')
            if isinstance(raw, list):
                if not key.isascii() or not key.isdigit() or (len(key) > 1 and key[0] == '0'):
                    raise ValueError('invalid array pointer')
                raw = raw[int(key)]
            else:
                raw = raw[key]
        return raw
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('artifact pointer does not exist') from exc


def _geometric_mean(inputs: SalienceInputs) -> float:
    return float((inputs.legitimacy * inputs.urgency * inputs.power) ** (1/3))


class TheoryContextDefinition(BaseModel):
    model_config = ConfigDict(extra='forbid')
    schema_version: Literal['1.0']
    record_type: Literal['theory_context_definition']
    study_id: str
    title: str
    artifact: TheoryArtifactReference
    analyst_inputs: SalienceInputs | None = None
    source_review: SourceReviewReference | None = None


class ArtifactSourceRef(BaseModel):
    model_config = ConfigDict(extra='forbid')
    pointer: str
    value: Any
    scope: Literal['artifact_only'] = 'artifact_only'


class TheoryConstruct(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    kind: Literal['entities', 'relationships', 'property']
    source_ref: ArtifactSourceRef


class TheoryOperation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    method: str
    status: Literal['available_unexecuted', 'unavailable_unexecuted', 'executed_example_rule']
    reason: str
    source_ref: ArtifactSourceRef


class TheoryCalculation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    origin: Literal['analyst_supplied']
    input_basis: str
    inputs: SalienceInputs
    input_sha256: str
    result: float
    formula_source_ref: ArtifactSourceRef
    claim_limit: str


class TheoryContext(BaseModel):
    model_config = ConfigDict(extra='forbid')
    reference: TheoryArtifactReference
    name: str
    constructs: list[TheoryConstruct]
    source_refs: list[ArtifactSourceRef]
    scholarly_anchors: list[ArtifactSourceRef]
    required_observations: list[ArtifactSourceRef]
    assumptions_and_examples: list[ArtifactSourceRef]
    producer_claims: dict[str, Any]
    operations: list[TheoryOperation]
    calculation: TheoryCalculation | None
    limits: list[str]
    producer_artifact: KGASTheoryView
    source_review_reference: SourceReviewReference | None = None
    source_review: TheorySourceReview | None = None
    counterexample_result: float | None = None
    comparator_result: float | None = None


def build_theory_context(directory: Path) -> dict[str, Any]:
    definition = TheoryContextDefinition.model_validate_json(
        (directory / 'theory_context.json').read_bytes())
    pin = definition.artifact
    path = (directory / pin.file).resolve()
    if not path.is_relative_to(directory.resolve()):
        raise ValueError('theory artifact path escapes context directory')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != pin.sha256:
        raise ValueError('theory artifact sha256 mismatch')
    raw = json.loads(data)
    review = None
    if definition.source_review is not None:
        review_path = (directory / definition.source_review.file).resolve()
        if not review_path.is_relative_to(directory.resolve()):
            raise ValueError('source review path escapes context directory')
        review_bytes = review_path.read_bytes()
        if hashlib.sha256(review_bytes).hexdigest() != definition.source_review.sha256:
            raise ValueError('source review sha256 mismatch')
        review = TheorySourceReview.model_validate_json(review_bytes)
        if review.artifact_sha256 != pin.sha256:
            raise ValueError('source review artifact sha256 mismatch')
        sources = {item.id: item for item in review.sources}
        if len(sources) != len(review.sources) or len({c.id for c in review.claims}) != len(review.claims):
            raise ValueError('duplicate source review identifiers')
        references: list[SourceAppraisalClaim | SourceCounterexample] = [
            *review.claims, review.counterexample
        ]
        for item in references:
            if item.source_id not in sources or not set(item.pages) <= set(sources[item.source_id].printed_pages):
                raise ValueError('source review references undeclared source or page')
        for claim in review.claims:
            value = _pointer_value(raw, claim.artifact_pointer)
            if json.dumps(value, sort_keys=True) != json.dumps(claim.artifact_value, sort_keys=True):
                raise ValueError('source review artifact value mismatch')
    view = KGASTheoryView.model_validate(raw)
    if view.version.split('.')[0] != '1':
        raise ValueError('unsupported KGAS theory major version')
    refs: list[dict[str, Any]] = []

    def ref(pointer: str) -> dict[str, Any]:
        value: Any = raw
        for part in pointer.split('/')[1:]:
            key = part.replace('~1', '/').replace('~0', '~')
            value = value[int(key)] if isinstance(value, list) else value[key]
        result = ArtifactSourceRef(pointer=pointer, value=value).model_dump()
        refs.append(result)
        return result

    steps = view.execution.analysis_steps
    ids = [step.step_id for step in steps]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate KGAS operation identifiers')
    if definition.analyst_inputs is not None and 'calculate_salience' not in ids:
        raise ValueError('analyst inputs require a declared supported salience rule')
    constructs = []
    for kind in ('entities', 'relationships'):
        for i, item in enumerate(raw['ontology'][kind]):
            pointer = f'/ontology/{kind}/{i}'
            constructs.append({'name': item['name'], 'kind': kind, 'source_ref': ref(pointer)})
            for j, prop in enumerate(item.get('properties', [])):
                constructs.append({'name': prop['name'], 'kind': 'property',
                                   'source_ref': ref(f'{pointer}/properties/{j}')})
    operations = []
    formula_ref = None
    for i, operation in enumerate(raw['execution']['analysis_steps']):
        pointer = f'/execution/analysis_steps/{i}'
        available = operation['step_id'] == 'calculate_salience'
        if available:
            formula_ref = ref(pointer + '/custom_script/implementation_hint')
            if formula_ref['value'] != 'salience = (legitimacy * urgency * power) ^ (1/3)':
                raise ValueError('unsupported salience formula')
        operations.append({'name': operation['step_id'], 'method': operation['method'],
                           'status': 'available_unexecuted' if available else 'unavailable_unexecuted',
                           'reason': 'Local geometric mean only; categories unavailable' if available
                           else 'Declared by artifact; no implementation invoked',
                           'source_ref': ref(pointer)})
    calculation = None
    if definition.analyst_inputs is not None:
        scores = definition.analyst_inputs.model_dump()
        calculation = {'origin': 'analyst_supplied', 'input_basis': 'Illustrative supplied numbers; not observed data', 'inputs': scores,
                       'input_sha256': hashlib.sha256(json.dumps(scores, sort_keys=True).encode()).hexdigest(),
                       'result': _geometric_mean(definition.analyst_inputs),
                       'formula_source_ref': formula_ref,
                       'claim_limit': 'Computation under an unverified example rule; not empirical or theory validation; no category assigned'}
        next(o for o in operations if o['name'] == 'calculate_salience')['status'] = 'executed_example_rule'
    context = {'reference': pin.model_dump(), 'name': view.theory_name, 'constructs': constructs,
               'source_refs': refs, 'scholarly_anchors': [],
               'source_review_reference': definition.source_review.model_dump() if definition.source_review else None,
               'source_review': review.model_dump(mode='json') if review else None,
               'counterexample_result': _geometric_mean(review.counterexample.inputs) if review else None,
               'comparator_result': _geometric_mean(review.counterexample.comparator_inputs) if review and review.counterexample.comparator_inputs else None, 'producer_artifact': view.model_dump(),
               'required_observations': [ref(f'/execution/analysis_steps/{i}/inputs') for i in range(len(operations))],
               'assumptions_and_examples': [ref('/validation/operationalization_notes'),
                                           ref('/validation/theory_tests'), ref('/validation/boundary_cases')],
               'producer_claims': view.metadata, 'operations': operations, 'calculation': calculation,
               'limits': [('Original artifact has no scholarly anchors. Attached source appraisal is an attributable authored interpretation, not automatic or empirical theory validation.' if review else 'Artifact-only JSON Pointers: no verified scholarly paper anchors or paper quotes.'),
                          'Pinned origin is recorded; local SHA256 is checked. Upstream history is not revalidated by this build.',
                          'Producer validation_status and test_coverage fields are declarations, not validated evidence.',
                          'Required inputs and illustrative scenarios are not empirical observations.',
                          'No stakeholder identification, score assessment, graph, prediction, causal conclusion or management recommendation is executed.']}
    if review is not None and formula_ref is None:
        raise ValueError('source counterexample requires supported salience rule')
    return {'schema_version': '1.0', 'mode': 'theory_context', 'study_id': definition.study_id,
            'title': definition.title, 'theory_context': TheoryContext.model_validate(context).model_dump(mode='json'),
            'steps': [{'step': 'verify local artifact hash and supported major', 'artifacts': 1},
                      {'step': 'project exact artifact fields', 'constructs': len(constructs), 'operations': len(operations)},
                      {'step': 'verify attached authored source appraisal', 'claims': len(review.claims) if review else 0, 'sha256': definition.source_review.sha256 if definition.source_review else None},
                      {'step': 'compute analyst supplied example rule', 'calculations': int(calculation is not None), 'model_calls': 0}]}
