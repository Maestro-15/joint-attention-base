#!/usr/bin/env bash
# One command demo. Runs the full base pipeline on a video, draws the timeline chart, and
# re-encodes the annotated video to H.264 so it plays in any browser or slide deck.
#
#   ./demo.sh VIDEO [OUT_DIR] [OBJECT_WORDS]
#
#   OUT_DIR       default ../demo/output/<video name>
#   OBJECT_WORDS  comma list for YOLO-World, default "toy,ball,book,doll,stuffed animal,cup,picture"
#                 pass "none" to use plain YOLO (80 everyday classes, misses most toys)
set -euo pipefail
cd "$(dirname "$0")"

VIDEO="${1:?usage: ./demo.sh VIDEO [OUT_DIR] [OBJECT_WORDS]}"
NAME="$(basename "${VIDEO%.*}")"
OUT="${2:-../demo/output/$NAME}"
WORDS="${3:-toy,ball,book,doll,stuffed animal,cup,picture}"

OBJ_ARGS=()
[[ "$WORDS" != "none" ]] && OBJ_ARGS=(--objects "$WORDS")

echo "== 1/3 pipeline (perception, gaze, pointing, scene graph, timeline)"
start=$(date +%s)
mkdir -p "$OUT"
if ! .venv/bin/python run.py "$VIDEO" --out "$OUT" "${OBJ_ARGS[@]}" >"$OUT/run.log" 2>&1; then
  echo "pipeline failed, last lines of $OUT/run.log:"; tail -20 "$OUT/run.log"; exit 1
fi
echo "   done in $(( $(date +%s) - start ))s"

echo "== 2/3 timeline chart"
.venv/bin/python plot_timeline.py "$OUT" >/dev/null

echo "== 3/3 browser friendly video"
ffmpeg -v error -y -i "$OUT/annotated.mp4" -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$OUT/annotated_h264.mp4"

echo
echo "Outputs in $OUT"
echo "  annotated_h264.mp4      the video with boxes, gaze arrows, pointing arrows, labels"
echo "  timeline.png            who looked at and pointed at what, over time"
echo "  summary.json            seconds of gaze per target, pointing count, label percentages"
echo "  timeline_segments.json  the segments behind the chart"
echo "  timeline.jsonl          every frame in full"
