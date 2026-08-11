# Lab 3 — Software Requirements (instructor reference)

Reference answer set for Lab 3's activities. REQ IDs here are the ones Lab 3
and Lab 4 reference — do not renumber without updating both.

## Limiter (Lab 3, Part 2)

`limiter(value_in, min, max) -> value_out`

- **REQ-LIM-01** — IF `value_in` is greater than `max`, THEN the Limiter shall set `value_out` to `max`.
- **REQ-LIM-02** — IF `value_in` is less than `min`, THEN the Limiter shall set `value_out` to `min`.
- **REQ-LIM-03** — The Limiter shall set `value_out` equal to `value_in` whenever `value_in` is within `[min, max]`. *(Ubiquitous — this is the normal case, not an unwanted-behavior condition; REQ-LIM-01/02 already cover the two abnormal cases, so this one is "otherwise.")*

## Counter (Lab 3, Part 4)

`counter(init_value, step) -> count`

- **REQ-CNT-01** — WHEN the Counter is initialized (first cycle), the Counter shall set `count` to `init_value`.
- **REQ-CNT-02** — WHEN a simulation cycle occurs after the first, the Counter shall set `count` to the previous cycle's `count` plus `step`.

## Cruise Control (Lab 4)

Reuses Lab 2's REQ-01/02/04 IDs; adds REQ-07/08 for behavior that only exists once the regulator and limiter become separate model elements.

- **REQ-01** — IF the brake is pressed, THEN the Cruise Control system shall deactivate (transition out of `cc_active`/`cc_enabled` toward `cc_disabled` or `cc_standby`, per the state table).
- **REQ-02** — IF vehicle speed exceeds the safety threshold (130 km/h), THEN the Cruise Control system shall deactivate.
- **REQ-04** — WHILE Cruise Control is in `cc_standby` (suspended), the system shall remain suspended until the driver issues an explicit `res` (resume) action — `set` alone shall not resume regulation.
- **REQ-07** — WHILE Cruise Control is in `cc_active`, the regulator shall drive `throttle` to bring `v_speed` toward `set_point`.
- **REQ-08** — The regulator's `throttle` output shall remain within `[0, max_throttle]` at all times. *(Ubiquitous — same shape as REQ-LIM-01..03, because the regulator reuses the `limiter` operator internally to enforce this.)*

## Traceability preview

| REQ ID | State-table row(s) (Lab 4, Activity 4B) |
|---|---|
| REQ-01 | `cc_disabled` → `cc_enabled` (guard `on`); `cc_enabled` → `cc_disabled` (guard `not on`) |
| REQ-02 | `cc_active` → `cc_standby` (guard `brake > 10.0 or accel > 10.0`), speed-exceeds-threshold case |
| REQ-04 | `cc_active` → `cc_standby`; `cc_standby` → `cc_active` (guard `res and brake < 10.0`) |
| REQ-07 | `cc_active` internal behavior — `regulator` suboperator |
| REQ-08 | `regulator` → internal `limiter` instance clamping `throttle` |

## Activity 1A — self-checking quiz

Activity 1A is now an auto-graded multiple-choice quiz in `docs/lab3/lab.md`
(`#ears-pattern-quiz`), not a free-text exercise — there's nothing to grade
by hand. Answer key, for reference: Q1 Ubiquitous, Q2 Event-driven, Q3
State-driven, Q4 Optional feature.

## Activity 5A reference answer — test case for REQ-07

> **REQ-07** — WHILE Cruise Control is active, the regulator shall drive `throttle` toward `set_point`.

REQ-07 can't be checked with a single `expected_throttle` value — the PI
regulator converges gradually, so "correct" means *the trend is right*, not
*one exact number*. A reasonable scenario:

| cycle | on | v_speed | set_point (locked at activation) | expected_throttle | req | note |
|---|---|---|---|---|---|---|
| 1 | True | 20.0 | 28.0 (locked from rising edge of `on`) | *(blank)* | REQ-07 | activation, v_speed below set_point |
| 2–13 | True | ramps from 20.0 toward 28.0 | 28.0 | *(blank)* | REQ-07 | v_speed should approach set_point as throttle regulates |

This is exactly `tc02_cc_active_regulates.csv` in Lab 4's reference
scenarios: every row is tagged `req = REQ-07` (or left blank, per the "no
single expected value" note), and the requirement is checked **visually**
via the Activity 6E throttle/`v_speed` chart — `v_speed` should trend toward
`set_point` over the run, not jump there in one cycle and not diverge. This
is the answer to "how do you check a requirement with no hardcoded
expected value": the `req` tag still provides traceability (this scenario
is evidence for REQ-07) even when the checkpoint itself isn't a pass/fail
assertion.
