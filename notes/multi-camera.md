# Multi camera (parked)

**Status.** Parked by Lakshya on 2026-11-17. The base assumes one camera. The board's "for all cameras?" means the team decides how to do it.

## Options discussed

| Option | How | Good | Bad |
|---|---|---|---|
| 1. Per camera, then merge (suggested start) | Run each camera alone. For each moment, take each person's gaze from the camera that sees their face best, and gestures from the one that sees their arms best. Match people by role, objects by class | No calibration. The 2D gaze models work as they are | Two identical toys get confused. Not a true combination of views |
| 2. Calibrated 3D | Calibrate once (checkerboard), merge skeletons into 3D, gaze becomes a 3D line, the target is the object it hits | Most accurate. Handles occlusion and close objects | Needs fixed cameras, synced clocks, calibration. 2D gaze models do not output 3D directly |
| 3. Best single view | Pick the clearest camera each moment, ignore the rest | Simplest | Throws away information |
| 4. Learned fusion | Feed features from all cameras into one model | Could be best | Needs lots of labelled multi camera data |

## What decides it

Ask W about their data.
- How many cameras, and are they fixed?
- Are the videos time synced?
- Is there calibration data?
- Are labels per camera or per session?

If the cameras are fixed and calibrated, option 2 is the long term answer. Option 1 is the quick way to get something working.

The code already keys people by role and objects by class name so option 1 can be added later without changing the stages.
