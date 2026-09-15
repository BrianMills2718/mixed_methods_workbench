---
plan_id: "mixed_methods_workbench#method-dash-c2-plain-language"
dependencies: []
dependencies_reviewed: "2026-09-15"
---
# METHOD-DASH-C2: Plain-Language Study Brief

Status: implemented comprehension repair; stakeholder re-review pending

Authorized: Brian's 2026-08-12 review found that the primary study form was not
understandable without prior methodology knowledge. In particular, “interpret
meaning” and “where are you starting?” did not communicate the decisions being
asked of the user.

## User and task

The user is a researcher or analyst who has a real question but may not know the
names or boundaries of analytical methods. They should be able to describe the
work they need without first learning the dashboard's taxonomy.

## Visible correction

- Replace terse methodology labels with ordinary-language choices.
- Put a one-sentence explanation directly beside every primary choice.
- Add keyboard-accessible `?` tooltips for optional examples and distinctions.
- Explain why “what you already have” and “what you will study or compare”
  affect the suggested paths.
- Rewrite the result headings and summary so terms such as “warrant,” “source of
  leverage,” “comparison scope,” and “portfolio status” are not required for the
  primary journey.

Tooltips supplement the visible explanations; they do not carry information
required to complete the form.

## Preservation contract

- Preserve the question-first planner, method library, capability map, stress
  tests, three examples, typed brief, and deterministic routing semantics.
- Preserve multi-valued analytical goals and the same-evidence warning.
- Do not change method selection rules or claim that the dashboard chooses the
  correct method automatically.

## Development acceptance

- A fresh rendered page explains each primary input without opening a tooltip.
- Every primary choice has optional hover/focus help with a concrete example.
- “Interpret” is presented as understanding what something means to the people
  involved.
- The starting-point question explains that it asks what the user already has
  or needs to act on, and that the answer changes which method paths appear.
- The city-policy example still produces the same ten method paths.
- The invalid empty-form path remains visible, with no console or network
  errors in the repaired flow.

## Stop boundary

Stop after repairing this observed comprehension failure. Do not expand the
method taxonomy, change routing behavior, connect an engine, or redesign the
secondary architecture views in this slice.
