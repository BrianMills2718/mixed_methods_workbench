# Investigation Spine

**Status:** authorized implementation slice
**Authorized by:** Brian, 2026-08-13, immediately after the merged product
integration assessment recommended this exact slice

## Outcome

Make one completed analytical journey understandable from the Mixed Methods
Workbench. The page follows a qualitative explanation into an independent
PsychosisBank/TalkBank case, shows what Process Tracing added, preserves its
withheld publication result, returns the explanation as unconfirmed, and names
the evidence needed next.

The internal proposition identifier `P5` is provenance, not the user-facing
name of the investigation.

## User contract

- **User:** a policy or social-science researcher unfamiliar with the internal
  repository history.
- **Question:** what did the new case establish about why PsychosisBank uses
  controlled access?
- **Primary action:** inspect the completed investigation from explanation to
  unresolved result.
- **Result:** a plain-language, evidence-linked conclusion plus the next
  evidence need.

## Visible flow

```text
qualitative interviews -> candidate explanation
-> different case and new sources -> Process Tracing appraisal
-> inconclusive and publication-blocked result
-> explanation retained as unconfirmed -> targeted evidence needs
```

## Boundaries

- Read three byte-pinned fixtures through Workbench-owned Pydantic consumers.
- Keep the mapping specific to this completed journey.
- Process Tracing owns its rival comparison, mechanism appraisal, and
  publication gate. Qualitative Coding owns the explanation and its returned
  disposition.
- Do not call an LLM, rerun either producer, import producer internals, retrieve
  sources, adopt Data Contracts, or introduce a universal analytical schema.
- Producer-retained run artifacts may be referenced by exact ID and digest;
  they must not be represented as embedded when their bytes are absent.

## Pass/fail criteria

1. A newcomer can answer the investigation question, what the qualitative work
   proposed, what Process Tracing added, what remains unresolved, and what
   evidence is needed next without knowing `P5`.
2. The browser page and JSON endpoint are projections of the same typed model.
3. Unsupported schema versions, fixture digest changes, missing source
   references, and contradictory result/disposition states fail loudly.
4. A blocked Process Tracing publication cannot appear as a validated theory,
   and Process Tracing cannot silently change the Qualitative Coding theory
   disposition.
5. The existing dashboard and its prior examples remain reachable.

## Development verification

- Focused model, corruption, route, and static-interface tests.
- Strict package type-check.
- One fresh-browser observation of the investigation route and one preserved
  dashboard control, with console/network inspection.
