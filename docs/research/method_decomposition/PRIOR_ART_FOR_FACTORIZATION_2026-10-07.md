# Prior art for turning the 14 decompositions into a factorization (2026-10-07)

Question: how to compare analytical moves across the 14 Phase 3 method records (`phase3/methods/p01`–`p14`) to find a
small canonical set of reusable operations while method-specific judgement stays method-owned. Background research by an
agent; maintenance of OntoAligner (1.9.4, 2026-09-01), DeclareDesign (1.1.1, 2026-04-28) and SSSOM (0.4.21, 2026-05-23)
checked against PyPI/CRAN. Not verified: exact CommonKADS inference names, DeclareDesign coverage of QCA.

## Adopt
- **Verb list:** CommonKADS inference catalogue (Schreiber et al. 2000; ~18 inference types defined by input/output
  roles and required knowledge), extended for data collection, estimation and identification, which it lacks.
- **Phase alignment frame:** MIDA (Model, Inquiry, Data strategy, Answer strategy; Blair, Coppock and Humphreys 2023,
  DeclareDesign). Fits the estimand-based methods (RCT, DiD, survey, forecasting, process tracing) well; fits Delphi,
  grounded theory and option appraisal poorly.
- **Ownership rule:** ISO/IEC 24744 Task versus Technique (reconfirmed 2026): "test a hypothesis" is a canonical task; a
  process-tracing hoop test or QCA calibration is a method-owned technique.
- **Mapping record:** SSSOM, one row per proposed match with predicate, confidence and justification.
- **Warning list for false merges:** Goertz and Mahoney's two cultures (average effects versus set-theoretic logic);
  Brady and Collier's dataset versus causal-process observations.

## Matching procedure
1. Candidate pairs only within the same MIDA slot, using each move's signature (verb, input and output types,
   information origin, guards) plus text embeddings (OntoAligner's retrieve-then-verify pattern).
2. Two critics from different model families label each pair: same, broader/narrower, or distinct, quoting evidence.
3. A human settles disagreements and seeds a gold set; record agreement.
4. Promote a move to canonical only when it recurs across at least k methods with compatible types; otherwise it stays a
   method-owned technique.

Process Model Matching Contests (2013, 2015): label-only matching recall about 0.26–0.44, so match on inputs and outputs,
not verb names.

## Genuinely novel
The canonical move set for these methods, with information origin, temporal and access guards and the six authority
roles, and the test of whether a factorization holds. None of the sources covers this.

## Sources
CommonKADS: https://www.inf.ed.ac.uk/teaching/courses/kmm/PDF/5-knowledge-model-20110228.pdf ·
ISO/IEC 24744: https://www.iso.org/standard/38854.html · DeclareDesign: https://book.declaredesign.org/library/observational-causal.html ·
OntoAligner: https://arxiv.org/abs/2503.21902v1 · Process model matching: https://link.springer.com/doi/10.1007/978-3-319-45468-9_8 ·
EDAM: https://bioportal.bioontology.org/ontologies/EDAM · TaDiRAH: https://vocabs.dariah.eu/tadirah/en/
