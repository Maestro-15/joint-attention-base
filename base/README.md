# Base perception pipeline (one camera)

The base layer from the 2026-11-17 whiteboard. It turns one video into who is where, who looks at what, and who points at what, over time. It does **not** detect RJA or IJA. That is the research layer and sits on top of these outputs.

Design, decisions and test results are in `../notes/base-pipeline.md`.

```
frame
 → [1] Perception      faces, skeletons, objects, child or adult role   jabase/perception.py
 → [2a] Gaze           gaze target per person                           jabase/gaze.py
 → [2b] Gesture        arm pointing and its target                      jabase/gesture.py
 → scene graph         adjacency matrix, Single / Mutual / Share        jabase/scene_graph.py
 → [3] Temporal flow   stable segments per person                       jabase/temporal.py
```

`jabase/pipeline.py` wires the stages together and draws the video. `jabase/types.py` holds the shared data types.

## Setup

```bash
cd base
uv venv -p 3.12 .venv
uv pip install -p .venv/bin/python -r requirements.txt
```

YOLO weights download into `weights/` on first run (YOLO-World large is about 94 MB, and its CLIP text model about 338 MB caches in `~/.cache/clip`). Gaze LLE downloads through torch.hub on first run.

## Live view

```bash
./live.sh                  # laptop webcam, press q in the window to stop
./live.sh path/to/video    # watch a video being processed live
```

Shows boxes, gaze and pointing arrows, and a status bar (each person's label and target) as frames are processed, about 10 fps on the laptop GPU. Same as `run.py SOURCE --show`. Camera numbers work as the source (`0` is the webcam). If the window does not open, `QT_QPA_PLATFORM=xcb` is the setting to check (already set by the script).

## Demo, one command

```bash
./demo.sh path/to/video.mp4            # outputs to ../demo/output/<video name>
```

Runs the pipeline with YOLO-World toy words, draws `timeline.png`, and re-encodes `annotated_h264.mp4` so it plays in a browser. The meeting guide is `../demo/README.md`.

## Run

```bash
.venv/bin/python run.py path/to/video.mp4 --out path/to/output
```

| Flag | Meaning |
|---|---|
| `--gaze gazelle` | Gaze LLE, the default |
| `--gaze headpose` | Fallback ray from the head keypoints, no model, weak |
| `--roles 3=child,1=adult` | Fix track ids to roles instead of the body size rule |
| `--stride 2` | Process every 2nd frame |
| `--max-frames 300` | Stop early |
| `--device cpu` | Force a device |
| `--objects "toy,ball,book"` | Use YOLO-World with these words instead of plain YOLO's 80 classes (plain YOLO misses most toys) |
| `--obj-conf 0.12` | Object confidence threshold (default 0.12 for YOLO-World, 0.35 for plain YOLO) |

Chart a finished run with `.venv/bin/python plot_timeline.py OUT_DIR`, which writes `OUT_DIR/timeline.png`.

## Outputs

| File | Contents |
|---|---|
| `annotated.mp4` | Boxes, skeleton points, gaze arrows, pointing arrows in pink, labels |
| `timeline.jsonl` | One line per frame with persons, objects, targets and the adjacency matrix |
| `timeline_segments.json` | Per person segments for gaze target, pointing target and atomic label |
| `summary.json` | Visible percent, gaze seconds by target, pointing count, atomic label percent |

Target values. A person or `obj:<label>` when named. `unrecognized` when gaze or pointing lands on something no detector named. `out_of_frame` when Gaze LLE says the person looks off screen. `null` means no data (face not visible).
