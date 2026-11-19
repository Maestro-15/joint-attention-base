# Professor demo

Everything needed to show the base pipeline working. Built 2026-11-18.

## What is here

| File | What |
|---|---|
| `summary.pdf` | One page handout. Pipeline, demo result, what each part is built on, limits, next steps. Source `summary.html` |
| `assets/` | The frame grid and timeline chart used in the handout |
| `videos/` | Input clips (gitignored). Currently one CDC milestone clip |
| `output/<clip>/` | Pipeline outputs per clip (gitignored). The video to play is `annotated_h264.mp4` |

**Demo clip.** CDC "Learn the Signs. Act Early." 18 month milestone, "Points to show someone what he wants". Public domain (US government work), from Wikimedia Commons. 12 s, 1280x720. More CDC milestone clips are in the Commons category "CDC videos about developmental milestones". Good next ones are "2 Year Milestone, Points to things or pictures when they are named" and "1 Year Milestone, Looks at the right picture or thing when it's named". Wikimedia rate limited the script download, so grab them in a browser.

**Why not the Kosmydel test set.** Its Zenodo files are restricted (access request needed), even though the paper says it is public.

## Live run in the meeting

```bash
cd "projects/comp vision/base"
./demo.sh ../demo/videos/cdc_18mo_points_to_show.webm
```

Takes about 40 s on the laptop GPU. Then open `demo/output/cdc_18mo_points_to_show/annotated_h264.mp4` and `timeline.png`.

Run once before the meeting so the models are cached. The first ever run downloads Gaze LLE and the CLIP text model.

## Live view

```bash
cd "projects/comp vision/base"
./live.sh                                              # webcam
./live.sh ../demo/videos/cdc_18mo_points_to_show.webm  # the clip, live
```

A window shows the annotations as each frame is processed. Press q to stop. With the webcam, have someone sit next to you, look at each other (Mutual), both look at an object like a cup or phone (Share), and point with a straight arm (pink arrow). Pointing needs the elbow visible, so sit back from the laptop.

## Suggested order (about 5 minutes)

1. **The handout first.** Point at the pipeline row. Everything left of RJA and IJA runs. RJA and IJA is the research.
2. **Play `annotated_h264.mp4`.** What to watch for.
   - About 2 s. Adult and child in Mutual gaze (labels on the face boxes)
   - About 6 to 8 s. Pink arrow, child pointing
   - About 8 to 10 s. Child gaze line to the green "toy" box, then Share
3. **Show `timeline.png`.** This is the output the research layer will consume. Every bar is a timed segment, so response latency and who moved first can be measured from it.
4. **Be upfront about the limits** (bottom of the handout). Gaze is adult trained (AGT numbers), toy detection is weak, child vs adult role is a size guess and fails in the last scene, arm pointing only.
5. **Asks.** W's datasets and a real session video, AGT dataset access, Kosmydel 2026 as a baseline, how to define RJA and IJA events.

## Honest result on this clip

Pipeline found Mutual gaze at 2.2 s, two pointing segments (6.2 s and 7.6 s), child looking at the toy 8.2 to 10.3 s, Share at 9.7 s. Misses. The adult's face is often cut off at the top of frame, so her gaze is mostly missing. In the final scene the girl is labelled "child" and the boy "person2". YOLO-World also tags a wall photo of a baby as a toy.
