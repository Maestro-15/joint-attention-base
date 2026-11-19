"""Ties the stages together for one camera and draws an annotated video."""
from __future__ import annotations

import json
import time
from pathlib import Path

import cv2

from .gaze import make_gaze
from .gesture import PointingDetector
from .perception import Perception
from .scene_graph import build_graph
from .temporal import build_timeline, summarize
from .types import FrameState

WIN = "joint attention base  (q = stop, f = fullscreen)"
COLORS = {"child": (0, 200, 255), "adult": (255, 120, 0), "other": (160, 160, 160)}


def draw(frame, s: FrameState):
    for o in s.objects:
        b = o.box
        cv2.rectangle(frame, (int(b.x1), int(b.y1)), (int(b.x2), int(b.y2)), (0, 220, 0), 2)
        cv2.putText(frame, o.label, (int(b.x1), int(b.y1) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 0), 1)
    for p in s.persons:
        c = COLORS.get(p.role, COLORS["other"])
        for x, y, conf in p.keypoints:
            if conf > 0.35:
                cv2.circle(frame, (int(x), int(y)), 3, c, -1)
        if p.face:
            f = p.face
            cv2.rectangle(frame, (int(f.x1), int(f.y1)), (int(f.x2), int(f.y2)), c, 2)
            label = f"{p.key} [{s.atomic.get(p.key, '')}] -> {p.gaze_target or '?'}"
            cv2.putText(frame, label, (int(f.x1), int(f.y1) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, 2)
        if p.gaze_dir is not None:
            end = p.gaze_point if p.gaze_point is not None else p.gaze_origin + p.gaze_dir * 250
            cv2.arrowedLine(frame, tuple(p.gaze_origin.astype(int)), tuple(end.astype(int)), c, 2, tipLength=0.05)
        if p.pointing:
            end = p.point_origin + p.point_dir * 150
            cv2.arrowedLine(frame, tuple(p.point_origin.astype(int)), tuple(end.astype(int)), (255, 0, 255), 3)
    return frame


def hud(frame, s: FrameState, fps_now: float):
    """Small status bar for the live window: time, speed, and each person's label and target."""
    parts = [f"t={s.t:5.1f}s  {fps_now:4.1f} fps"]
    for p in s.persons:
        if p.role in ("child", "adult"):
            pt = f" POINT->{p.point_target}" if p.pointing else ""
            parts.append(f"{p.key}: {s.atomic.get(p.key, '')} -> {p.gaze_target or '?'}{pt}")
    text = "   |   ".join(parts)
    cv2.rectangle(frame, (0, frame.shape[0] - 30), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
    cv2.putText(frame, text, (8, frame.shape[0] - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    return frame


def run(video, out_dir: str, gaze="gazelle", roles=None, device=None, max_frames=None, stride=1,
        objects=None, obj_conf=None, show=False, show_width=1600):
    """video is a file path, or an int camera index (0 = laptop webcam).
    show=True opens a live window with the annotations; q stops, f toggles fullscreen."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    live_source = isinstance(video, int)
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        raise FileNotFoundError(f"cannot open video source {video}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    perceive = Perception(roles=roles, device=device, objects=objects, obj_conf=obj_conf)
    gaze_model = make_gaze(gaze, device=device)
    gesture = PointingDetector()

    states, writer = [], None
    idx, t0, last = 0, time.monotonic(), time.monotonic()
    fps_now = 0.0
    window_open = False
    while True:
        ok, frame = cap.read()
        if not ok or (max_frames and len(states) >= max_frames):
            break
        if idx % stride == 0:
            t = time.monotonic() - t0 if live_source else idx / fps   # webcam uses wall clock
            persons, objects = perceive(frame)                 # stage 1
            gaze_model(frame, persons, objects)                # stage 2a
            gesture(frame, persons, objects)                   # stage 2b
            s = FrameState(idx, t, "cam0", persons, objects)
            build_graph(s)                                     # per frame graph
            states.append(s)

            drawn = draw(frame, s)
            if writer is None:
                h, w = drawn.shape[:2]
                out_fps = 10.0 if live_source else fps / stride
                writer = cv2.VideoWriter(str(out / "annotated.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), out_fps, (w, h))
            writer.write(drawn)
            if show:
                now = time.monotonic()
                fps_now = 0.8 * fps_now + 0.2 / max(now - last, 1e-6)
                last = now
                if not window_open:
                    # Resizable window, opened at show_width pixels wide (drag to resize, f = fullscreen)
                    cv2.namedWindow(WIN, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                    h, w = drawn.shape[:2]
                    cv2.resizeWindow(WIN, show_width, int(show_width * h / w))
                    window_open = True
                cv2.imshow(WIN, hud(drawn.copy(), s, fps_now))
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                if key == ord("f"):
                    full = cv2.getWindowProperty(WIN, cv2.WND_PROP_FULLSCREEN) == cv2.WINDOW_FULLSCREEN
                    cv2.setWindowProperty(WIN, cv2.WND_PROP_FULLSCREEN,
                                          cv2.WINDOW_NORMAL if full else cv2.WINDOW_FULLSCREEN)
        idx += 1
    cap.release()
    if writer is not None:
        writer.release()
    if show:
        cv2.destroyAllWindows()

    timeline = build_timeline(states)                          # stage 3
    summary = summarize(states, timeline)

    with open(out / "timeline.jsonl", "w") as f:
        for s in states:
            f.write(json.dumps(s.to_json()) + "\n")
    (out / "timeline_segments.json").write_text(json.dumps(timeline, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary, timeline
