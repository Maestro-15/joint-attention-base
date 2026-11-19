#!/usr/bin/env bash
# Live view. Opens a window that shows boxes, gaze arrows, pointing arrows and labels as each
# frame is processed. Press q in the window to stop. Outputs are still saved afterwards.
#
#   ./live.sh                 laptop webcam
#   ./live.sh VIDEO           a video file
#   ./live.sh 1               another camera number
#
# OBJECTS env var changes the object words, e.g. OBJECTS="cup,phone,book" ./live.sh
# WIDTH env var sets the starting window width, e.g. WIDTH=1200 ./live.sh
set -euo pipefail
cd "$(dirname "$0")"

SRC="${1:-0}"
if [[ "$SRC" =~ ^[0-9]+$ ]]; then NAME="webcam_$(date +%H%M%S)"; else NAME="$(basename "${SRC%.*}")_live"; fi
# Research data stays inside datasets/ (gitignored). Everything else goes to demo/output/.
if [[ "$SRC" == *datasets/* ]]; then OUT="../datasets/results/$NAME"; else OUT="../demo/output/$NAME"; fi
WORDS="${OBJECTS:-toy,ball,book,doll,stuffed animal,cup,phone,bottle,picture}"

export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-xcb}"   # OpenCV's Qt window runs through XWayland here

echo "Loading models (about 10 s)... the window opens on the first frame. Press q to stop, f for fullscreen."
.venv/bin/python run.py "$SRC" --out "$OUT" --show --show-width "${WIDTH:-1600}" --objects "$WORDS" 2>&1 \
  | grep -v -i -E "warn|^\s*$" | grep -v '^[{} ]' || true
.venv/bin/python plot_timeline.py "$OUT" >/dev/null 2>&1 || true
echo "Saved to $OUT (annotated.mp4, timeline.png, summary.json)"
