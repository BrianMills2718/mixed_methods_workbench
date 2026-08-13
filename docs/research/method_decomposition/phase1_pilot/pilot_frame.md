# Phase 1 pilot frames

Status: frozen before decomposition

Purpose: stress the rev-5.1 decomposition format across five materially
different methods. These frames are comparison instruments, not canonical
definitions of their method families.

```yaml
frames:
  - method_id: systematic_review
    variant: >-
      Cochrane-style systematic review of randomized intervention-effect
      studies, with pairwise meta-analysis when studies are sufficiently
      comparable.
    use_case: >-
      Does a reminder intervention increase timely enrollment in a public
      benefit among eligible adults compared with usual outreach?
    excluded_variants:
      - scoping review
      - realist review
      - qualitative evidence synthesis
      - network meta-analysis
      - diagnostic-test-accuracy review

  - method_id: grounded_theory
    variant: >-
      Charmaz-style constructivist grounded theory using concurrent data
      collection and analysis, initial and focused coding, constant comparison,
      memo-writing, theoretical sampling, category integration, and an explicit
      adequacy argument.
    use_case: >-
      How do frontline caseworkers adapt when a new benefits-eligibility system
      conflicts with local knowledge and workload constraints?
    excluded_variants:
      - classic Glaserian grounded theory
      - Straussian axial-coding prescription
      - fixed-corpus grounded-theory-inspired analysis with no theoretical sampling
      - generic thematic analysis

  - method_id: process_tracing
    variant: >-
      Theory-testing process tracing in one bounded case, comparing explicit
      rival causal explanations using predicted within-case evidence and
      Bayesian likelihood-ratio reasoning.
    use_case: >-
      Why did one city adopt a congestion-pricing policy after years of failed
      proposals: fiscal pressure, coalition change, or a policy-learning mechanism?
    excluded_variants:
      - theory-building process tracing
      - explaining-outcome process tracing without frozen rivals
      - cross-case comparative analysis
      - mediation analysis using statistical path coefficients

  - method_id: causal_effect_estimation_rct
    variant: >-
      Individually randomized, two-arm, parallel-group superiority trial with a
      prespecified intention-to-treat estimand and primary outcome.
    use_case: >-
      What is the effect of a simplified renewal notice versus the standard
      notice on benefit renewal within 60 days among eligible recipients?
    excluded_variants:
      - cluster-randomized trial
      - adaptive trial
      - non-inferiority or equivalence trial
      - factorial or crossover trial
      - quasi-experimental design
    quasi_experimental_divergence: >-
      A quasi-experimental variant must replace randomized assignment with a
      design-specific identification strategy, such as discontinuity,
      instrument, difference-in-differences, or matching assumptions. That
      change affects the warrant, diagnostics, sensitivity analysis, and
      admissible causal conclusion; it is not a parameter toggle.

  - method_id: policy_option_appraisal
    variant: >-
      HM Treasury Green Book 2026 appraisal: define rationale and objectives,
      generate a longlist, select a shortlist, appraise social costs, benefits,
      risks, uncertainty, and distributional effects, and identify a preferred
      option for decision-maker consideration.
    use_case: >-
      Which heat-risk reduction package should a regional government advance:
      business as usual, cooling centers, home retrofits, or a combined package?
    excluded_variants:
      - ex-post impact evaluation
      - formal legal analysis
      - procurement/business-case approval after appraisal
      - purely deliberative option comparison without social-value appraisal
      - additive MCDA as the sole decision rule

hostile_counterexample:
  method_id: agent_based_policy_simulation
  variant: >-
    Agent-based policy simulation described with ODD, executed as a designed
    computational experiment, and subjected to uncertainty and sensitivity
    analysis.
  use_case: >-
    Under alternative evacuation-warning policies, what model-conditional
    congestion and clearance patterns emerge from heterogeneous household
    decisions and network interactions?
  excluded_variants:
    - system dynamics
    - discrete-event simulation
    - microsimulation without interacting adaptive agents
    - simulation used only for training or visualization
```

The appendix in the external rev-5.1 handoff remained sealed until these frames
and `sources.md` were frozen.
