# How to run everything

Step by step, from a fresh clone to a live demo. Tested on Linux with an RTX 4070 laptop GPU.

## 1. What you need first

| Tool | Why | Check |
|---|---|---|
| NVIDIA GPU with a recent driver | Real time speed. CPU works but is very slow | `nvidia-smi` |
| `git` | Clone the repo and install CLIP | `git --version` |
| `uv` | Creates the Python environment | `uv --version` (install from docs.astral.sh/uv) |
| `ffmpeg` | Re encodes videos, turns frame folders into videos | `ffmpeg -version` |
| A webcam | Only for the live webcam view | `ls /dev/video*` |

## 2. One time setup

```bash
git clone https://github.com/Maestro-15/joint-attention-base.git
cd joint-attention-base/base

uv venv -p 3.12 .venv
uv pip install -p .venv/bin/python -r requirements.txt
```

Check the GPU is visible to Python. It should print `True`.

```bash
.venv/bin/python -c "import torch; print(torch.cuda.is_available())"
```

**First run downloads the models** (about 1 GB in total, once).

| Model | Size | Saved to |
|---|---|---|
| YOLO11n and YOLO11n pose | about 12 MB | `base/weights/` |
| YOLO-World v2 large | about 94 MB | `base/weights/` |
| CLIP text model (used by YOLO-World) | about 338 MB | `~/.cache/clip/` |
| Gaze LLE with DINOv2 ViT B/14 | about 350 MB | `~/.cache/torch/hub/` |

Gaze LLE loads through `torch.hub` from `github.com/fkryan/gazelle`.

**Linux only, live window fonts.** If the live window prints `QFontDatabase: Cannot find font directory`, point OpenCV at the system fonts once.

```bash
ln -sfn /usr/share/fonts .venv/lib/python3.12/site-packages/cv2/qt/fonts
```

All commands below are run from inside `base/`.

## 3. Live view (watch it work in real time)

```bash
./live.sh                     # laptop webcam
./live.sh path/to/video.mp4   # a video file, processed live
./live.sh 1                   # a different camera number
```

| Key | Action |
|---|---|
| `q` | Stop |
| `f` | Toggle fullscreen |

Options, set before the command.

```bash
WIDTH=1200 ./live.sh                      # starting window width in pixels (default 1600)
OBJECTS="cup,phone,book" ./live.sh        # what objects to look for
```

When you stop, results are saved (see section 6). Webcam runs go to `demo/output/webcam_<time>/`.

**Webcam test of Mutual and Share.** Sit next to someone, both facing the laptop, far enough back that both heads and elbows are in frame.

1. Turn and look at each other for a second. Both labels show `[Mutual]`
2. Both look at a cup or phone. Both labels show `[Share]`
3. Point at it with a straight arm. A pink arrow appears

The smaller person is labelled `child`, the larger `adult`.

## 4. Full run on a video (with chart and playable video)

```bash
./demo.sh path/to/video.mp4
./demo.sh path/to/video.mp4 OUT_DIR
./demo.sh path/to/video.mp4 OUT_DIR "toy,ball,book"   # custom object words
./demo.sh path/to/video.mp4 OUT_DIR none              # plain YOLO instead of YOLO-World
```

Runs the pipeline, draws `timeline.png`, and re encodes `annotated_h264.mp4` so it plays in any browser or slide deck. Default output is `demo/output/<video name>/`. A 12 second 720p clip takes about 40 seconds.

The demo clip used in `demo/summary.pdf` is a public domain CDC milestone video ("18 Month Milestone, Points to show someone what he wants", Wikimedia Commons). It is not in the repo. Download it and run `./demo.sh` on it to reproduce the handout.

## 5. The underlying command (all options)

`live.sh` and `demo.sh` are shortcuts for `run.py`.

```bash
.venv/bin/python run.py SOURCE --out OUT_DIR [options]
```

`SOURCE` is a video file, or a camera number (`0` is the webcam).

| Option | Meaning |
|---|---|
| `--show` | Live window while processing |
| `--show-width 1600` | Starting live window width |
| `--objects "toy,ball,book"` | Use YOLO-World with these words. Leave out for plain YOLO (80 everyday classes, misses most toys) |
| `--obj-conf 0.12` | Object confidence threshold (default 0.12 for YOLO-World, 0.35 for plain YOLO) |
| `--gaze gazelle` | Gaze LLE, the default |
| `--gaze headpose` | Fallback from head keypoints, no gaze model, much weaker |
| `--roles 3=child,1=adult` | Fix tracker ids to roles instead of the body size rule |
| `--stride 2` | Process every 2nd frame (faster, coarser) |
| `--max-frames 300` | Stop early |
| `--device cpu` | Force a device |

Draw the chart for any finished run.

```bash
.venv/bin/python plot_timeline.py OUT_DIR
```

## 6. What comes out

| File | Contents | Open with |
|---|---|---|
| `annotated.mp4` | Video with boxes, gaze arrows, pointing arrows, labels | `xdg-open`, mpv, VLC |
| `annotated_h264.mp4` | Same, re encoded to play anywhere (`demo.sh` only) | Any player or browser |
| `timeline.png` | Chart of who looked at and pointed at what, over time | Any image viewer |
| `summary.json` | Seconds of gaze per target, pointing count, label percentages | `firefox summary.json` |
| `timeline_segments.json` | The timed segments behind the chart. The input for RJA and IJA work | `firefox timeline_segments.json` |
| `timeline.jsonl` | Every frame in full, one JSON per line | `sed -n 300p timeline.jsonl \| python3 -m json.tool` |

**Reading the video**

| On screen | Means |
|---|---|
| Orange or yellow | The child |
| Blue | The adult |
| Grey | Anyone else |
| Dots on the body | Body keypoints |
| Box on the head, with `child [Share] -> obj:cup#5` | Who, their label, what they look at |
| Thin arrow from a face | Gaze. The tip is exactly where the model thinks they look |
| Green box with a word | A detected object |
| Thick pink arrow | Pointing |
| Black bar at the bottom | Live readout (live window only) |

**Target values.** A person (`child`, `adult`), an object (`obj:cup#5`, the number tells two cups apart), `unrecognized` (lands on nothing named), `out_of_frame` (looking off screen), or `null` (no face visible).

**Labels.** `Mutual` means two people look at each other. `Share` means two people look at the same thing. `Single` is anything else.

## 7. Running on research data

Research data never goes in git. Put it in `datasets/` at the repo root, which is gitignored.

If the data comes as folders of numbered frames (for example `CLIP_412.jpg` to `CLIP_554.jpg`), turn each folder into a video first. Set the frame rate to the source's real rate (30 is assumed below).

```bash
cd ../datasets
mkdir -p videos
for d in extracted/*/; do
  n=$(basename "$d")
  start=$(ls "$d" | sed 's/.*_//;s/\.jpg//' | sort -n | head -1)
  prefix=$(ls "$d" | head -1 | sed 's/_[0-9]*\.jpg$//')
  ffmpeg -v error -y -framerate 30 -start_number "$start" -i "$d/${prefix}_%d.jpg" \
         -c:v libx264 -pix_fmt yuv420p "videos/$n.mp4"
done
cd ../base
```

Then run as usual. Anything under `datasets/` is saved into `datasets/results/` automatically by `live.sh`. For `demo.sh`, pass the output folder.

```bash
./live.sh ../datasets/videos/CLIP.mp4
./demo.sh ../datasets/videos/CLIP.mp4 ../datasets/results/CLIP
```

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `cannot open video source 0` | The webcam is busy. Close the other live window (press `q`) or any app using the camera |
| Live window does not open | It runs through XWayland. Check `echo $DISPLAY` is set. `live.sh` already sets `QT_QPA_PLATFORM=xcb` |
| Live window is small | Press `f`, drag to resize, or `WIDTH=1920 ./live.sh` |
| `torch.cuda.is_available()` is `False` | Driver or CUDA build issue. Everything still runs on CPU, slowly |
| YOLO-World fails to install or load CLIP | `uv pip install -p .venv/bin/python "git+https://github.com/ultralytics/CLIP.git"` |
| Gaze LLE asks to trust the repo, or fails on first load | Needs internet once. It is loaded with `trust_repo=True` from `fkryan/gazelle` |
| Toys come out `unrecognized` | Use `--objects` with words that fit the scene, or lower `--obj-conf` |
| Child and adult labels swapped | The rule is body size. Use `--roles` with the tracker ids shown on screen |

## 9. What is not here yet

The pipeline stops at the timeline. Detecting RJA and IJA events from `timeline_segments.json` is the research layer. Nothing is trained on child data yet, every part is pretrained or a rule. Known limits are in `notes/base-pipeline.md`.
