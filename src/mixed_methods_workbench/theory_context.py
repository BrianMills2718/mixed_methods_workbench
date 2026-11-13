"""Read the preserved KGAS example without claiming scholarly validation.

Implements: kgas-theory-context/Preserve pinned theory context
Implements: kgas-theory-context/Preserve epistemic limits
Implements: kgas-theory-context/Calculate the declared rule with explicit inputs
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


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


class TheoryContextDefinition(BaseModel):
    model_config = ConfigDict(extra='forbid')
    schema_version: Literal['1.0']
    record_type: Literal['theory_context_definition']
    study_id: str
    title: str
    artifact: TheoryArtifactReference
    analyst_inputs: SalienceInputs | None = None


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
                       'result': (scores['legitimacy'] * scores['urgency'] * scores['power']) ** (1/3),
                       'formula_source_ref': formula_ref,
                       'claim_limit': 'Computation under an unverified example rule; not empirical or theory validation; no category assigned'}
        next(o for o in operations if o['name'] == 'calculate_salience')['status'] = 'executed_example_rule'
    context = {'reference': pin.model_dump(), 'name': view.theory_name, 'constructs': constructs,
               'source_refs': refs, 'scholarly_anchors': [], 'producer_artifact': view.model_dump(),
               'required_observations': [ref(f'/execution/analysis_steps/{i}/inputs') for i in range(len(operations))],
               'assumptions_and_examples': [ref('/validation/operationalization_notes'),
                                           ref('/validation/theory_tests'), ref('/validation/boundary_cases')],
               'producer_claims': view.metadata, 'operations': operations, 'calculation': calculation,
               'limits': ['Artifact-only JSON Pointers: no verified scholarly paper anchors or paper quotes.',
                          'Pinned origin is recorded; local SHA256 is checked. Upstream history is not revalidated by this build.',
                          'Producer validation_status and test_coverage fields are declarations, not validated evidence.',
                          'Required inputs and illustrative scenarios are not empirical observations.',
                          'No stakeholder identification, score assessment, graph, prediction, causal conclusion or management recommendation is executed.']}
    return {'schema_version': '1.0', 'mode': 'theory_context', 'study_id': definition.study_id,
            'title': definition.title, 'theory_context': TheoryContext.model_validate(context).model_dump(),
            'steps': [{'step': 'verify local artifact hash and supported major', 'artifacts': 1},
                      {'step': 'project exact artifact fields', 'constructs': len(constructs), 'operations': len(operations)},
                      {'step': 'compute analyst supplied example rule', 'calculations': int(calculation is not None), 'model_calls': 0}]}
