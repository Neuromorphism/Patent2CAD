---
marp: true
paginate: true
size: 16:9
title: Generating CAD with AI
description: AI CAD generation presentation with patent-to-CAD as a worked example
style: |
  :root {
    --ink: #101820;
    --accent: #005f73;
    --signal: #ee9b00;
    --paper: #f7f7f2;
    --muted: #52616b;
  }
  section {
    font-family: "Aptos", "Segoe UI", sans-serif;
    background: linear-gradient(135deg, #f7f7f2 0%, #fffdf7 50%, #eef3f3 100%);
    color: var(--ink);
    padding: 54px 64px;
  }
  h1, h2, h3 {
    font-family: "Georgia", "Times New Roman", serif;
    color: var(--ink);
    letter-spacing: 0.02em;
  }
  h1 {
    border-bottom: 6px solid var(--signal);
    display: inline-block;
    padding-bottom: 0.1em;
  }
  p, li {
    font-size: 0.92em;
    line-height: 1.35;
  }
  strong { color: var(--accent); }
  code {
    font-family: "IBM Plex Mono", "Consolas", monospace;
    background: rgba(16, 24, 32, 0.08);
    padding: 0.08em 0.28em;
    border-radius: 6px;
  }
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
  }
  .panel {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(16, 24, 32, 0.1);
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 12px 24px rgba(16, 24, 32, 0.06);
  }
  .visual {
    border: 2px dashed rgba(16, 24, 32, 0.22);
    border-radius: 16px;
    padding: 18px;
    min-height: 210px;
    color: var(--muted);
    background: rgba(255,255,255,0.6);
  }
  .small {
    font-size: 0.76em;
    color: var(--muted);
  }
  .figure {
    text-align: center;
  }
  .figure img {
    max-width: 100%;
    max-height: 410px;
  }
  .caption {
    margin-top: 8px;
    font-size: 0.72em;
    color: var(--muted);
  }
---

![bg right:38% contain](./assets/figure-1a.png)

# Generating CAD with AI

## Internal Research Demo: Patent-To-CAD As A Worked Example

Hydraulic Involute Cam Actuator  
US Patent `8,047,094 B2`

<!--
This version is for internal technical review.
The patent example is a concrete probe of what our AI CAD workflow can and cannot currently do.
-->

---

## Why AI Changes CAD Workflows

AI expands what can happen before a human opens a traditional CAD package in earnest.

- text can become structured geometry proposals
- sketches and figures can become candidate assemblies
- constraints can be surfaced earlier in the process
- iteration cost drops enough to explore more mechanism hypotheses

<div class="panel">

For internal engineering teams, this matters less as "automation" and more as a new front-end for design exploration and model bootstrapping.

</div>

<!--
This is the opening motivation slide for a technical audience.
Talk about leverage and speed, not replacement.
-->

---

## From Idea To Editable Model

<div class="two-col">
<div class="panel">

**Traditional path**

- concept note
- whiteboard sketch
- manual CAD setup
- repeated re-interpretation of intent

</div>
<div class="panel">

**AI-assisted path**

- concept note or reference figure
- extracted parts, joints, and constraints
- generated parametric model
- rapid critique and correction loop

</div>
</div>

<!--
The point here is compression of translation cost.
AI can reduce the number of times an engineer has to restate the same idea in different representations.
-->

---

## Where The Leverage Comes From

- language is a natural interface for incomplete ideas
- figures encode mechanism hints even when dimensions are missing
- LLMs can translate between text, code, and structured representations
- parametric CAD lets critique accumulate instead of resetting the work

<div class="small">
The value is highest when the output stays editable and the intermediate states remain inspectable.
</div>

<!--
This slide bridges the broad motivation to the technical workflow.
-->

---

## Talk Structure

1. AI as an idea-to-CAD accelerator
2. The workflow under test
3. Patent-to-CAD as a worked example
4. Failure modes, lessons, and open research questions

<div class="small">
Designed for a 30-minute internal talk without Q&A.
</div>

<!--
Use this to pace the room.
-->

---

## System Question

How should an AI CAD stack handle inputs that are:

- under-specified
- mechanically constrained
- visually ambiguous
- and only partially described in text or drawings?

<div class="panel">

Patent-to-CAD is useful here because it forces parsing, latent-structure formation, and geometric verification in one test case.

</div>

<!--
Set up the technical thesis before diving into the example.
This deck is about failure modes and architecture, not market framing.
-->

---

## Why Use Patent-To-CAD As A Research Probe

<div class="two-col">
<div class="panel">

**What it stresses**

- figure parsing
- implicit part segmentation
- joint inference
- global frame consistency

</div>
<div class="panel">

**What it exposes**

- when geometry looks plausible but is mechanically wrong
- when a representation is too weak to preserve constraints
- where human feedback contributes the most signal

</div>
</div>

<!--
Use this slide to make the benchmark useful to engineers.
It is a stress test for intermediate state quality.
-->

---

## Workflow Under Test

- ingest source text and figures
- extract parts, joints, and constraints
- build an intermediate mechanism representation
- generate editable CAD
- verify geometry, motion, and contact
- iterate with human or automated feedback

<div class="small">
The example we will walk through touches each of these stages.
</div>

<!--
This is the working architecture.
The rest of the deck shows where this flow succeeded and where it needed stronger intermediate state.
-->

---

## Worked Example

Patent: `US 8,047,094 B2`  
Mechanism: hydraulic involute cam actuator

Goal:

- infer the moving parts from figure `1A`
- build a functioning `OpenSCAD` model
- preserve the intended piston-to-cam coupling

<div class="figure">
<img src="./assets/figure-1a.png" alt="Patent Figure 1A">
<div class="caption">Figure 1A: compact benchmark for translating a patent figure into a constrained mechanism.</div>
</div>

<!--
Now narrow into the case study.
Keep the example grounded and concrete.
-->

---

## What The First Pass Got Wrong

<div class="two-col">
<div class="panel">

**The model could**

- parse equations
- draw involute-inspired geometry
- produce a visually plausible cam

</div>
<div class="panel">

**But it could not yet**

- reconstruct the actual mechanism
- align all parts in a shared frame
- maintain roller-cam contact through motion

</div>
</div>

<div class="panel">

The first output was equation-driven and visually plausible, but it did not yet preserve the intended actuator-to-cam relationship.

</div>

<!--
This slide makes an important distinction between geometry generation and mechanism generation.
-->

---

## Why The Example Improved

The task got better as the AI was pushed into more structured reasoning:

- from curve generation to part decomposition
- from shape to kinematic chain
- from single representation to `OpenSCAD` + equations + `URDF`
- from static geometry to motion and contact verification

<!--
This is the central AI story.
Performance improved as the representation became more explicit and mechanistic.
-->

---

## Intermediate Representations Matter

<div class="two-col">
<div class="panel">

**Kinematic abstraction**

- base
- revolute pivot
- two prismatic piston branches
- coupled motion relation

</div>
<div class="panel">

**Robot-style description**

- `URDF` joints
- `mimic` constraints
- easy translation back into animated geometry

</div>
</div>

<div class="two-col">
<div class="figure">
<img src="./assets/figure-2a.png" alt="Patent Figure 2A">
<div class="caption">Figure 2A: one side-view state of the actuator pair and rotating body.</div>
</div>
<div class="figure">
<img src="./assets/figure-2b.png" alt="Patent Figure 2B">
<div class="caption">Figure 2B: alternate state, useful for reasoning about motion and alignment.</div>
</div>
</div>

<!--
This slide generalizes the lesson.
AI CAD systems should not jump directly from prompt to final mesh or solids.
-->

---

## The Core Technical Bottleneck

The hardest issue was not syntax, file format, or code generation.

It was **contact geometry**.

<div class="panel">

- Where is the contact point between roller and cam?
- How does that point move as the arm rotates?
- How do we keep one contact point without separation or penetration?

</div>

<!--
This is the slide that separates toy demos from engineering systems.
Contact is where many "successful" generations fail.
-->

---

## The Fix That Made It Work

<div class="two-col">
<div class="panel">

```text
Roller center must lie on the pitch curve
Cam surface is the inward offset of the pitch curve
Neutral contact depth = -r * (pi / 2)
```

Once the offset was corrected, the final model maintained contact across motion.

</div>
<div class="figure">
<img src="./assets/figure-3.png" alt="Patent Figure 3">
<div class="caption">Figure 3: the reference curve that grounded the contact calculation.</div>
</div>
</div>

<!--
Use this as the concrete example of how AI needed explicit geometric reasoning to converge.
-->

---

## What This Suggests About Our AI CAD Stack

- LLMs are useful for decomposition, translation, and iterative repair
- They need structured intermediate states to stay mechanically grounded
- Verification should target motion, contact, and constraints, not just appearance
- Human feedback is most valuable when it sharpens the physical invariants
- We should treat kinematic state as a first-class artifact, not an implicit byproduct

<!--
Tie the example back to system design principles.
-->

---

## Open Technical Questions

<div class="two-col">
<div class="panel">

**Representation**

- What is the minimal internal representation that preserves intent?
- When should the stack emit `URDF`, symbolic constraints, or parametric CAD?
- How do we encode contact assumptions explicitly?

</div>
<div class="panel">

**Evaluation**

- How do we score mechanism correctness before full simulation?
- Which user critiques are highest-value for recovery?
- How much of this loop can be automated with geometry checks?

</div>
</div>

<!--
This is the internal research slide.
Leave the audience with concrete next questions rather than generic implications.
-->

---

## Closing

Patent-to-CAD is a strong demonstration case because it shows both sides of AI-generated engineering:

- the promise: rapid translation from technical text to editable CAD
- the limit: good results require explicit reasoning about mechanism behavior

<div class="two-col">
<div class="figure">
<img src="./assets/figure-1a.png" alt="Patent Figure 1A">
<div class="caption">Source mechanism from the patent.</div>
</div>
<div class="figure">
<img src="./assets/actuator-angle.png" alt="Rendered CAD reconstruction">
<div class="caption">Rendered CAD reconstruction produced from the final OpenSCAD assembly.</div>
</div>
</div>

<!--
End on a balanced claim.
Not "AI replaces CAD engineering," but "AI accelerates it when the workflow is constraint-aware."
-->

---

## Final Takeaway

The strongest use of AI in CAD is at the boundary between **idea formation** and **formal engineering representation**.

- it helps bootstrap models faster
- it helps keep multiple representations in play
- it exposes assumptions earlier
- and it can shorten the path to a testable CAD artifact

<div class="panel">

The patent case is one example, but the broader lesson is general: AI is most useful when it helps engineers turn intent into structured, verifiable geometry.

</div>

<!--
Close on the broader thesis so the audience leaves with a reusable framing, not just one interesting example.
-->
