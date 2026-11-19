# Base pipeline

Code is in `base/`. How to run it is in `base/README.md`.

## Flow, one camera

```
frame
 → [1] Perception      faces, 17 point skeletons with track ids, objects, child or adult role
 → [2a] Gaze           each person's gaze target, a face or an object
 → [2b] Gesture        arm pointing and its target
 → scene graph         A[i,j] = 1 when i looks at j, labels Single, Mutual, Share
 → [3] Temporal flow   stable segments per person, short flickers removed
 → outputs             annotated.mp4, timeline.jsonl, timeline_segments.json, summary.json
```

## Each component

| Component | File | How it works | Origin |
|---|---|---|---|
| Objects | `jabase/perception.py` | YOLO11n detector, pretrained on COCO (80 everyday classes). People and furniture are ignored | Our choice |
| Skeleton | `jabase/perception.py` | YOLO11n pose, 17 COCO keypoints, ByteTrack ids so a person keeps an id across frames | Our choice |
| Face | `jabase/perception.py` | A square box built from the head keypoints (nose, eyes, ears). No separate face model | Our choice |
| Role | `jabase/perception.py` | Smallest median body height is the child, tallest is the adult. Placeholder. Override with `--roles` | Our choice |
| Gaze, default | `jabase/gaze.py` `GazeLLEGaze` | Gaze LLE (`gazelle_dinov2_vitb14_inout`) via torch.hub. Gives a heatmap and an in frame score per head. Heatmap peak inside a face box means looking at that person, otherwise the object it lands on | Gaze LLE is a base model in AGT. The face box check is AGT's fine semantic check |
| Gaze, fallback | `jabase/gaze.py` `HeadPoseGaze` | A ray from the ear midpoint through the nose. No model. Fails when the face points at the camera | Our choice |
| Gesture | `jabase/gesture.py` | Arm counts as pointing when the elbow is straight (145 degrees or more), the arm is extended, and it is not hanging down. Ray from elbow through wrist | Our choice |
| Scene graph | `jabase/scene_graph.py` | Adjacency matrix per frame. Mutual when two people look at each other, Share when two look at the same target, otherwise Single | GazeTransformer, section 4.2 |
| Temporal flow | `jabase/temporal.py` | A target counts only once held 0.3 s. Output is segments per person for gaze, pointing and atomic label, plus stats. No behaviour rules | Our choice |

## Decisions

- **No RJA or IJA logic.** A first draft had rule based RJA and IJA detection. Lakshya removed it on 2026-11-17 because that is his research
- **One camera.** Multi camera parked, see `multi-camera.md`
- **Gaze LLE as default gaze.** The head pose version was visibly wrong in testing. Lakshya approved running Gaze LLE code from GitHub on 2026-11-17
- **Objects keyed by class name** (`obj:cup`), so the same key can later match across cameras. Cost is that two cups count as one target

## Test results, 2026-11-17

Only test so far is the YOLO sample image `zidane.jpg` (two adult men) repeated as a 20 frame video.

| Check | Head pose gaze | Gaze LLE |
|---|---|---|
| Right man looking at left man | Wrong, arrow pointed up and away | Correct, target `child` (the left man got the child role) |
| Left man looking off frame | Arrow drawn, no target | In frame score 0.17, correctly treated as off frame |
| Pointing by left man | Detected | Detected |
| Roles | Both adults, so child and adult labels are meaningless here | Same |

## Test results, 2026-11-18, first real video

Clip is the CDC 18 month milestone "Points to show someone what he wants" (12 s, public domain, edited montage with cuts). Full write up and the meeting guide are in `../demo/README.md`.

- First run exposed two bugs, both fixed. Pointing with no named target was dropped (144 pointing frames, 0 in the summary), and gaze landing on nothing named was stored as null, same as no data. Both now record `unrecognized`, and Gaze LLE off screen records `out_of_frame`
- Plain YOLO11n could not see the toy truck at any confidence. Added YOLO-World v2 large as an option (`--objects`). The small version also missed it. The large one found it as "toy" at about 0.15, with false hits (a wall photo of a baby)
- Final run found Mutual gaze 2.2 s, pointing 6.2 s and 7.6 s, child gaze on toy 8.2 to 10.3 s, Share 9.7 s. About 40 s for the 12 s clip including the chart and re encode
- Misses. Adult face often cut off at the top, so little adult gaze. Two children in the last scene broke the size based role rule

## Test results, 2026-11-19, Wang's sample

Three clips from source `1Ab4vLMMAbY`, shared by Wang (W) to Lakshya's UMN email. JPG frames only, 640x360, no labels. Stitched to video at an assumed 30 fps. Kept in `../datasets/` (gitignored, never commit).

| Clip | Scene | Result |
|---|---|---|
| 412 to 554 | Toddler, adult, Elmo, tea cups | Share 64%, both on Elmo (detected as stuffed animal) then the same cup |
| 557 to 690 | Baby, adult, books | Mutual 30%, Share 26%, two pointing segments that are really the baby holding a toy up (showing) |
| 2354 to 2439 | Baby on blanket, adult close up | Mutual 33%, adult gaze on baby correct. Baby looking at her hands came out `out_of_frame` |

Takeaways. Much better than the CDC clip (fixed camera, both faces visible). Errors match the known gaps, adult trained gaze on a baby looking down, and the arm rule confusing showing with pointing.

Also fixed 2026-11-19. Objects with the same label shared one key (two cups were both `obj:cup`). Keys are now `obj:<label>#<track id>`.

## Known gaps

- Never run on a real clinical session, only one public clip
- Role rule fails if the adult sits on the floor, or with two children in frame
- COCO has no toy classes. YOLO-World helps but is low confidence and noisy, fine tuning on the clinic's toys is the real fix
- Pointing is arm level, not finger level. Showing and giving are not detected, and holding a toy up is mistaken for pointing
- Gaze LLE was trained on adults (GazeFollow, VideoAttentionTarget). AGT shows it drops badly on autistic children until fine tuned
