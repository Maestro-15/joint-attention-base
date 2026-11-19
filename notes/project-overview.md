# Project overview

## Goal

Build AI that detects and helps diagnose autism in young children from video, by measuring **joint attention** through gaze and gesture.

Joint attention is when a child and a partner share focus on the same object. It has two halves.

| Term | Meaning | Example |
|---|---|---|
| **RJA**, responding to joint attention | the partner starts it, the child follows | adult points at a ball, child looks at the ball |
| **IJA**, initiating joint attention | the child starts it | child looks at a toy, then at the adult, then back at the toy |

Trouble with joint attention is one of the earliest observable signs of autism. Assessing it by hand needs trained clinicians and does not scale, which is the gap this project targets.

## Who

- **Lakshya**, UMN CS student, does the work
- **The professor** (UMN) runs the project and sets the tasks. Whiteboard sessions define the pipeline
- **W** is the person the team will ask for datasets (named on the 2026-11-17 whiteboard)

## Two layers

1. **Base** (built, in `base/`). Everything up to a timeline of who looks at and points at what. Detection, gaze, gesture, scene graph, temporal smoothing.
2. **Research** (not built, owned by Lakshya). RJA and IJA detection on top of the base outputs. Do not build this unless he asks.

## Timeline

| Date | What happened |
|---|---|
| 2026-10-26 | Joined. Professor's first three tasks (datasets, presentations, 2025 and 2026 autism gaze papers) done. See `literature_tracking.md` and `professor_email_draft.md` |
| 2026-11-17 | Whiteboard session defined the pipeline. Base pipeline built for one camera. See `session-log.md` |

## Current state

- Base runs start to finish on one video, with Gaze LLE as the gaze model
- Tested only on a sample photo of two adults, not on a real child session
- No training done yet. Every model is pretrained or a hand written rule. See `training-plan.md`
- Waiting on data from W
