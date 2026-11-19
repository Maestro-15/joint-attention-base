"""Stage 2a: gaze. Who or what is each person looking at?

Two interchangeable backends, same output (gaze_dir / gaze_point / gaze_target per person):

HeadPoseGaze  Zero dependency baseline. A 2D head direction from the skeleton's head
              keypoints, cast as a ray. Works for profile views, weak when the face points
              at the camera. It exists so the whole pipeline runs end to end today.
GazeLLEGaze   Gaze-LLE (Ryan et al., CVPR 2025), frozen DINOv2 + head prompt, outputs a
              heatmap and an in/out of frame score per head. This is one of the two base
              models the AGT paper fine-tunes, so it is the natural upgrade path.

Target resolution follows the AGT paper's "fine semantic check": a predicted gaze point
that lands inside a face box counts as looking at that person, otherwise the object it
lands on.
"""
from __future__ import annotations

import math

import numpy as np

from .perception import KP_CONF, L_EAR, L_EYE, NOSE, R_EAR, R_EYE
from .types import Box, Obj, Person

Candidate = tuple[str, Box]

# Gaze or pointing that lands on something no detector named. Kept as its own value so
# "looked at something we cannot name" is not confused with "no data" (None).
UNRECOGNIZED = "unrecognized"
OUT_OF_FRAME = "out_of_frame"


def candidates_for(p: Person, persons: list[Person], objects: list[Obj]) -> list[Candidate]:
    c = [(q.key, q.face) for q in persons if q is not p and q.face is not None]
    c += [(o.key, o.box) for o in objects]
    return c


def ray_target(origin, direction, cands: list[Candidate], min_deg=12.0) -> str | None:
    """Pick the candidate the ray points at most squarely, if any is within tolerance."""
    best, best_score = None, 1.0
    for key, box in cands:
        v = box.center - origin
        dist = float(np.linalg.norm(v))
        if dist < 1e-6:
            continue
        cos = float(np.dot(v / dist, direction))
        if cos <= 0:
            continue
        ang = math.degrees(math.acos(min(1.0, cos)))
        tol = max(min_deg, math.degrees(math.atan2(0.5 * math.hypot(box.w, box.h), dist)))
        score = ang / tol
        if score < best_score:
            best, best_score = key, score
    return best


def point_target(pt, cands: list[Candidate]) -> str | None:
    hits = [(k, b) for k, b in cands if b.contains(pt)]
    if not hits:
        return None
    faces = [h for h in hits if not h[0].startswith("obj:")]
    pool = faces or hits
    return min(pool, key=lambda h: h[1].w * h[1].h)[0]


class HeadPoseGaze:
    name = "headpose"

    def __call__(self, frame, persons: list[Person], objects: list[Obj]) -> None:
        for p in persons:
            kp, f = p.keypoints, p.face
            if f is None or kp[NOSE, 2] < KP_CONF:
                continue
            ears = [kp[i, :2] for i in (L_EAR, R_EAR) if kp[i, 2] > KP_CONF]
            eyes = [kp[i, :2] for i in (L_EYE, R_EYE) if kp[i, 2] > KP_CONF]
            ref = np.mean(ears, axis=0) if ears else (np.mean(eyes, axis=0) if eyes else None)
            if ref is None:
                continue
            v = kp[NOSE, :2] - ref
            if len(ears) == 2 or (not ears and len(eyes) == 2):
                v[1] -= 0.12 * f.h          # level head: nose sits a bit below the ear/eye line
            n = float(np.linalg.norm(v))
            if n < 1e-6:
                continue
            p.gaze_origin = f.center
            p.gaze_dir = v / n
            p.gaze_conf = float(np.clip(n / (0.35 * f.w), 0, 1))
            if p.gaze_conf >= 0.3:          # low = facing the camera, target is off image
                p.gaze_target = ray_target(p.gaze_origin, p.gaze_dir, candidates_for(p, persons, objects)) or UNRECOGNIZED


class GazeLLEGaze:
    """Gaze-LLE via torch.hub (github.com/fkryan/gazelle). Downloads weights on first use."""
    name = "gazelle"

    def __init__(self, variant="gazelle_dinov2_vitb14_inout", device=None, inout_thresh=0.5):
        import torch
        self.torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.transform = torch.hub.load("fkryan/gazelle", variant, trust_repo=True)
        self.model.eval().to(self.device)
        self.inout_thresh = inout_thresh

    def __call__(self, frame, persons: list[Person], objects: list[Obj]) -> None:
        from PIL import Image
        heads = [p for p in persons if p.face is not None]
        if not heads:
            return
        h, w = frame.shape[:2]
        img = Image.fromarray(frame[:, :, ::-1])
        bboxes = [[(max(0, p.face.x1) / w, max(0, p.face.y1) / h,
                    min(w, p.face.x2) / w, min(h, p.face.y2) / h) for p in heads]]
        with self.torch.no_grad():
            out = self.model({"images": self.transform(img).unsqueeze(0).to(self.device), "bboxes": bboxes})
        for i, p in enumerate(heads):
            hm = out["heatmap"][0][i].float().cpu().numpy()
            inout = float(out["inout"][0][i]) if out.get("inout") is not None else 1.0
            y, x = np.unravel_index(hm.argmax(), hm.shape)
            pt = np.array([(x + 0.5) / hm.shape[1] * w, (y + 0.5) / hm.shape[0] * h])
            p.gaze_origin = p.face.center
            d = pt - p.gaze_origin
            p.gaze_dir = d / (np.linalg.norm(d) + 1e-6)
            p.gaze_point = pt
            p.gaze_conf = inout
            if inout >= self.inout_thresh:
                p.gaze_target = point_target(pt, candidates_for(p, persons, objects)) or UNRECOGNIZED
            else:
                p.gaze_target = OUT_OF_FRAME


def make_gaze(name: str, device=None):
    if name == "headpose":
        return HeadPoseGaze()
    if name == "gazelle":
        return GazeLLEGaze(device=device)
    raise ValueError(f"unknown gaze backend {name}")
