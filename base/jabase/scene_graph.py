"""Per frame social graph, following GazeTransformer (de Belen et al., NeurIPS 2023 GMML).

Nodes are people and objects. A[i, j] = 1 when node i looks at node j (diagonal is 0).
Atomic labels per person come straight out of the matrix:

  Mutual  A[i, j] = A[j, i] = 1 for some person j
  Share   A[i, j] = 1 and column j has more than one 1 (two people on the same target)
  Single  anything else

These three are the paper's (M)VACATION labels. Avert/Refer/Follow are deliberately left to
the temporal stage, because the paper's point is that they need time, not one frame.
"""
from __future__ import annotations

import numpy as np

from .types import FrameState


def build_graph(state: FrameState) -> None:
    nodes = [p.key for p in state.persons]
    nodes += [o.key for o in state.objects if o.key not in nodes]
    idx = {k: i for i, k in enumerate(nodes)}
    A = np.zeros((len(nodes), len(nodes)), dtype=np.uint8)
    for p in state.persons:
        if p.gaze_target in idx and idx[p.gaze_target] != idx[p.key]:
            A[idx[p.key], idx[p.gaze_target]] = 1
    state.nodes, state.adjacency = nodes, A

    for p in state.persons:
        i = idx[p.key]
        label = "Single"
        for j in np.flatnonzero(A[i]):
            if A[j, i]:
                label = "Mutual"
                break
            if A[:, j].sum() > 1:
                label = "Share"
        state.atomic[p.key] = label
