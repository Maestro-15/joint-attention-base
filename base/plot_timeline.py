"""Draw timeline_segments.json as a chart: one row per person per stream, coloured by target.

  .venv/bin/python plot_timeline.py OUT_DIR [--min-visible 20] [--title "..."]

Reads OUT_DIR/timeline_segments.json and OUT_DIR/summary.json, writes OUT_DIR/timeline.png.
Purely descriptive (who looked at or pointed at what, when). No RJA or IJA interpretation.
"""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FIXED = {"unrecognized": "#b0b0b0", "out_of_frame": "#e0e0e0",
         "child": "#f5a623", "adult": "#2f6fd6", "Mutual": "#d64545", "Share": "#2e9e5b", "Single": "#cfd8e3"}
PALETTE = ["#8e5bd6", "#13a3a3", "#c2569b", "#7a8f1f", "#b5651d", "#4b6584"]
STREAMS = [("gaze_target", "looks at"), ("point_target", "points at"), ("atomic", "label")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--min-visible", type=float, default=20, help="hide people seen in less than this % of frames")
    ap.add_argument("--title", default="Who looks at and points at what, over time")
    a = ap.parse_args()
    out = Path(a.out_dir)
    tl = json.loads((out / "timeline_segments.json").read_text())
    summ = json.loads((out / "summary.json").read_text())
    people = [k for k in tl if summ["persons"].get(k, {}).get("visible_pct", 0) >= a.min_visible]
    people.sort(key=lambda k: {"child": 0, "adult": 1}.get(k, 2))

    colors, extra = dict(FIXED), iter(PALETTE)
    rows = []
    for k in people:
        for stream, verb in STREAMS:
            rows.append((f"{k} {verb}", tl[k][stream]))
            for seg in tl[k][stream]:
                if seg["target"] not in colors:
                    colors[seg["target"]] = next(extra, "#555555")

    fig, ax = plt.subplots(figsize=(11, 0.55 * len(rows) + 1.6))
    for i, (_, segs) in enumerate(rows):
        y = len(rows) - 1 - i
        for seg in segs:
            ax.barh(y, seg["t_end"] - seg["t_start"], left=seg["t_start"], height=0.7,
                    color=colors[seg["target"]], edgecolor="white")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)])
    ax.set_xlim(0, summ["duration_s"])
    ax.set_xlabel("seconds")
    ax.set_title(a.title)
    used = {seg["target"] for _, segs in rows for seg in segs}
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[t]) for t in colors if t in used]
    ax.legend(handles, [t for t in colors if t in used], loc="upper center",
              bbox_to_anchor=(0.5, -0.18), ncol=min(6, len(handles)), frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "timeline.png", dpi=150)
    print(out / "timeline.png")


if __name__ == "__main__":
    main()
