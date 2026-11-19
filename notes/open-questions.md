# Open questions

Tick and move the answer into the right note once answered.

## For W (datasets). W is Wang (confirmed 2026-11-19)

Wang shared a first sample on 2026-11-19 (3 frame clips, no labels), see `base-pipeline.md`.

- [ ] Which datasets can they share, and under what agreement (IRB, DUA)?
- [ ] Format. Raw video, or derived data only?
- [ ] Number of cameras, fixed or moving, time synced, calibration available?
- [ ] Labels. Gaze targets, gestures, RJA and IJA events? Per camera or per session?
- [ ] Which toys appear in sessions (decides whether YOLO needs fine tuning)
- [x] Sample to test on. Wang sent 3 clips 2026-11-19
- [ ] What is the source video `1Ab4vLMMAbY` (looks like a YouTube id), its fps, and are there labels for these clips?
- [ ] Terms for storing and processing the data on a laptop

## For the professor

- [ ] Which is the "2024 dataset" on the whiteboard?
- [ ] What was the math on the bottom left of the board (60 over 4 squared equals 3.75, AR, K)?
- [ ] What does the question mark on the arrow into Temporal Flow mean?
- [ ] Gesture scope. Pointing only, or also showing, giving, reaching?
- [ ] Is there existing IRB or DUA coverage (carried over from `literature_tracking.md`)

## Decisions still open

- [ ] How to do multiple cameras, see `multi-camera.md`
- [ ] Which test video to use until W's data arrives

## From the novelty check (2026-11-17)

- [ ] Professor aware of Kosmydel 2026 (dual camera, Gaze LLE, joint attention)? Use it as a baseline?
- [ ] Which novelty angle to pursue, see `novelty-check.md`
- [x] Download and read Kosmydel 2026 and Ko 2023 in full (done 2026-11-17, see `papers.md`)
