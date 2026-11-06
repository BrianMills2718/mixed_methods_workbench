# Domain glossary: Mixed Methods Workbench

The concepts this repository is about, what each means and where it is defined. The graph is
[domain.graph.json](domain.graph.json). Dashed concepts are not implemented here: producers run in
their own repositories, and meta-inference is named by the method but not computed.

| Concept (node id) | Meaning | Status | Source |
| --- | --- | --- | --- |
| Method engine (producer) (`producer_engine`) | A method repository (qualitative_coding, process_tracing) that runs its own method and owns its strict export schema. | in producer repositories | `AGENTS.md:81` |
| Method export (`producer_export`) | A producer's strict, versioned export (QC, PT or GT-inspired) as the workbench receives it. | implemented | `src/mixed_methods_workbench/models.py:268` |
| Workbench consumer view (`workbench_view`) | The workbench's permissive, compatible reading of a producer export; it fails on an unsupported major version. | implemented | `src/mixed_methods_workbench/models.py:438` |
| Source segment (`source_segment`) | An exact span of a source document that evidence points to. | implemented | `src/mixed_methods_workbench/models.py:98` |
| Cross-method link (`cross_method_link`) | A typed link between objects from two methods' exports. | implemented | `src/mixed_methods_workbench/models.py:505` |
| Review packet (`review_packet`) | What a reviewer reads: the assembled exports, links and claim limits for one demonstration. | implemented | `src/mixed_methods_workbench/models.py:523` |
| Evidence anchor (`evidence_anchor`) | A pointer from a finding to the exact source text that backs it. | implemented | `src/mixed_methods_workbench/investigation_spine.py:127` |
| Publication gate (`publication_gate`) | The rule that withholds a causal conclusion from publication until a researcher has reviewed it. | implemented | `src/mixed_methods_workbench/investigation_spine.py:160` |
| Connected run receipt (`connected_run_receipt`) | The record of one run across producers: inputs, attempts, where it stopped and the trace ids. | implemented | `src/mixed_methods_workbench/investigation_run.py:124` |
| Independent challenge (`verification_challenge`) | A second model's advisory challenge to one finding, with the excerpts it saw. | implemented | `src/mixed_methods_workbench/investigation_verification.py:42` |
| Method profile (`method_profile`) | A method's description for question-first routing on the method dashboard. | implemented | `src/mixed_methods_workbench/method_dashboard.py:118` |
| Route plan (`route_plan`) | The dashboard's suggested route from a study brief to method stages. | implemented | `src/mixed_methods_workbench/method_dashboard.py:190` |
| Method phase (`method_phase`) | Level 1 of the accepted discovery format: a phase of a method. | implemented | `src/mixed_methods_workbench/method_topology.py:62` |
| Analytical move (`analytical_move`) | Level 2: an analytical move inside a phase. | implemented | `src/mixed_methods_workbench/method_topology.py:69` |
| Execution action (`execution_action`) | Level 3: an executable action a move is carried out by. | implemented | `src/mixed_methods_workbench/method_topology.py:86` |
| Method decomposition (`method_decomposition`) | One of the 14 frozen Phase 3 records of a method's phases, moves and actions, checked by the validator. | implemented | `scripts/validate_phase3_methods.py:77` |
| STATO term (`stato_term`) | A term of the pinned STATO 2026-04-20 release naming what a statistical step computes. | implemented | `scripts/fetch_stato.py:42` |
| Collision group (`collision_group`) | Steps from different methods grouped by canonical signature, verb, type pair or shared STATO term. | implemented | `scripts/crosswalk_phase4.py:72` |
| Capability verdict (`capability_verdict`) | The section-10 verdict on a collision group: same_capability, shared_shell or different_capability, with its justification. | implemented | `scripts/crosswalk_phase4.py:144` |
| Guarded decision (`guarded_decision`) | A decision request checked against bound artifacts, evidence and policy before it returns an outcome. | implemented | `src/mixed_methods_workbench/guarded_decision/models.py:175` |
| Quantitative audit (`quantitative_audit`) | The NYC bounded quantitative comparison: frozen query, drift replay and predicted-versus-observed audit. | implemented | `src/mixed_methods_workbench/nyc_crz_quantitative.py:193` |
| Meta-inference (`meta_inference`) | A bounded conclusion drawn by intentionally joining qualitative and quantitative strands; planned for version 0.4, not computed. | docs only | `AGENTS.md:104` |

"Method" is ambiguous here: a research method (qualitative coding, process tracing) or a method
decomposition record. The decomposition is always called a decomposition.
