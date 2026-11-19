# Training plan

**Nothing has been trained yet.** The base runs because every part is either a model someone else already trained or a hand written rule.

## What each part is today

| Part | Today | Trained on |
|---|---|---|
| Objects | Pretrained YOLO11n | COCO, everyday photos |
| Skeleton | Pretrained YOLO11n pose | COCO keypoints |
| Face | Rule on head keypoints | n/a |
| Role, child or adult | Rule on body size | n/a |
| Gaze | Pretrained Gaze LLE | GazeFollow and VideoAttentionTarget, mostly adults |
| Pointing | Rule on arm joints | n/a |
| Scene graph, temporal flow | Logic | n/a |

## What will need training, in priority order

1. **Gaze on children.** The biggest gap. AGT measured Gaze LLE at F1 0.4865 off the shelf on autistic children and 0.6684 after fine tuning on their data. Needs child gaze data (AGT, or whatever W provides)
2. **Objects.** Fine tune YOLO on labelled frames of the actual toys used in sessions, since COCO lacks most toys
3. **Child or adult.** Replace the size rule with a small classifier, or set roles by hand per video
4. **Hands and gestures.** A hand landmark model (for example MediaPipe Hands) for finger pointing, then training on child gestures such as showing and giving
5. **RJA and IJA.** Lakshya's research model, trained on labelled sessions. Out of scope for the base

## Blocker

Training cannot start without data. Getting datasets from W is the first step.
