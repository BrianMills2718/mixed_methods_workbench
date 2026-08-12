# METHOD-DASH-C1: Question-First Methodology Dashboard

Status: implemented local prototype; stakeholder review pending

Authorized: Brian's 2026-08-12 approval to deepen the think-tank methodology
spine and work toward a dashboard that can become a product entry point and a
review/test surface.

## Visible outcome

A researcher can open one local dashboard, describe an analytical need, select
one or more intended aims, record their starting point, scope, and available
evidence, and receive a reviewable set of possible analytical paths.

The dashboard explains:

- why each method appears;
- what it could establish;
- what it cannot establish;
- which inputs or design decisions are still missing;
- how the method fits into a policy-research workflow; and
- where the process may branch, loop, or stop.

It returns several compatible or complementary paths when appropriate. It does
not pretend that one method is universally best.

## Canonical examples

1. **Policy decision:** Which package of heat-risk interventions should a city
   adopt, given unequal neighborhood exposure, uncertain future temperatures,
   implementation constraints, and competing stakeholder priorities?
2. **Within-case explanation:** Why did one public program fail during a
   specific implementation episode despite formal organizational support?
3. **Evidence synthesis:** What is already known about remote-work policies,
   for whom, in which settings, and with what evidence limitations?

## Prototype contract

- `StudyBrief` owns the question, multi-valued aims, starting point, comparison
  scope, available evidence, and an optional same-evidence exposure warning.
- `MethodProfile` states method kind, suitable aims/scopes/evidence, source of
  leverage, possible claims, non-claims, requirements, workflow stages, and
  current portfolio availability.
- `route_study()` deterministically returns explainable candidate routes,
  missing design information, warnings, and a relevant workflow projection.
- `GET /api/catalog` and `POST /api/route` expose the same data and operation
  used by the browser.

## Success checks

- Multi-valued aims produce multiple paths without treating the aims as a
  ladder.
- A bounded within-case explanation with records surfaces Process Tracing; a
  population intervention-effect question does not.
- A policy decision surfaces evidence synthesis, empirical analysis, and
  appraisal/decision paths rather than treating policy analysis as one method.
- Reusing theory-generating evidence produces a visible warning, not a generic
  blocker.
- Every route shows positive warrant, limitations, and missing prerequisites.
- A ranked architecture stress-test portfolio states its selection criteria,
  falsifiable assumptions, visible output, effort, prerequisites, and stop rule.
- The critical flow works through both JSON and a rendered 1440px browser view.

## Non-goals

- no producer-engine invocation or cross-repository adapter;
- no LLM call or automated substantive research judgment;
- no universal method ontology, workflow state machine, evidence weight, or
  confidence score;
- no persistent project store, authentication, deployment, or production
  hardening;
- no claim that the current profile set is complete or that dashboard
  comprehension is empirically validated.

## Stop and next-decision boundary

Stop this slice after the question-first study map, method library, workflow
view, JSON parity, focused tests, and one browser observation work. Brian's
review should decide whether the next increment deepens study authoring,
connects one real method engine, or expands methodology coverage.
