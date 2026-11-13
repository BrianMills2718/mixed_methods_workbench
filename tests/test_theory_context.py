"""Pinned KGAS example context: custody and computation, never scholarly validation."""
import hashlib
import json
import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from mixed_methods_workbench.study_workbench import build_study_payload
from mixed_methods_workbench.theory_context import SalienceInputs, build_theory_context
from scripts.build_study_page import build, render

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/theory/kgas_stakeholder'


@pytest.mark.req("kgas-theory-context/review-a-preserved-artifact", existing=True)
def test_real_source_and_refs():
    p = build_study_payload(EXAMPLE)
    t = p['theory_context']
    assert t['reference']['sha256'] == hashlib.sha256((EXAMPLE / 'stakeholder_theory_v10.json').read_bytes()).hexdigest()
    assert len(t['constructs']) == 13
    raw = json.loads((EXAMPLE / 'stakeholder_theory_v10.json').read_text())
    for ref in t['source_refs']:
        value = raw
        for part in ref['pointer'].split('/')[1:]:
            value = value[int(part)] if isinstance(value, list) else value[part]
        assert value == ref['value']
    assert t['scholarly_anchors'] == []
    assert len(t['operations']) == 7
    assert sum(o['status'] == 'executed_example_rule' for o in t['operations']) == 1
    assert t['producer_claims']['test_coverage'] == .85
    assert t['calculation']['origin'] == 'analyst_supplied'
    assert 'qualitative_strand' not in p
    assert b'/*STUDY_PAYLOAD*/' not in render(EXAMPLE)[0]


@pytest.mark.parametrize('field,value', [('legitimacy', float('nan')), ('urgency', float('inf')), ('power', -0.1), ('power', 1.1), ('power', True), ('power', '0.4')])
@pytest.mark.req("kgas-theory-context/refuse-invalid-numeric-inputs", existing=True)
def test_input_controls(field, value):
    with pytest.raises(ValidationError):
        SalienceInputs.model_validate({'legitimacy': .8, 'urgency': .6, 'power': .4} | {field:value})


@pytest.mark.req("kgas-theory-context/calculate-a-supplied-example", existing=True)
def test_calculation_is_analyst_input_not_observation(tmp_path):
    shutil.copytree(EXAMPLE, tmp_path / 'context')
    d = tmp_path / 'context'
    config = json.loads((d / 'theory_context.json').read_text())
    config['analyst_inputs'] = {'legitimacy': .8, 'urgency': .6, 'power': .4}
    (d / 'theory_context.json').write_text(json.dumps(config))
    t = build_theory_context(d)['theory_context']
    assert t['calculation']['result'] == pytest.approx((.8*.6*.4)**(1/3))
    assert t['calculation']['origin'] == 'analyst_supplied'
    assert t['operations'][4]['status'] == 'executed_example_rule'
    assert t['calculation']['input_sha256']


@pytest.mark.parametrize('mutation', ['hash', 'escape', 'major'])
@pytest.mark.req("kgas-theory-context/refuse-incompatible-or-corrupted-input", existing=True)
def test_failed_pins_and_schema(tmp_path, mutation):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config = json.loads((d / 'theory_context.json').read_text())
    config.pop('source_review', None)
    if mutation == 'hash': config['artifact']['sha256'] = '0'*64
    if mutation == 'escape': config['artifact']['file'] = '../outside.json'
    if mutation == 'major':
        source = d / config['artifact']['file']
        raw = json.loads(source.read_text()); raw['version'] = '2.0.0'
        source.write_text(json.dumps(raw)); config['artifact']['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    (d / 'theory_context.json').write_text(json.dumps(config))
    expected = {'hash': 'theory artifact sha256 mismatch',
                'escape': 'theory artifact path escapes context directory',
                'major': 'unsupported KGAS theory major version'}
    with pytest.raises(ValueError, match=expected[mutation]):
        build_theory_context(d)


@pytest.mark.req("kgas-theory-context/display-unverified-operationalization", existing=True)
def test_no_inputs_means_unexecuted(tmp_path):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config = json.loads((d / 'theory_context.json').read_text())
    config.pop('analyst_inputs')
    (d / 'theory_context.json').write_text(json.dumps(config))
    t = build_theory_context(d)['theory_context']
    assert t['calculation'] is None
    assert t['operations'][4]['status'] == 'available_unexecuted'

@pytest.mark.parametrize('mutation', ['missing_rule', 'duplicate', 'collection', 'formula', 'missing_description'])
@pytest.mark.req("kgas-theory-context/refuse-incompatible-or-corrupted-input", existing=True)
def test_rule_and_collection_controls(tmp_path, mutation):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config = json.loads((d / 'theory_context.json').read_text())
    config.pop('source_review', None)
    source = d / config['artifact']['file']
    raw = json.loads(source.read_text())
    steps = raw['execution']['analysis_steps']
    if mutation == 'missing_rule':
        raw['execution']['analysis_steps'] = [s for s in steps if s['step_id'] != 'calculate_salience']
    elif mutation == 'duplicate':
        steps.append(steps[4])
    elif mutation == 'missing_description':
        del raw['ontology']['entities'][0]['description']
    elif mutation == 'formula':
        steps[4]['custom_script']['implementation_hint'] = 'arbitrary code'
    else:
        raw['ontology']['entities'] = 'invalid'
    source.write_text(json.dumps(raw))
    config['artifact']['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    (d / 'theory_context.json').write_text(json.dumps(config))
    expected = {
        'missing_rule': 'analyst inputs require a declared supported salience rule',
        'duplicate': 'duplicate KGAS operation identifiers',
        'collection': 'Input should be a valid list',
        'formula': 'unsupported salience formula',
        'missing_description': r'ontology\.entities\.0\.description',
    }
    with pytest.raises(ValueError, match=expected[mutation]):
        build_theory_context(d)


@pytest.mark.req("kgas-theory-context/build-the-review", existing=True)
def test_real_build_receipt_records_calculation_and_outputs(tmp_path):
    page, receipt_path = build(EXAMPLE, out_dir=tmp_path)
    receipt = json.loads(receipt_path.read_text())
    calculation, = receipt['calculations']
    assert calculation['inputs'] == {'legitimacy': .8, 'urgency': .6, 'power': .4}
    assert calculation['result'] == pytest.approx((.8*.6*.4)**(1/3))
    assert calculation['formula_source_ref']['pointer'] == '/execution/analysis_steps/4/custom_script/implementation_hint'
    assert calculation['input_sha256'] == hashlib.sha256(json.dumps(calculation['inputs'], sort_keys=True).encode()).hexdigest()
    assert receipt['source_appraisal']['kgas_result'] == receipt['source_appraisal']['kgas_comparator_result'] == 0
    assert receipt['source_appraisal']['counterexample']['source_id'] == 'maw1997'
    assert receipt['source_appraisal']['counterexample']['pages'] == [874, 876]
    assert receipt['outputs'][0]['sha256'] == hashlib.sha256(page.read_bytes()).hexdigest()
    assert receipt['outputs'][1]['sha256'] == hashlib.sha256((tmp_path / 'payload.json').read_bytes()).hexdigest()


@pytest.mark.req("kgas-theory-context/refuse-invalid-numeric-inputs", existing=True)
def test_zero_inputs_and_missing_score(tmp_path):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config = json.loads((d / 'theory_context.json').read_text())
    config['analyst_inputs'] = {'legitimacy': 0, 'urgency': 0, 'power': 0}
    (d / 'theory_context.json').write_text(json.dumps(config))
    assert build_theory_context(d)['theory_context']['calculation']['result'] == 0
    with pytest.raises(ValidationError):
        SalienceInputs.model_validate({'legitimacy': .8, 'urgency': .6})


@pytest.mark.req('kgas-source-appraisal/display-a-source-comparison')
@pytest.mark.req('kgas-source-appraisal/inspect-a-logical-counterexample')
def test_attached_appraisal_and_counterexample():
    t = build_theory_context(EXAMPLE)['theory_context']
    assert t['source_review']['artifact_sha256'] == t['reference']['sha256']
    assert len(t['source_review']['claims']) >= 5
    assert t['source_review_reference']['sha256'] == hashlib.sha256((EXAMPLE / 'scholarly_review.json').read_bytes()).hexdigest()
    assert t['counterexample_result'] == t['comparator_result'] == 0
    assert t['calculation']['inputs'] == {'legitimacy': .8, 'urgency': .6, 'power': .4}


@pytest.mark.parametrize('mutation', ['digest', 'target', 'pointer', 'value', 'source', 'page', 'empty_pages', 'escape'])
@pytest.mark.req('kgas-source-appraisal/refuse-a-broken-review-binding')
def test_appraisal_fail_closed(tmp_path, mutation):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config_path = d / 'theory_context.json'
    config = json.loads(config_path.read_text())
    path = d / config['source_review']['file']
    review = json.loads(path.read_text())
    if mutation == 'target': review['artifact_sha256'] = '0'*64
    if mutation == 'pointer': review['claims'][0]['artifact_pointer'] = '/missing'
    if mutation == 'value': review['claims'][0]['artifact_value'] = 'wrong'
    if mutation == 'source': review['claims'][0]['source_id'] = 'missing'
    if mutation == 'page': review['counterexample']['pages'] = [999]
    if mutation == 'empty_pages': review['claims'][0]['pages'] = []
    path.write_text(json.dumps(review))
    config['source_review']['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    if mutation == 'digest': config['source_review']['sha256'] = '0'*64
    if mutation == 'escape': config['source_review']['file'] = '../outside.json'
    config_path.write_text(json.dumps(config))
    with pytest.raises(ValueError): build_theory_context(d)


@pytest.mark.req('kgas-source-appraisal/preserve-unreviewed-context')
def test_no_review_compatibility(tmp_path):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config = json.loads((d / 'theory_context.json').read_text())
    config.pop('source_review')
    (d / 'theory_context.json').write_text(json.dumps(config))
    t = build_theory_context(d)['theory_context']
    assert t['source_review'] is None
    assert t['counterexample_result'] is None
    assert 'Artifact-only' in t['limits'][0]


@pytest.mark.req('kgas-source-appraisal/display-a-source-comparison')
def test_review_script_escaping(tmp_path):
    d = tmp_path / 'context'
    shutil.copytree(EXAMPLE, d)
    config_path = d / 'theory_context.json'
    config = json.loads(config_path.read_text())
    path = d / config['source_review']['file']
    review = json.loads(path.read_text())
    review['claims'][0]['rationale'] = '</script><script>alert(1)</script>'
    path.write_text(json.dumps(review))
    config['source_review']['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    config_path.write_text(json.dumps(config))
    page, _, _ = render(d)
    assert b'</script><script>alert(1)</script>' not in page
    assert b'<\\/script><script>alert(1)<\\/script>' in page
