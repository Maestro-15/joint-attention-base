"""Stage 3: temporal flow. Turns per frame outputs into a timeline of segments.

Per frame gaze and pointing are noisy (a target can flicker for one frame), so each
person's stream is collapsed into stable segments: "child looked at obj:cup from 2.1s to
4.0s". A segment only survives if it holds for `min_hold` seconds.

This is the base layer only. It does NOT interpret the segments (no RJA / IJA or any other
behaviour rules). That interpretation is the research and sits on top of this output.
"""
from __future__ import annotations

from collections import defaultdict

from .types import FrameState

STREAMS = ("gaze_target", "point_target")


def smooth(values: list[tuple[float, str | None]], min_hold: float) -> list[dict]:
    """Collapse a per frame stream into segments, dropping blips shorter than min_hold."""
    segs: list[list] = []
    for t, v in values:
        if segs and segs[-1][2] == v:
            segs[-1][1] = t
        else:
            segs.append([t, t, v])
    stable = [s for s in segs if s[1] - s[0] >= min_hold]
    merged: list[list] = []
    for s in stable:
        if merged and merged[-1][2] == s[2]:
            merged[-1][1] = s[1]
        else:
            merged.append(list(s))
    return [{"t_start": round(a, 2), "t_end": round(b, 2), "target": v} for a, b, v in merged if v is not None]


def build_timeline(states: list[FrameState], min_hold=0.3) -> dict:
    """{person_key: {"gaze_target": [segments], "point_target": [segments], "atomic": [segments]}}"""
    keys = sorted({p.key for s in states for p in s.persons})
    timeline = {}
    for k in keys:
        per = {}
        for attr in STREAMS:
            vals = []
            for s in states:
                p = next((q for q in s.persons if q.key == k), None)
                vals.append((s.t, getattr(p, attr) if p else None))
            per[attr] = smooth(vals, min_hold)
        per["atomic"] = smooth([(s.t, s.atomic.get(k)) for s in states], min_hold)
        timeline[k] = per
    return timeline


def summarize(states: list[FrameState], timeline: dict) -> dict:
    """Plain descriptive stats, no behavioural interpretation."""
    n = max(1, len(states))
    out = {"duration_s": round(states[-1].t, 2) if states else 0, "frames": len(states), "persons": {}}
    for k, per in timeline.items():
        visible = sum(any(p.key == k for p in s.persons) for s in states)
        gaze_time = defaultdict(float)
        for seg in per["gaze_target"]:
            gaze_time[seg["target"]] += seg["t_end"] - seg["t_start"]
        atomic = defaultdict(int)
        for s in states:
            if k in s.atomic:
                atomic[s.atomic[k]] += 1
        out["persons"][k] = {
            "visible_pct": round(100 * visible / n, 1),
            "gaze_seconds_by_target": {t: round(v, 2) for t, v in sorted(gaze_time.items(), key=lambda x: -x[1])},
            "pointing_segments": len(per["point_target"]),
            "atomic_pct": {a: round(100 * c / n, 1) for a, c in atomic.items()},
        }
    return out
