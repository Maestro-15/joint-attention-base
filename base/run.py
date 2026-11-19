"""Run the base perception pipeline on one video.

  .venv/bin/python run.py VIDEO --out results/name [--gaze gazelle|headpose] [--roles 1=child,2=adult] [--objects toy,ball,book]
"""
import argparse
import json

from jabase.pipeline import run


def parse_roles(s):
    if not s:
        return None
    return {int(k): v for k, v in (pair.split("=") for pair in s.split(","))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="video file, or a camera number like 0 for the webcam")
    ap.add_argument("--out", default="results/run")
    ap.add_argument("--gaze", default="gazelle", choices=["headpose", "gazelle"])
    ap.add_argument("--roles", help="fix track ids to roles, e.g. 1=child,2=adult")
    ap.add_argument("--device", default=None)
    ap.add_argument("--max-frames", type=int, default=None)
    ap.add_argument("--stride", type=int, default=1, help="process every Nth frame")
    ap.add_argument("--objects", help="comma list for YOLO-World, e.g. toy,ball,book. Omit for plain YOLO")
    ap.add_argument("--show", action="store_true", help="live window while processing, q to stop, f fullscreen")
    ap.add_argument("--show-width", type=int, default=1600, help="starting width of the live window in pixels")
    ap.add_argument("--obj-conf", type=float, default=None, help="object confidence threshold")
    a = ap.parse_args()
    objects = [o.strip() for o in a.objects.split(",")] if a.objects else None
    video = int(a.video) if a.video.isdigit() else a.video
    summary, timeline = run(video, a.out, a.gaze, parse_roles(a.roles), a.device, a.max_frames, a.stride,
                            objects, a.obj_conf, a.show, a.show_width)
    print(json.dumps(summary, indent=2))
    print(f"outputs in {a.out}")
