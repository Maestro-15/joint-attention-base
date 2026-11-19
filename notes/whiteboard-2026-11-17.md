# Whiteboard, 2026-11-17

Photo is in `assets/whiteboard-2026-11-17.jpeg`.

## The pipeline on the board

```
camera frames (stacked, several cameras)
   → [Face Detection · Skeleton · Object Detection · "for all cameras?"]
   → Gaze
   → Hand / Gesture
   → [Temporal Flow]
   → (arrow down)
RJA
IJA
```

| Box | Meaning | Source of the meaning |
|---|---|---|
| Stacked frames with a stick figure looking at two squares | Video of the session, people looking at objects | Read from the board |
| Face Detection, Skeleton, Object Detection | Find faces (needed for gaze), body joints (needed for gesture), and objects (the things looked at or pointed to) | Read from the board |
| "for all cameras?" | **How** to do this across all cameras is for the team to decide | Confirmed by Lakshya. An earlier read that the professor was undecided was wrong |
| Gaze | Where each person is looking | Board, and the AGT paper |
| Hand / Gesture | What the hands do, such as pointing | Board only. Neither paper covers gesture |
| Temporal Flow | Gaze and gesture over time, not one frame | Board, and the GazeTransformer temporal module |
| RJA, IJA | Responding to and initiating joint attention | Standard autism terms. **This is the research layer, not part of the base** (Lakshya) |

## The numbered list on the board

1. **Datasets from W**. W is a person the team will ask for datasets (confirmed by Lakshya)
2. **Share papers**. Likely the two papers in `papers/`
3. **Gaze Transformer discussion**. The GazeTransformer paper, see `papers.md`
4. **2024 dataset**. Unknown which one. Not AGT, which is 2025. Ask
5. **Basic block diagram**. The pipeline above, cleaned up

## Not understood yet

- The math on the bottom left (60 over 4 squared equals 3.75, AR, K). Unknown context
- The small question mark on the arrow going into Temporal Flow

## Decisions made that day (by Lakshya)

- Leave multiple cameras out for now and assume one camera
- RJA and IJA are the research and stay out of the base
- Everything else on the board is the base
