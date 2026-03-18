---
marp: true
paginate: true
size: 16:9
title: Converting a US Patent to CAD with AI
description: Walkthrough of the Hydraulic Involute Cam Actuator example from patent2cad.md
style: |
  :root {
    --ink: #14213d;
    --accent: #c1121f;
    --gold: #fca311;
    --paper: #f8f4ec;
    --muted: #5c677d;
    --panel: #ffffff;
  }

  section {
    font-family: "Aptos", "Segoe UI", sans-serif;
    background: linear-gradient(160deg, var(--paper) 0%, #fffdf7 55%, #f1efe8 100%);
    color: var(--ink);
    padding: 54px 64px;
  }

  h1, h2, h3 {
    font-family: "Georgia", "Times New Roman", serif;
    letter-spacing: 0.02em;
    color: var(--ink);
    margin-bottom: 0.35em;
  }

  h1 {
    font-size: 1.9em;
    border-bottom: 6px solid var(--gold);
    display: inline-block;
    padding-bottom: 0.1em;
  }

  h2 {
    font-size: 1.45em;
  }

  p, li {
    font-size: 0.92em;
    line-height: 1.35;
  }

  strong {
    color: var(--accent);
  }

  code {
    font-family: "IBM Plex Mono", "Consolas", monospace;
    font-size: 0.92em;
    background: rgba(20, 33, 61, 0.08);
    padding: 0.08em 0.28em;
    border-radius: 6px;
  }

  blockquote {
    border-left: 8px solid var(--gold);
    background: rgba(255, 255, 255, 0.72);
    padding: 16px 20px;
    margin: 18px 0;
  }

  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
    align-items: start;
  }

  .panel {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(20, 33, 61, 0.1);
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 12px 24px rgba(20, 33, 61, 0.06);
  }

  .visual {
    border: 2px dashed rgba(20, 33, 61, 0.25);
    border-radius: 16px;
    padding: 18px;
    min-height: 210px;
    background: rgba(255, 255, 255, 0.55);
    color: var(--muted);
  }

  .small {
    font-size: 0.76em;
    color: var(--muted);
  }
---

# Converting a US Patent to CAD with AI

## Hydraulic Involute Cam Actuator

US Patent `8,047,094 B2` -> figure interpretation -> kinematic reasoning -> `OpenSCAD`

Source narrative: `patent2cad.md`

---

## The Goal

Turn a patent drawing and text description into a **mechanically coherent CAD model**, not just a visually similar shape.

<div class="two-col">
<div class="panel">

**Input**

- Patent figure `1A`
- Patent claims and equations
- User feedback on geometry, orientation, and contact

</div>
<div class="panel">

**Output**

- Working `OpenSCAD` model
- Explicit kinematic relationships
- `URDF` intermediate description
- Parameterized final assembly

</div>
</div>

---

## Why This Is Hard

Generating CAD from a patent is not a pure text-to-shape problem.

- Patent figures are schematic, not production drawings
- Claims define constraints, not full geometry
- Contact mechanics matter more than visual resemblance
- Multiple components move in different planes and frames
- A plausible 3D model can still be mechanically wrong

> The core challenge was moving from "draw something cam-like" to "model the exact rolling constraint between rollers and involute surfaces."

---

## The Example Trajectory

<div class="panel">

1. Initial prompt: "implement figure `1A` in `OpenSCAD`"
2. First model: mathematically inspired, but mechanically wrong
3. User critique tightened the problem around **two pistons + two rollers + dual involute surface**
4. The workflow shifted into kinematics, part decomposition, and coordinate consistency
5. Final success came from solving **contact location and offset calibration**

</div>

<div class="small">
This is the important presentation shift: the example is best told as an iterative engineering dialogue, not as a one-shot generation demo.
</div>

---

## Step 1: Naive Geometry Fails

<div class="two-col">
<div class="panel">

**What the model did first**

- Pulled equations from the patent
- Drew involute-like lobes
- Extruded them into a cam body

</div>
<div class="panel">

**Why it failed**

- Shape did not reflect the actual mechanism
- Pistons and rollers were not meaningfully coupled
- The geometry looked analytical, but not functional

</div>
</div>

<div class="visual">
Suggested visual:

- Patent figure `1A`
- First incorrect `OpenSCAD` render
- One annotation showing "mathematically derived, mechanically wrong"
</div>

---

## Step 2: Reframe Around The Mechanism

After critique, the problem was restated in physical terms:

- Two hydraulic pistons are **parallel**
- Each piston carries a **roller**
- The rollers engage a **dual involute curved surface**
- The cam and body part `12` must behave as **one solid rotating part**

<div class="panel">

This was the turning point: the AI stopped optimizing the curve alone and started modeling the **interaction** between actuator, roller, cam, and pivot.

</div>

---

## Step 3: Build The Kinematic Chain

<div class="two-col">
<div class="panel">

**Fixed**

- Base housing (`14`)
- Main pivot (`16`)

**Linear motion**

- Left and right hydraulic rods
- Rollers translated with piston motion

</div>
<div class="panel">

**Rotary motion**

- Arm / cam body (`12` + `18`)
- Rotation about the pivot

**Constraint**

- Linear actuator displacement must remain consistent with involute contact

</div>
</div>

Key relation used repeatedly:

`Delta y = r * Delta theta`

---

## Step 4: Introduce Explicit Representations

The workflow became more reliable once the system was represented in multiple ways.

<div class="two-col">
<div class="panel">

**Part list + orientations**

- Which parts are fixed
- Which parts translate
- Which part rotates

</div>
<div class="panel">

**`URDF` abstraction**

- Revolute pivot
- Prismatic pistons
- `mimic` relationships encoding the coupling

</div>
</div>

<div class="small">
This is a strong story point for the deck: AI improved once the mechanism was expressed as structure and constraints, not just code.
</div>

---

## Step 5: Solve Coordinate Consistency

Several iterations focused on a non-obvious issue:

- Cylinder bodies, rods, rollers, and cam were not initially aligned in a consistent global frame
- Some parts were correct in isolation but wrong relative to the rest of the chain
- The roller axis had to be oriented to **roll along** the involute surface
- The cam surface had to face the rollers from the correct side

<div class="visual">
Suggested visual:

- One exploded view with labeled axes
- One corrected assembly view
- Highlight the orientation fixes: `rotate([90,0,0])`, cam facing downward, roller axis parallel to pivot axis
</div>

---

## Step 6: Contact Is The Real Problem

The last major improvement was not aesthetic. It was geometric contact closure.

<div class="panel">

**What had to be true**

- The roller must maintain a single contact point with the cam
- The roller cannot float away from the cam
- The roller cannot penetrate the cam
- Contact must hold across the full motion range

</div>

This led to the key insight:

- The **roller center must lie on the pitch curve**
- The physical cam surface is the pitch curve offset inward by the roller radius

---

## Final Geometric Correction

The final model used a corrected neutral contact depth and removed an earlier double subtraction of the roller radius.

```text
Neutral contact depth = -r * (pi / 2)
Roller center lies on the pitch curve
Physical cam surface = inward offset of that pitch curve
```

<div class="panel">

This is the most important technical lesson in the example:

**getting the involute equation was not enough; getting the contact geometry right was the breakthrough.**

</div>

---

## Final Assembly Logic

<div class="two-col">
<div class="panel">

**Rotating assembly**

- Fused cam body
- Central hub to close the gap
- Upper arm mass
- Single solid part for body `12` and cam surfaces

</div>
<div class="panel">

**Actuator branches**

- Left and right rollers at `x = +/- r`
- Piston displacement computed from `theta`
- Cam vertical offset exposed as a parameter for tuning

</div>
</div>

---

## What The AI Actually Did Well

- Translated user feedback into progressively sharper constraints
- Switched between geometry, kinematics, and robot-description abstractions
- Repaired frame alignment issues
- Parameterized the final model so the user could tune fit and contact

## Where Human Guidance Mattered

- Detecting when the geometry "didn't make sense"
- Re-centering the task on mechanism behavior
- Catching contact, attachment, and orientation errors

---

## Takeaways For Patent-To-CAD Systems

<div class="panel">

1. Patent interpretation should produce a **mechanism graph**, not just code.
2. Intermediate representations like part lists, kinematic chains, and `URDF` reduce error.
3. Iteration with visual verification is essential.
4. Contact and constraint solving are the real gate between "looks right" and "works right."
5. The most effective AI loop was: **generate -> inspect -> formalize constraints -> regenerate**.

</div>

---

## Suggested Demo Sequence

- Show patent figure `1A`
- Show the first wrong `OpenSCAD` result
- Show the point where the problem is reframed around pistons, rollers, and involute surfaces
- Show the kinematic relation `Delta y = r * Delta theta`
- Show the `URDF` abstraction
- Show the final render and call out the contact fix

<div class="small">
If presenting live, animate the final `OpenSCAD` model and pause on one frame where the roller-to-cam contact is clearly visible.
</div>

---

## Closing

This example is a useful benchmark because it demonstrates that:

- **LLMs can help translate patents into CAD**
- but only when the workflow includes **mechanical reasoning, representation changes, and iterative correction**

<div class="visual">
Suggested final visual:

- Final `OpenSCAD` render
- Small inset of patent figure `1A`
- Caption: "From patent drawing to parameterized mechanism"
</div>

