# Joint attention base pipeline

Research code for measuring joint attention (gaze and gesture) in video of young children, as groundwork for AI assisted autism assessment. UMN research project.

This repo is the **base layer**. It turns one camera's video into a timeline of who is looking at and pointing at what, with per frame Single, Mutual and Share labels. Detecting RJA and IJA events on top of that timeline is the research layer and is not in here yet.

```
video → people, body points, objects → gaze → pointing → who looks at whom → timed segments
```

## Layout

| Path | What |
|---|---|
| `RUNNING.md` | How to set up and run everything |
| `base/` | The pipeline code. Code level details in `base/README.md` |
| `demo/` | Demo handout (`summary.pdf`) and meeting guide |
| `notes/` | Project overview, pipeline design and test results, paper summaries, open questions, training plan |
| `papers/` | Papers the design draws on |
| `literature_tracking.md` | Literature and dataset review |

## Quick start

Full instructions for every command, outputs and troubleshooting are in **[RUNNING.md](RUNNING.md)**.

```bash
cd base
uv venv -p 3.12 .venv
uv pip install -p .venv/bin/python -r requirements.txt
./live.sh                    # live view from the webcam, q to stop, f for fullscreen
./demo.sh path/to/video.mp4  # full run plus timeline chart
```

Needs an NVIDIA GPU for real time speed (tested on an RTX 4070 laptop). Model weights download on first run.

## Data

No research data is stored in this repo. Put datasets in `datasets/` at the repo root, which is gitignored. Never commit child video or frames.
