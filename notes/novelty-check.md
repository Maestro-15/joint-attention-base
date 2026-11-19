# Novelty check, 2026-11-17

Question from Lakshya. Is "AI that measures joint attention (gaze and gesture) in video of young children to help detect autism" new, or already done?

**Short answer.** The idea as a whole is **not new**. A handful of groups have done versions of it. But the field is thin, and there are specific, defensible openings. Novelty has to come from a chosen angle, not the general idea.

**Confidence.** Medium to high. Kosmydel 2026 and Ko 2023 were **read in full** on 2026-11-17 (details in `papers.md`). The review was checked against its full text page. Prakash 2023 exists (Crossref) but its contents are only from search snippets.

## Closest prior work

| Work | What it does | How close to us | Checked against |
|---|---|---|---|
| **Kosmydel, Gajewski, Białek 2026**, arXiv 2604.27105, "Automated Detection of Mutual Gaze and Joint Attention in Dual Camera Settings via Dual Stream Transformers" | Detects mutual gaze and joint attention from **two synced cameras**, using **frozen Gaze LLE backbones** plus token fusion. Caregiver and infant interactions. Beats a CNN baseline and a multimodal LLM. Open source weights | **Very close to our whiteboard**, including multi camera and Gaze LLE. But typical caregiver and infant pairs, **not autism**, no RJA vs IJA split, no gesture | arXiv abstract |
| **Ko et al. 2023**, JAMA Network Open (Yonsei, Seoul National University, LumanLab) | Deep learning on video of three JA tasks (IJA, low level RJA, high level RJA) with a live examiner. 45 ASD and 50 TD children, 24 to 72 months. Classifies ASD vs TD and severity. Input is fixed 10 s clips (224 by 224, 300 frames) | Same goal (autism from JA video). But it is a black box classifier on task clips, it does **not detect** gaze targets, pointing, or RJA and IJA events. Large IQ gap between groups | Read in full |
| **Prakash et al. 2023**, IEEE Access, "Computer Vision Based Assessment of Autistic Children" | 300 videos of autistic children. Pose based models for following eye gaze and hand pointing, plus activity and emotion models | Gaze plus gesture for autism from video. Close on components | **Search snippets only, unverified** |
| **Zhang et al. 2018** (via the review) | RGB camera plus Kinect. Detects adult pointing or gaze, eye contact, and child gaze following, i.e. RJA | Early version of the same RJA idea. Validated on only 8 non ASD adults | Review text |
| **Chong et al. 2020**, CVPR, "Detecting Attended Visual Targets in Video" | Gaze target model (VideoAttentionTarget). Search snippets say it includes a toddler study detecting toy to examiner face gaze shifts, 20 toddlers, 10 with autism | Gaze shift as a JA building block | **Search snippet, check the PDF** |
| **AGT, Deng et al. 2025** | Gaze target detection in autistic children. See `papers.md` | Gaze only, no events, no gesture | Read in full |
| **RJAfinder 2022** | Automated RJA from **eye tracking** data, not video | Different sensor | Search snippet |

## What the field says about itself

From the 2026 review, Qaraqe et al., "Joint attention in autism, a narrative review of assessment techniques from behavioral observation to artificial intelligence", Behavior Research Methods 58(3)77.
- "only three studies were identified that employed computer vision and AI for automated assessment" (Zhang 2018, Prakash 2023, Ko 2023)
- "the use of videos to develop AI models remains underexplored"
- "benchmark datasets remain scarce in autism research on JA assessment"

## Where real novelty could be

1. **Explicit RJA and IJA event detection** from session video, giving clinician readable measures (who initiated, response latency, missed bids). Ko 2023 classifies whole clips instead. Strongest angle, and it is Lakshya's research layer.
2. **Child specific gaze in the loop.** AGT shows adult trained gaze models fail on autistic children. Kosmydel and Prakash do not address this.
3. **Gaze plus gesture together** for both RJA and IJA, rather than gaze alone (AGT, Kosmydel) or task clips (Ko).
4. **AGT's open bottleneck.** The face vs not face router (F1 0.69 real vs 0.99 perfect).
5. **Multi camera for autism.** Kosmydel does dual camera for typical infants. Applying and adapting that to clinical autism sessions is open.

## Must tell the professor

- **Kosmydel 2026 is the paper most like our whiteboard.** It already does Gaze LLE plus multi camera plus joint attention. It is open source, so it may be a baseline or starting point instead of a competitor. Read it in full before the meeting.
- Kosmydel 2026 and Ko 2023 are now in `papers/` and summarised in `papers.md`.
