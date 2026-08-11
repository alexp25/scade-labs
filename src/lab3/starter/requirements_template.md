# Lab 3 — Software Requirements (student template)

Fill in every `TODO`. Keep the REQ IDs exactly as spelled — Lab 3 and Lab 4
reference them by this literal string.

## Limiter (Lab 3)

- REQ-LIM-01 — IF `value_in` is greater than `max`, THEN the Limiter shall set `value_out` to `max`.
- REQ-LIM-02 — TODO (clamp-to-minimum case)
- REQ-LIM-03 — TODO (pass-through case — pick ubiquitous or unwanted-behavior and justify your choice)

## Counter (Lab 3)

- REQ-CNT-01 — WHEN the Counter is initialized (first cycle), the Counter shall set `count` to `init_value`.
- REQ-CNT-02 — TODO (accumulation on every cycle after the first)

## Cruise Control (Lab 4)

- REQ-01 — IF the brake is pressed, THEN the Cruise Control system shall deactivate.
- REQ-02 — TODO (rewrite Lab 2's overspeed requirement as EARS)
- REQ-04 — TODO (rewrite Lab 2's "reactivation requires an explicit action" requirement as EARS)
- REQ-07 — TODO (regulator behavior while active — new for this model)
- REQ-08 — TODO (regulator throttle output stays within a safe range — new for this model, same pattern as REQ-LIM-01..03)

## Traceability (fill in after Activity 4C)

| REQ ID | State-table row(s) / design element it corresponds to |
|---|---|
| REQ-01 | TODO |
| REQ-02 | TODO |
| REQ-04 | TODO |
| REQ-07 | TODO |
| REQ-08 | TODO |

## Activity 5A — test case sketch for REQ-07

TODO — sketch a short scenario (cycle-by-cycle table or prose) that would
exercise REQ-07. State which column should carry the `REQ-07` tag, and
explain how the requirement gets checked given it has no single
`expected_throttle` value.
