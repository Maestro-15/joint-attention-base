"""Stage 2b: hand / gesture. Is anyone pointing, and at what?

Pointing from the arm skeleton: the arm is nearly straight, extended away from the body,
and not hanging down. The ray runs elbow -> wrist and is resolved against objects and faces
with the same ray caster as gaze.

Limits, on purpose for a base: body keypoints stop at the wrist, so this sees arm pointing,
not index finger pointing, and it cannot see showing or giving. A hand landmark model
(e.g. MediaPipe Hands, 21 points) is the next step for finger level gestures.
"""
from __future__ import annotations

import math

import numpy as np

from .gaze import UNRECOGNIZED, candidates_for, ray_target
from .perception import KP_CONF
from .types import Obj, Person

ARMS = ((5, 7, 9), (6, 8, 10))   # (shoulder, elbow, wrist) left, right


def _angle(a, b, c) -> float:
    u, v = a - b, c - b
    cos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-6)
    return math.degrees(math.acos(np.clip(cos, -1, 1)))


class PointingDetector:
    def __init__(self, min_elbow_deg=145.0, min_from_down_deg=40.0, min_extension=0.75):
        self.min_elbow = min_elbow_deg
        self.min_from_down = min_from_down_deg
        self.min_ext = min_extension

    def __call__(self, frame, persons: list[Person], objects: list[Obj]) -> None:
        for p in persons:
            kp = p.keypoints
            best = None
            for s, e, w in ARMS:
                if min(kp[s, 2], kp[e, 2], kp[w, 2]) < KP_CONF:
                    continue
                S, E, W = kp[s, :2], kp[e, :2], kp[w, :2]
                arm_len = np.linalg.norm(E - S) + np.linalg.norm(W - E)
                if arm_len < 1e-6 or _angle(S, E, W) < self.min_elbow:
                    continue
                if np.linalg.norm(W - S) / arm_len < self.min_ext:
                    continue
                d = (W - S) / np.linalg.norm(W - S)
                from_down = math.degrees(math.acos(np.clip(d[1], -1, 1)))  # image y grows downward
                if from_down < self.min_from_down:
                    continue
                if best is None or from_down > best[0]:
                    best = (from_down, W, (W - E) / (np.linalg.norm(W - E) + 1e-6))
            if best:
                p.pointing = True
                p.point_origin, p.point_dir = best[1], best[2]
                p.point_target = ray_target(p.point_origin, p.point_dir, candidates_for(p, persons, objects)) or UNRECOGNIZED
