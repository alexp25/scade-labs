# Lab 6 — Software Architecture

**Course:** Software Engineering
**Lesson:** Software Architecture
**Duration:** 45–60 minutes
**Tool:** None — a short recap, then the page's interactive, auto-graded diagram canvas for two hands-on exercises
**Work mode:** Individual, written deliverable
**Recommended prerequisite:** the Lesson 6 lecture/slides on Software Architecture (this lab assumes you've already seen that material) and [Lab 4](../lab4/) (you need to already know the Cruise Control system's interface — what it takes in, what it outputs — to complete Parts 1–2)

---

# Context

Lab 4 built the Cruise Control system's software in Scade One — but only
the software. It was never placed in a documented picture of the whole
vehicle it actually has to work inside: the driver who operates it, the
sensors it depends on, the signal bus its data travels over, the actuator
it commands. **Deciding a system's structure before deciding its design**
is what real safety-critical projects do; Lab 4 skipped straight to
design. This lab builds the missing system-level picture — starting from
what you already know about the Cruise Control system, not by
re-deriving its internal design — then extends it with a new safety
feature.

The Recap below brings the key vocabulary back to mind before you start.

---

# Learning Objectives

By the end of this lab you will be able to:

- Recall, in your own words, why software architecture matters, how it
  differs from design, and the four elements (components, connectors,
  interfaces, constraints) it's made of
- Apply the requirements-driven architecture pattern from the lecture to a
  system you already know
- Place a known component (the Cruise Control system from Lab 4) correctly
  inside a system-level (SysML-style) view of the *whole* vehicle, not
  just its embedded software
- Extend that system view with a new safety feature (automatic emergency
  braking), including proposed requirements and a description of how it
  would be simulated

---

# Recap — Software Architecture Essentials

> Quick reminder of the lecture, not a replacement for it. If any of this
> is unfamiliar, go back to the slides before starting Part 1.

- **Why it matters:** without an architecture, components get tightly
  coupled and changes get expensive; with one, you get organized structure,
  clear responsibilities, and easier evolution.
- **Definition (ISO/IEC/IEEE 42010):** a system's components, their
  relationships, and the principles guiding their design and evolution. It
  answers three questions — what are the major building blocks, how do
  they communicate, how is complexity managed?
- **Architecture vs design:** architecture is **WHAT** (major components,
  responsibilities, interfaces); design is **HOW** (algorithms, data
  structures, detailed behavior). Architecture changes are expensive
  because they affect the whole system; design changes are usually
  localized.
- **Four elements of embedded architecture — you'll use this exact
  vocabulary in Part 1:** **components** (application functions, drivers,
  middleware, HAL), **connectors** (function calls, buses, message queues,
  pub/sub), **interfaces** (provided/required services, hardware/
  communication/sensor interfaces), **constraints** (timing, memory, power,
  safety, security).
- **Quality attributes drive architecture:** most architectural decisions
  come from non-functional requirements, not functional ones — e.g. "the
  system shall respond within 100 ms" drives caching, parallelism, or
  distributed services, none of which the requirement itself mentions.
- **Requirements-driven architecture:** architecture should flow from
  requirements, with traceability running down to implementation and
  testing and back — the same idea as Lab 3's `#pragma requirement`
  mechanism, one level higher up.
- **The lecture's worked example:** an autonomous medical monitoring
  system's requirements (continuous ECG acquisition, alarm within 2
  seconds, patient data encryption, 24/7 availability) each map to a
  *specific* architectural decision — edge sensor + gateway + ingestion;
  an optimized stream/alarm pipeline; TLS + encrypted storage + key
  management; load balancer + replication + failover — no single component
  does everything. **Part 1 asks you to place a system you already know
  into a similar system-level picture.**

---

> **Parts 1–2's diagrams are an interactive canvas, not a picture.** Each
> one gives you the component boxes already placed — no connections yet.
> Drag from the small dot on a box's right edge to a dot on another box's
> left edge to draw a connection between them (click a connection line and
> press Delete to remove it; drag a box to reposition it). Click
> **✓ Check** at any point to see how many of the expected connections
> you've found so far — this is auto-graded, not a hint, so use the bullet
> list in each activity to work out what should connect to what. If you're
> signed in, each Check also records your score for that diagram to your
> account, the same way a quiz score is recorded — if you're not signed
> in, Check still works, it just isn't tracked anywhere. **↺ Reset** clears
> your connections and puts the boxes back where they started. Use
> **−** / **+** to zoom, or click the percentage to reset it; the small
> overview box in the bottom-right corner shows the whole diagram at once
> — click, or click-and-drag, anywhere on it to pan the main view there in
> real time. Your in-progress layout itself is always kept only in your
> own browser (`localStorage`), signed in or not.

# Part 1 — Hands-On: System-Level View (SysML-Style)

You already know the Cruise Control system's interface from Lab 2 and
Lab 4: it's turned on/off and resumed by driver controls (`on`, `res`,
`accel`, `brake`), it needs the current vehicle speed (`v_speed`), and it
produces a `throttle` command. You don't need to re-derive any of its
internals here — treat it as a single, known component (the **Cruise
Control ECU**) and place it in the physical system it actually lives
inside: the driver, the sensors that feed it, the bus its signals travel
over, and the actuator that receives its output.

> **Caveat:** the diagram below is a **SysML-style** block diagram —
> boxes for parts, arrows for connections/flows — because this repo has no
> SysML modeling tool installed. It is not output from a real SysML tool
> (e.g. a `.sysml`/Capella/Papyrus export), and should not be read as one.

## Activity 1A — Draw the whole-system block diagram

Here is exactly how signals flow through this system — turning this list
into connections is the exercise:

- **Driver → HMI** — the driver presses buttons and pedals on the
  dashboard.
- **HMI → Vehicle Signal Bus** — the HMI publishes the driver's requests
  (`on`, `res`, `set_point`) onto the shared bus.
- **Wheel-Speed Sensor → Bus**, **Brake Pedal Sensor → Bus**,
  **Accelerator Pedal Sensor → Bus** — each sensor publishes its own
  reading onto the same bus, rather than wiring straight to the ECU.
- **Bus → Cruise Control ECU** — the ECU reads whatever signals it needs
  off the bus.
- **Cruise Control ECU → Bus** — the ECU publishes its `throttle` command
  back onto the bus.
- **Bus → Throttle/Powertrain Actuator** — the actuator reads the
  throttle command off the bus.
- **Throttle/Powertrain Actuator → Vehicle Dynamics** — the actuator
  applies torque to the vehicle.
- **Vehicle Dynamics → Wheel-Speed Sensor** — the vehicle's resulting
  speed is what the sensor measures next, closing the loop.
- **HMI → Driver** — the HMI reports status back to the driver.

**This is the deliverable for Part 1.** The boxes below are the parts of
the whole vehicle system — driver, HMI, three sensors, the signal bus, the
Cruise Control ECU, the throttle actuator, and the vehicle itself. None of
them are connected yet. Draw the 11 connections listed above, then click
**✓ Check**.

```flowgraph
{
  "height": 500,
  "nodes": [
    { "key": "Driver", "label": "Driver", "x": 20, "y": 40 },
    { "key": "HMI", "label": "HMI / Dashboard", "x": 20, "y": 240 },
    { "key": "WheelSensor", "label": "Wheel-Speed Sensor", "x": 300, "y": 20 },
    { "key": "BrakeSensor", "label": "Brake Pedal Sensor", "x": 300, "y": 140 },
    { "key": "AccelSensor", "label": "Accelerator Pedal Sensor", "x": 300, "y": 260 },
    { "key": "Bus", "label": "Vehicle Signal Bus\n(CAN-style)", "x": 560, "y": 140 },
    { "key": "ECU", "label": "Cruise Control ECU\n(the system you built in Lab 4)", "x": 800, "y": 40 },
    { "key": "Powertrain", "label": "Throttle / Powertrain Actuator", "x": 800, "y": 220 },
    { "key": "Vehicle", "label": "Vehicle Dynamics\n(the physical car)", "x": 800, "y": 380 }
  ],
  "expected": [
    ["Driver", "HMI"],
    ["HMI", "Bus"],
    ["WheelSensor", "Bus"],
    ["BrakeSensor", "Bus"],
    ["AccelSensor", "Bus"],
    ["Bus", "ECU"],
    ["ECU", "Bus"],
    ["Bus", "Powertrain"],
    ["Powertrain", "Vehicle"],
    ["Vehicle", "WheelSensor"],
    ["HMI", "Driver"]
  ]
}
```

## Reflection

The **Cruise Control ECU** box stands in for everything you actually built
in Lab 4 — the state machine, the PI regulator, the clamping logic — none
of which needs to appear here. That's what "architecture manages
complexity" means in practice: each level of an architecture hides the
detail of the level below it. You don't need to see the regulator's
internals to reason about how the ECU fits into the vehicle; you don't
need to see the wheel-speed sensor's electrical interface either.

---

# Part 2 — Hands-On: Extending the Architecture — Automatic Emergency Braking

This is a **paper design exercise** that extends Part 1's diagram — it
does not touch Lab 4's Scade model. Nothing here is implemented in
`src/lab4/starter/CruiseControl/` — the shipped Scade One model, its
generated wrapper, and its scenario CSVs are **not** modified by this lab.
You are practicing requirements-driven architecture on a *new* feature, the
same way the Recap's medical-monitoring example was worked for you.

## Activity 2A — Propose the new component

Add an **Emergency Braking Controller** and an **Obstacle/Distance Sensor**
to the architecture from Part 1:

| Component | Responsibility |
|---|---|
| Obstacle/Distance Sensor | Measures `distance` to the nearest obstacle ahead and `relative_speed` toward it |
| Emergency Braking Controller | If a collision risk is detected, outputs a `brake_override` command that takes priority over both the driver's brake pedal and the Cruise Control ECU's `throttle` output |

**Interface:**

| Component | Provided interface | Required interface |
|---|---|---|
| Obstacle/Distance Sensor | `distance`, `relative_speed` | (physical sensing hardware — outside the software boundary) |
| Emergency Braking Controller | `brake_override` (bool/float) | `distance`, `relative_speed`, `v_speed` |

**Connector / arbitration:** both new components join the system the same
way every existing one already does — as participants on the shared
signal bus, not through a special new kind of wire. The Obstacle/Distance
Sensor publishes `distance`/`relative_speed` onto the bus exactly like the
three existing sensors publish theirs. The Emergency Braking Controller
reads whatever it needs off the bus and publishes `brake_override` back
onto it, exactly like the ECU publishes its `throttle` command.
Arbitration — `brake_override` taking priority over the ECU's `throttle`
whenever both are present — happens where the two commands are actually
consumed, at the Powertrain Actuator, not through a dedicated override
wire.

## Activity 2B — Propose requirements (EARS)

The requirement IDs already in use across this repo are REQ-01 through
REQ-08 (REQ-01–06 from Lab 2, REQ-07/08 added in Lab 3/4 for the
regulator). The next free IDs are REQ-09/REQ-10. Write them in EARS syntax,
the same style taught in Lab 3 Part 1:

> **REQ-09 (proposed — not implemented in the shipped model)** — IF the
> Obstacle/Distance Sensor reports a collision risk (e.g. `distance` below
> a safety threshold given the current `relative_speed`), THEN the
> Emergency Braking Controller shall set `brake_override` to override both
> the driver's brake input and the Cruise Control ECU's `throttle`
> output.
>
> **REQ-10 (proposed — not implemented in the shipped model)** — WHILE
> `brake_override` is active, the Cruise Control system shall remain
> suspended and shall not resume regulation until `brake_override` clears
> and the driver issues `res`.

These two IDs are explicitly marked **proposed** — this lab does not add
them to `src/lab3/solution/requirements.md` or to `CC_design.swan`. That
would require a real maintainer/instructor decision and a Scade One
session, exactly the same boundary Lab 4's Activity 7A draws around its own
unfinished traceability links.

## Activity 2C — How would you simulate it?

You don't need to write code for this — describe the approach in a
sentence or two, using the mechanism Lab 4 Part 6 already built:

Lab 4's `evaluate_cc_full_report.py` drives the generated wrapper
cycle-by-cycle from `scenarios/*.csv`, one row per simulation cycle, with
optional `expected_throttle`/`req`/`note` columns. Extending it for REQ-09/
REQ-10 would mean: (1) adding an `obstacle_distance` (and optionally
`relative_speed`) column to the scenario CSV schema, (2) adding rows where
`obstacle_distance` drops below the safety threshold mid-scenario, tagged
`req = REQ-09`, and (3) checking — the same way REQ-07 already is (Lab 3's
Activity 5A reference answer) — that the *trend* is right: `brake_override`
should engage and `throttle` should fall, rather than asserting one exact
value. This is a description of an extension, not a new script — no file
under `src/lab4/` is created or changed by this lab.

## Activity 2D — Draw the extended architecture

**This is the deliverable for Part 2.** The canvas below has the same
nine boxes from Part 1, plus two new ones: the Obstacle/Distance Sensor
and the Emergency Braking Controller from Activity 2A. Re-draw Part 1's
11 connections, then add:

- **Obstacle/Distance Sensor → Bus** — publishes `distance`/
  `relative_speed`, the same way the existing sensors do.
- **Bus → Emergency Braking Controller** — it reads `distance`,
  `relative_speed`, and `v_speed` off the bus.
- **Emergency Braking Controller → Bus** — it publishes `brake_override`
  back onto the bus, for the Powertrain Actuator to prioritize over the
  ECU's `throttle` command.

Click **✓ Check** to see how many of the 14 expected connections you've
found.

```flowgraph
{
  "height": 620,
  "nodes": [
    { "key": "Driver", "label": "Driver", "x": 20, "y": 40 },
    { "key": "HMI", "label": "HMI / Dashboard", "x": 20, "y": 280 },
    { "key": "WheelSensor", "label": "Wheel-Speed Sensor", "x": 300, "y": 20 },
    { "key": "BrakeSensor", "label": "Brake Pedal Sensor", "x": 300, "y": 140 },
    { "key": "AccelSensor", "label": "Accelerator Pedal Sensor", "x": 300, "y": 260 },
    { "key": "Obstacle", "label": "Obstacle/Distance Sensor", "x": 300, "y": 380 },
    { "key": "Bus", "label": "Vehicle Signal Bus\n(CAN-style)", "x": 560, "y": 200 },
    { "key": "ECU", "label": "Cruise Control ECU\n(the system you built in Lab 4)", "x": 800, "y": 40 },
    { "key": "Powertrain", "label": "Throttle / Powertrain Actuator", "x": 800, "y": 220 },
    { "key": "Emergency", "label": "Emergency Braking Controller", "x": 800, "y": 380 },
    { "key": "Vehicle", "label": "Vehicle Dynamics\n(the physical car)", "x": 800, "y": 540 }
  ],
  "expected": [
    ["Driver", "HMI"],
    ["HMI", "Bus"],
    ["WheelSensor", "Bus"],
    ["BrakeSensor", "Bus"],
    ["AccelSensor", "Bus"],
    ["Bus", "ECU"],
    ["ECU", "Bus"],
    ["Bus", "Powertrain"],
    ["Powertrain", "Vehicle"],
    ["Vehicle", "WheelSensor"],
    ["HMI", "Driver"],
    ["Obstacle", "Bus"],
    ["Bus", "Emergency"],
    ["Emergency", "Bus"]
  ]
}
```

## Reflection

Notice this activity re-used Part 1's diagram as a starting point instead
of starting from nothing, and that the two new components join the system
the *same way* every existing one does (as bus participants) instead of
needing a special-case connector — that's what "architecture is driven by
requirements, and requirements evolve" looks like in practice: a new
requirement (REQ-09/REQ-10) extends an existing architecture, it doesn't
replace it.

---

# Summary

- **Software architecture is the blueprint of a system** — it defines the
  system's high-level structure, major components, interfaces, and
  interactions *before* implementation begins, and it should be driven by
  requirements rather than technology choices.
- **Architecture and design are different activities** — Lab 4 built and
  validated the Cruise Control software without ever placing it in a
  documented picture of the whole vehicle system around it; Part 1 of this
  lab builds that missing picture, using what Lab 4 already established as
  the ECU's interface, rather than re-deriving its internals.
- **Architecture evolves without being replaced** — Part 2 extends Part
  1's system view with a new safety feature by adding new participants
  onto the same shared bus every existing component already uses, not by
  redesigning what was already there.
- **A well-documented architecture pays off downstream** — better
  traceability, easier validation, better maintainability, more
  predictable quality, less redesign effort, and (mentioned only as
  educational/reflection context, not a compliance claim about this repo)
  easier certification.

---

# Quiz

Answer the ten questions below to check your understanding of this lab's
material.

<style>
  #architecture-quiz { margin-top: 1rem; }
  .quiz-q { margin-bottom: 1.1rem; padding: 1.15rem 1.25rem; background: var(--white); border: 1px solid var(--border); border-radius: 8px; }
  .quiz-q strong { display: block; margin-bottom: .7rem; color: var(--navy); font-size: .97rem; }
  .quiz-option { display: flex; align-items: flex-start; gap: .55rem; padding: .42rem .55rem; border-radius: 5px; cursor: pointer; transition: background .13s; user-select: none; font-size: .92rem; }
  .quiz-option:hover { background: var(--ice); }
  .quiz-option input { margin-top: .22rem; flex-shrink: 0; accent-color: var(--blue); }
  .quiz-option.correct { background: #E8F5E9; color: #1B5E20; font-weight: 600; border-radius: 5px; }
  .quiz-option.wrong   { background: #FFEBEE; color: #B71C1C; text-decoration: line-through; border-radius: 5px; }
  .quiz-option.reveal  { background: #FFF8E1; color: #BF360C; font-weight: 600; border-radius: 5px; }
  #quiz-submit { margin-top: .75rem; padding: .55rem 1.5rem; background: var(--blue); color: var(--white); border: none; border-radius: 6px; font-size: .9rem; font-weight: 600; cursor: pointer; transition: background .15s; }
  #quiz-submit:hover:not(:disabled) { background: var(--sky); }
  #quiz-submit:disabled { opacity: .45; cursor: default; }
  #quiz-score { display: inline-block; margin-left: 1rem; font-size: 1rem; font-weight: 700; vertical-align: middle; }
  #quiz-reset { display: none; margin-left: .75rem; padding: .55rem 1.1rem; background: transparent; color: var(--muted); border: 1px solid var(--border); border-radius: 6px; font-size: .88rem; cursor: pointer; transition: color .15s, border-color .15s; vertical-align: middle; }
  #quiz-reset:hover { color: var(--blue); border-color: var(--sky); }
</style>

<div id="architecture-quiz">
  <div class="quiz-q" data-correct="b">
    <strong>Q1 — According to ISO/IEC/IEEE 42010, software architecture consists of a system's components, their relationships, and the principles guiding their design and evolution. Which question does architecture NOT primarily answer?</strong>
    <label class="quiz-option"><input type="radio" name="q1" value="a"><span>What are the major building blocks?</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="b"><span>What exact algorithm does each function use internally?</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="c"><span>How do the building blocks communicate?</span></label>
    <label class="quiz-option"><input type="radio" name="q1" value="d"><span>How is complexity managed?</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q2 — A team skips architecture and lets every module call every other module directly as the system grows. Which consequence does the lesson predict?</strong>
    <label class="quiz-option"><input type="radio" name="q2" value="a"><span>Reuse becomes easier</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="b"><span>Quality attributes become easier to achieve</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="c"><span>Components become tightly coupled and changes become expensive</span></label>
    <label class="quiz-option"><input type="radio" name="q2" value="d"><span>Testing becomes easier</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q3 — Which statement best distinguishes architecture from design?</strong>
    <label class="quiz-option"><input type="radio" name="q3" value="a"><span>Architecture defines major components and their responsibilities (WHAT); design defines the detailed implementation (HOW)</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="b"><span>Architecture and design are two names for the same activity</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="c"><span>Design always happens before architecture</span></label>
    <label class="quiz-option"><input type="radio" name="q3" value="d"><span>Architecture is only concerned with class-level method signatures</span></label>
  </div>
  <div class="quiz-q" data-correct="d">
    <strong>Q4 — A change to the architecture (e.g. splitting one service into two) is typically more expensive than a change to the design of one function. Why?</strong>
    <label class="quiz-option"><input type="radio" name="q4" value="a"><span>Architecture changes never affect other components</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="b"><span>Design changes always require full system re-certification</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="c"><span>Architecture has no impact on system quality</span></label>
    <label class="quiz-option"><input type="radio" name="q4" value="d"><span>Architecture decisions impact the whole system, while design changes are typically localized</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q5 — In embedded software architecture, which pairing correctly matches an element to an example?</strong>
    <label class="quiz-option"><input type="radio" name="q5" value="a"><span>Constraint — a message queue between two tasks</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="b"><span>Connector — a CAN bus carrying signals between the cruise control ECU and a sensor</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="c"><span>Component — a real-time performance budget of 10 ms</span></label>
    <label class="quiz-option"><input type="radio" name="q5" value="d"><span>Interface — the device driver implementation itself</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q6 — A requirement states "the system shall respond within 100 ms." Which of the following is this requirement's quality attribute, and what kind of architectural decision does it typically drive?</strong>
    <label class="quiz-option"><input type="radio" name="q6" value="a"><span>Security — it drives the choice of an encryption algorithm</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="b"><span>Portability — it drives the choice of programming language</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="c"><span>Performance — it may drive caching, parallel processing, or distributed services</span></label>
    <label class="quiz-option"><input type="radio" name="q6" value="d"><span>Maintainability — it drives the choice of variable naming conventions</span></label>
  </div>
  <div class="quiz-q" data-correct="a">
    <strong>Q7 — In Part 1's whole-vehicle diagram, which pairing is correct?</strong>
    <label class="quiz-option"><input type="radio" name="q7" value="a"><span>The Vehicle Signal Bus is a connector, not a component</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="b"><span>The Wheel-Speed Sensor publishes directly to the ECU, bypassing the bus</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="c"><span>The HMI has no connection back to the Driver</span></label>
    <label class="quiz-option"><input type="radio" name="q7" value="d"><span>The Powertrain Actuator is the source of the vehicle's speed signal</span></label>
  </div>
  <div class="quiz-q" data-correct="d">
    <strong>Q8 — Why does Part 1's whole-vehicle diagram treat the Cruise Control system as a single "ECU" box instead of showing its internal state machine and regulator separately?</strong>
    <label class="quiz-option"><input type="radio" name="q8" value="a"><span>Because that internal design doesn't actually exist</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="b"><span>Because SysML-style diagrams cannot represent embedded software</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="c"><span>Because Lab 4 never built that internal design</span></label>
    <label class="quiz-option"><input type="radio" name="q8" value="d"><span>Because each level of architecture hides the detail of the level below it — you already built and understand that detail from Lab 4, so this view doesn't need to repeat it</span></label>
  </div>
  <div class="quiz-q" data-correct="b">
    <strong>Q9 — Part 2 proposes REQ-09/REQ-10 for an Automatic Emergency Braking extension. What is the correct status of this proposal in this repository?</strong>
    <label class="quiz-option"><input type="radio" name="q9" value="a"><span>REQ-09/REQ-10 are implemented and traced inside the shipped `CC_design.swan`</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="b"><span>REQ-09/REQ-10 are a proposed, paper-only extension — not implemented in the shipped model or scenarios</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="c"><span>REQ-09/REQ-10 replace REQ-01 and REQ-02</span></label>
    <label class="quiz-option"><input type="radio" name="q9" value="d"><span>REQ-09/REQ-10 were auto-generated by `evaluate_cc_full_report.py`</span></label>
  </div>
  <div class="quiz-q" data-correct="c">
    <strong>Q10 — Which best summarizes this lab's central lesson about Lab 4?</strong>
    <label class="quiz-option"><input type="radio" name="q10" value="a"><span>Lab 4's software was incorrect because no system-level view existed</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="b"><span>Architecture and design are the same activity, so Lab 4 lost nothing by skipping it</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="c"><span>Lab 4's software worked, but it was never placed in a documented system-level picture until this lab built one — doing that before implementation is the better practice, but doing it afterward is still valuable</span></label>
    <label class="quiz-option"><input type="radio" name="q10" value="d"><span>Requirements are unnecessary once an architecture exists</span></label>
  </div>
  <div>
    <button id="quiz-submit" type="button">Check Answers</button>
    <button id="quiz-reset" type="button">Try Again</button>
    <span id="quiz-score"></span>
  </div>
</div>
