"""Stage 1 (per camera): object detection, skeleton, face detection.

Objects  : YOLO detector (COCO classes, people excluded since the pose model owns them)
Skeleton : YOLO pose model, 17 COCO keypoints per person, tracked across frames
Face     : derived from the head keypoints (nose, eyes, ears), so every face is already
           attached to a skeleton and a track id. Swap for a dedicated face detector later
           if small or turned away faces get missed.
Roles    : child vs adult. Placeholder heuristic, see RoleAssigner.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
from ultralytics import YOLO

from .types import Box, Obj, Person

NOSE, L_EYE, R_EYE, L_EAR, R_EAR = 0, 1, 2, 3, 4
L_SHO, R_SHO = 5, 6
KP_CONF = 0.35
WEIGHTS = Path(__file__).resolve().parent.parent / "weights"


def face_from_keypoints(kp: np.ndarray, body: Box) -> Box | None:
    head = kp[[NOSE, L_EYE, R_EYE, L_EAR, R_EAR]]
    vis = head[head[:, 2] > KP_CONF]
    if len(vis) < 2:
        return None
    c = vis[:, :2].mean(axis=0)
    spread = np.ptp(vis[:, 0]) if len(vis) > 1 else 0
    sho = kp[[L_SHO, R_SHO]]
    sho_w = abs(sho[0, 0] - sho[1, 0]) if (sho[:, 2] > KP_CONF).all() else 0
    s = max(spread * 1.8, sho_w * 0.6, body.h * 0.10, 12)
    return Box(c[0] - s / 2, c[1] - s / 2, c[0] + s / 2, c[1] + s / 2)


class RoleAssigner:
    """Labels tracks as child / adult.

    Default heuristic: the track with the smallest median body height is the child, the
    tallest remaining track is the adult. Good enough for one child + one examiner on a
    play mat; breaks if the adult sits on the floor. Override with fixed track ids.
    """

    def __init__(self, fixed: dict[int, str] | None = None):
        self.fixed = fixed or {}
        self.heights: dict[int, list[float]] = defaultdict(list)

    def __call__(self, persons: list[Person]) -> None:
        for p in persons:
            self.heights[p.track_id].append(p.box.h)
        if self.fixed:
            for p in persons:
                p.role = self.fixed.get(p.track_id, "other")
            return
        if not persons:
            return
        med = {p.track_id: float(np.median(self.heights[p.track_id][-90:])) for p in persons}
        ordered = sorted(persons, key=lambda p: med[p.track_id])
        ordered[0].role = "child"
        if len(ordered) > 1:
            ordered[-1].role = "adult"


class Perception:
    def __init__(self, det_weights=WEIGHTS / "yolo11n.pt", pose_weights=WEIGHTS / "yolo11n-pose.pt",
                 obj_conf=None, ignore_labels=("person", "chair", "couch", "bed", "dining table", "tv"),
                 roles: dict[int, str] | None = None, device=None, objects: list[str] | None = None,
                 world_weights=WEIGHTS / "yolov8l-worldv2.pt"):
        """objects=None uses plain YOLO (80 COCO classes, misses most toys).
        objects=["toy", "ball", ...] uses YOLO-World, an open vocabulary detector that finds
        whatever words it is given, with no training. Its scores run lower, so its default
        confidence threshold is lower too."""
        if objects:
            from ultralytics import YOLOWorld
            self.det = YOLOWorld(world_weights)
            self.det.set_classes(list(objects))
            self.obj_conf = obj_conf if obj_conf is not None else 0.12
        else:
            self.det = YOLO(det_weights)
            self.obj_conf = obj_conf if obj_conf is not None else 0.35
        self.pose = YOLO(pose_weights)
        self.ignore = set(ignore_labels)
        self.roles = RoleAssigner(roles)
        self.device = device

    def __call__(self, frame) -> tuple[list[Person], list[Obj]]:
        kw = dict(persist=True, verbose=False, device=self.device)
        pr = self.pose.track(frame, **kw)[0]
        persons: list[Person] = []
        if pr.boxes is not None and pr.keypoints is not None:
            ids = pr.boxes.id.int().tolist() if pr.boxes.id is not None else list(range(len(pr.boxes)))
            for tid, xyxy, kp in zip(ids, pr.boxes.xyxy.cpu().numpy(), pr.keypoints.data.cpu().numpy()):
                body = Box(*xyxy)
                persons.append(Person(track_id=tid, box=body, keypoints=kp, face=face_from_keypoints(kp, body)))
        self.roles(persons)

        dr = self.det.track(frame, conf=self.obj_conf, **kw)[0]
        objects: list[Obj] = []
        if dr.boxes is not None:
            ids = dr.boxes.id.int().tolist() if dr.boxes.id is not None else list(range(len(dr.boxes)))
            for tid, xyxy, cls, conf in zip(ids, dr.boxes.xyxy.cpu().numpy(),
                                            dr.boxes.cls.int().tolist(), dr.boxes.conf.tolist()):
                label = dr.names[cls]
                if label not in self.ignore:
                    objects.append(Obj(track_id=tid, label=label, box=Box(*xyxy), conf=conf))
        return persons, objects
