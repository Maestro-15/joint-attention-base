"""Shared data types for the joint attention base pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Box:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def center(self) -> np.ndarray:
        return np.array([(self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2])

    @property
    def w(self) -> float:
        return self.x2 - self.x1

    @property
    def h(self) -> float:
        return self.y2 - self.y1

    def contains(self, p) -> bool:
        return self.x1 <= p[0] <= self.x2 and self.y1 <= p[1] <= self.y2

    def as_list(self) -> list[float]:
        return [round(float(v), 1) for v in (self.x1, self.y1, self.x2, self.y2)]


@dataclass
class Person:
    track_id: int
    box: Box
    keypoints: np.ndarray            # (17, 3) COCO order: x, y, conf
    face: Box | None = None
    role: str = "other"              # child | adult | other

    # filled by the gaze stage
    gaze_origin: np.ndarray | None = None
    gaze_dir: np.ndarray | None = None      # unit 2D vector in image space
    gaze_point: np.ndarray | None = None    # pixel, only from heatmap backends
    gaze_conf: float = 0.0
    gaze_target: str | None = None          # node key, e.g. "adult" or "obj:cup"

    # filled by the gesture stage
    pointing: bool = False
    point_origin: np.ndarray | None = None
    point_dir: np.ndarray | None = None
    point_target: str | None = None

    @property
    def key(self) -> str:
        return self.role if self.role != "other" else f"person{self.track_id}"


@dataclass
class Obj:
    track_id: int
    label: str
    box: Box
    conf: float

    @property
    def key(self) -> str:
        # Track id keeps two objects with the same label apart (obj:cup#3 vs obj:cup#7),
        # and stays the same for one object across frames while the tracker holds it.
        return f"obj:{self.label}#{self.track_id}"


@dataclass
class FrameState:
    """Everything known about one moment, for one camera or fused across cameras."""
    frame_idx: int
    t: float
    camera: str
    persons: list[Person] = field(default_factory=list)
    objects: list[Obj] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    adjacency: np.ndarray | None = None      # A[i, j] = 1 if node i looks at node j
    atomic: dict[str, str] = field(default_factory=dict)   # person key -> Single/Mutual/Share

    def person(self, role: str) -> Person | None:
        return next((p for p in self.persons if p.role == role), None)

    def to_json(self) -> dict:
        return {
            "frame": self.frame_idx,
            "t": round(self.t, 3),
            "camera": self.camera,
            "persons": [
                {
                    "key": p.key,
                    "box": p.box.as_list(),
                    "face": p.face.as_list() if p.face else None,
                    "gaze_target": p.gaze_target,
                    "gaze_conf": round(float(p.gaze_conf), 2),
                    "pointing": p.pointing,
                    "point_target": p.point_target,
                    "atomic": self.atomic.get(p.key),
                }
                for p in self.persons
            ],
            "objects": [{"key": o.key, "box": o.box.as_list(), "conf": round(float(o.conf), 2)} for o in self.objects],
            "nodes": self.nodes,
            "adjacency": self.adjacency.astype(int).tolist() if self.adjacency is not None else None,
        }
