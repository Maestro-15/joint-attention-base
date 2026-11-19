# Autism Gaze/Joint-Attention Project — Literature & Dataset Tracker

Owner: Lakshya
Started: 2026-10-26
Last verification pass: 2026-10-26
Status: literature review phase (no code yet)

Purpose: single place to track datasets, background on gaze estimation -> joint attention, and
2025-2026 papers on autism gaze assessment, per the professor's three asks.

## How to read the Status column

- **VERIFIED** — a human or agent opened the actual paper or dataset page and read the number written here.
- **To verify** — came from a web search summary. Treat as a lead, not a fact.

**2026-10-26 verification pass.** All 9 arXiv IDs in this document were checked against the arXiv API
and **all 9 are real, with titles matching what was written**. The previous session's citations hold up.
Two papers (AGT, MMASD) were then read properly; their rows below are now VERIFIED and several numbers
changed substantially.

> **Process warning, learned the hard way today.** An automated summary of the AGT paper reported
> "29,580 annotated frames, 17,065 face-directed vs 12,515 non-face", a model named "Social-Aware
> Context-aware Fusion", and a results table of accuracy/precision/recall against "Baseline CNN" and
> "LSTM Temporal". **Every one of those was wrong.** The real figures are 16,582 frames, 1,088 face
> (6.6%), the model is "Socially Aware Coarse-to-Fine", and the metrics are L2 distance variants
> against Sharingan and GazeLLE. The summary even contradicted the paper's own abstract, which says
> face-directed gaze is the *minority* class. **Do not put a number in front of the professor that
> came from a summary. Open the PDF.**

---

## 1. Datasets (gaze / gesture, for joint attention)

| Dataset | Modality | Subjects | Access / License | Notes | Status |
|---|---|---|---|---|---|
| **AGT (Autism Gaze Target)** | Video frames, gaze-target point + 3-class target label | **59 video recordings** of autistic children, CSBS-DP administration, from the Autism Corpus (Rollins et al.) | Collected under **IRB with informed consent from legal guardians**. No public download link found in the paper. **Code is public** (github.com/ShijianDeng/AGT), dataset is not — must ask the authors | **16,582 annotated frames**, 1 fps sampling, 5-frame clips, CVAT, Cohen's κ 0.757 on 800 double-annotated frames. Splits 9,874 / 3,344 / 3,364. **Face gaze is only 6.6%** | **VERIFIED, see deep read below** |
| Saliency4ASD | Eye-tracking, free-viewing, saliency maps | 27 children (12 ASD, 15 TD), ages 3-10 | ICME'19 challenge dataset, check current hosting | Good for saliency-model comparisons, not video/JA directly | To verify |
| DREAM | Robot-therapy video, graded joint-attention cues (point+look+verbal / point+look / look-only), ADOS scores | Children with and without ASD | Public release via PLOS ONE paper, check repository link | Has built-in JA difficulty levels — useful for staged eval | To verify |
| ChildGaze | Video, child gaze behavior (not autism-specific) | General child population | Check arXiv paper / release | Useful as general pretraining baseline | To verify |
| ChildPlay | Video, child gaze behavior (not autism-specific) | General child population | arXiv:2307.01630 | Same use as above | To verify |
| **MMASD** | Optical flow, 2D skeleton, 3D skeleton, clinician scores. **No raw video** | 32 children with ASD, 1,315 samples from 100+ hrs of play-therapy intervention | **CC-BY-NC-SA-4.0, open on GitHub, no DUA mentioned.** This is the easiest dataset here to actually obtain | Privacy-preserving by construction, since only derived modalities are released. ADOS scores attached. Authors suggest action-quality and interpersonal-synchrony as downstream tasks | **VERIFIED** |
| Gait/skeleton ASD dataset (Kinect) | 3D joint coords + RGB, walking | 59 ASD + 50 TD children | Check source paper | Full-body movement, not gaze/JA directly — maybe secondary | To verify |

**Action items:**
- [ ] For each dataset above, find and record: exact access process (download / DUA / IRB), file formats, annotation schema, any existing baseline code.
- [ ] Flag to professor which datasets need an institutional data-use agreement before we can even look at them.
- [ ] Check whether our IRB (if any) already covers use of these datasets, or if that needs to be requested separately.

---

## 2. Background / presentations: gaze estimation from video -> joint attention

No single canonical tutorial found; the pipeline is best told as a 4-stage story
built from these foundational + recent papers:

| Stage | Paper | Venue/Year | Link | Role in the story |
|---|---|---|---|---|
| 1. Single-image gaze estimation | (survey) "A Survey on Gaze Estimation Techniques" / "In the Eye of the Beholder" | various | search as needed | Baseline: head pose + eye vector from a single frame |
| 2. Scene-context gaze target | Chong et al., "Connecting Gaze, Scene, and Attention" | ECCV 2018 | arXiv:1807.10437 | Defined the gaze-target-estimation task |
| 3. Video/temporal extension | Chong et al., "Detecting Attended Visual Targets in Video" | CVPR 2020 | arXiv:2003.02501 | Adds temporal modeling — closest analog to "video -> JA" |
| 4. Current SOTA | "Gaze-LLE: Gaze Target Estimation via Large-Scale Learned Encoders" | CVPR 2025 | CVF open access | Shows state of the art to present as "where the field is now" |
| Joint attention computation | "Attention Flow: End-to-End Joint Attention Estimation" | arXiv:2001.03960 | arXiv | Computing JA as intersection of two people's gaze vectors on a shared target |
| Workshop/talks source | GAZE Workshop series (CVPR, annual) | gazeworkshop.github.io | — | Check this year's and past invited talks for slides/recordings |

**Action items:**
- [ ] Watch/read GAZE workshop talks for actual presentation material (slides or recorded talks), not just papers.
- [ ] Build a 4-stage slide outline: single-frame gaze -> video gaze -> scene-context gaze target -> joint attention (two-person intersection).

---

## 3. 2025-2026 papers: autism gaze assessment

| Paper | Year | Method | Dataset used | Key result | Link |
|---|---|---|---|---|---|
| Toward Gaze Target Detection of Young Autistic Children | 2025 | Gaze-target detection model | Introduces AGT dataset | New benchmark + model | arXiv:2511.11244 |
| AOI-Net: Structural Face AOI-Guided Eye-Gaze Track Representation Learning | 2026 | AOI-guided representation learning | Check paper | ASD detection from gaze tracks | arXiv:2608.29289 |
| Diagnosing ASD based on eye tracking using deep learning models | 2025 | CNN-LSTM | Social-attention eye-tracking task | 99.78% accuracy (verify methodology/overfitting risk) | PMC12546099 |
| Explaining Autism Detection by Deep Learning Through Eye Gaze Patterns and Integrated Gradients | 2026 | Bimodal CNN+LSTM + Integrated Gradients | Check paper | 96.6% accuracy, explainability focus | Springer, Feb 2026 |
| Exploring Image Transforms derived from Eye Gaze Variables for Progressive Autism Diagnosis | 2025 | Transfer learning on gaze-derived image transforms | Check paper | — | arXiv:2506.09065 |
| An image-based analytics framework for early autism detection using eye movements | 2025 | Scanpath-image based deep learning | Check paper | Screening-oriented, grayscale scanpaths | ScienceDirect S2772442525000589 |
| GNNs and sequential architectures for autism detection from eye-tracking biomarkers: a multi-site study | 2026 | GNN + sequential models | Multi-site | Cross-site generalization — relevant if combining datasets | Springer 10.1186/s12888-026-08256-x |

**Action items:**
- [ ] Read each paper fully (these are summaries from search, not full reads) and fill in "Dataset used" and verify reported numbers.
- [ ] Note which papers report cross-dataset generalization — this matters a lot given how small/fragmented these datasets are.
- [ ] Watch for a pattern: is the field converging on a standard benchmark, or is everyone using their own private clinical dataset?

---

## Open questions for the professor

- [ ] Do we have existing IRB/DUA coverage for any of the datasets above, or does that need to be requested?
- [ ] Is "gesture" meant broadly (pointing, reaching) or specifically full-body movement (gait)?
- [ ] Should the literature review prioritize datasets we can realistically get access to over the theoretically best-fit ones?

---

## Deep read: AGT / SACF (the single most relevant paper to this project)

**Toward Gaze Target Detection in Young Autistic Children.** Deng, Kosloski, Vasireddy, Li, Sherwood,
Hatha, Patel, Rollins, Tian. **UT Dallas** (CS + School of Behavioral and Brain Sciences).
arXiv:2511.11244, 14 Nov 2025. Carries an **AAAI 2026** copyright line.
Code: https://github.com/ShijianDeng/AGT

This paper serves all three of the professor's asks at once: it introduces a dataset, it is a
2025-2026 autism gaze paper, and its related-work section is a ready-made map of the gaze-target
literature.

### Why it matters

It is the **first autism-specific dataset for gaze target detection**. Its stated motivation is the
exact distribution problem that shows up across the whole field:

| Dataset | Population | % of gaze targets that are a face |
|---|---|---|
| VideoAttentionTarget | adults, TV shows | **69.0%** |
| GazeFollow | adults, web images | 23.0% |
| ChildPlay | neurotypical children | 15.7% |
| **AGT** | **autistic children** | **6.6%** |

Models trained on neurotypical data learn "look for the nearest face". That heuristic earns a high
score on VideoAttentionTarget and collapses on autistic children, where the clinically important
event — a child looking at a person's face — is 1 frame in 15. The paper's words: trained models
"tend to predict non-social targets and could miss critical moments of social engagement."

### Method, SACF (Socially Aware Coarse-to-Fine)

A divide-and-conquer routing architecture rather than one monolithic model.

1. **SCA module (Social Context Awareness).** A fine-tuned **Qwen2.5-VL-7B-Instruct** MLLM is asked
   "where is the child looking?" and its next-token probability on "looking"/"not" gives a social
   context score `s = P(looking at face | I, T)`. Thresholded at τ into a binary coarse decision.
2. **Two gated expert models**, both built on the same gaze backbone:
   - `Ex_aware`, trained on data augmented with a **strong Gaussian blur over irrelevant regions**,
     so it specialises in the confident social case.
   - `Ex_agnostic`, trained on unmodified data, for the frequent non-social case.
3. **Fine semantic check.** After the expert predicts a point, the final class is decided by testing
   whether that point falls inside the union of adult-face bounding boxes.

Base gaze models used: **GazeLLE** (Ryan et al. 2025, frozen DINOv2 + positional prompt + transformer
decoder) and **Sharingan** (Tafasca, Gupta, Odobez 2024). Loss is pixel-wise BCE on a Gaussian-blurred
ground-truth heatmap. Trained in PyTorch on **NVIDIA A6000** GPUs.

### Results (Table 3). Lower L2 is better, higher F1 is better

| Model | L2 | L2 face | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Sharingan (off the shelf) | 0.0615 | 0.0647 | 0.4377 | 0.8010 | 0.5660 |
| Sharingan fine-tuned on AGT | 0.0486 | 0.0949 | 0.7744 | 0.7330 | 0.7531 |
| **Sharingan + SACF** | **0.0480** | 0.0817 | 0.7647 | 0.7573 | **0.7610** |
| *Sharingan + SACF, oracle gate* | *0.0478* | *0.0378* | *0.9581* | *1.0000* | *0.9786* |
| GazeLLE (off the shelf) | 0.0670 | 0.1092 | 0.3868 | 0.6553 | 0.4865 |
| GazeLLE fine-tuned on AGT | 0.0460 | 0.1130 | 0.6984 | 0.6408 | 0.6684 |
| **GazeLLE + SACF** | **0.0453** | 0.1019 | 0.7041 | 0.6699 | **0.6866** |
| *GazeLLE + SACF, oracle gate* | *0.0396* | *0.0307* | *0.9856* | *0.9951* | *0.9903* |

They macro-average P/R/F1 over Face vs Not-face specifically so the 93.4% majority class cannot
inflate the score, and they report L2 separately for object / face / person-non-face targets so
minority performance stays visible.

### The opening this paper leaves wide open

**The gate is the bottleneck, by a huge margin.** Compare the real system to its own oracle:

- GazeLLE + SACF, real gate: **F1 0.6866**
- GazeLLE + SACF, perfect gate: **F1 0.9903**

Table 4 shows why. The SCA module's own Face-vs-Not-face performance is **precision 69.23%, recall
65.53%, F1 0.673** on a support of only 206 face frames. The gaze models are not the limiting factor
any more — **the social-context router is**. Roughly 30 F1 points are sitting behind a better gate.

That is a concrete, measurable, already-quantified-by-the-authors gap, which is a much better place
to start than a blank field.

**Open questions this raises, worth bringing to the professor:**
- Could a purpose-built face/gaze-cue classifier beat a general 7B MLLM at the gate task?
- The gate is a hard threshold on a single scalar. Would soft mixing of the two experts beat routing?
- Would temporal context fix it? The gate currently sees one frame, but a child looking up at a face
  is a *transition*, and ChildPlay's "gaze shift" class exists precisely to describe that.
- AGT is 1 fps, which deliberately throws away the temporal signal. Is that leaving information on
  the table for joint-attention detection specifically?

### Access

Collected under IRB with informed consent from legal guardians. The paper does **not** give a public
download link. The code repo is public. **Action: email the authors** (contacts are @utdallas.edu,
listed on the paper's first page) to ask what the process is. Worth doing early, since this is the
closest dataset to the project and access will not be instant.

---

---

# VERIFICATION PASS 2, 2026-10-26. Tasks 1, 2 and 3 completed

## Task 2 answered: GAZE workshop is the presentations source

**GAZE 2026, the 7th International Workshop on Eye and Gaze in Computer Vision**, CVPR 2026,
Thursday 4 June 2026, half day. https://gazeworkshop.github.io/2026/ (past editions 2019 to 2024
linked from the same site). **No slides or recordings are posted on the page**, so talks would have
to be requested or found elsewhere.

**Invited speakers:**
- **James M. Rehg** (UIUC), *"Inference and Forecasting of 2D and 3D Gaze"*. **This is the most
  relevant name on the page for us.** Rehg co-authored VideoAttentionTarget (Chong et al. CVPR 2020),
  which is stage 3 of our pipeline story, and he also works on autism behaviour analysis.
- **Ken Pfeuffer** (Aarhus), *"Eye-Hand Symbiosis"*. Relevant to the gesture half.

**Accepted papers, one of which is directly on joint attention:**
- **End-to-End Shared Attention Estimation via Group Detection with Feedback Refinement** (Nakatani
  et al.). "Shared attention" is joint attention. Closest workshop paper to our goal.
- Learning Ego-Exo Visual Representations for Conversational Gaze Estimation (Gupta et al.)
- FlowScan, gaze scanpath prediction (Aklilu et al.)
- Learning to Look, CLIP-guided head-position-invariant gaze estimation (Lakhotia et al.)
- SIGN, statistically informed gaze network (Ye and Wedel)
- How Much Future Helps, causal egocentric gaze estimation (Li et al.)

## Task 3 additions: 2026 papers the first pass missed

| Paper | Venue | Why it matters | Status |
|---|---|---|---|
| **GazeAnywhere: Gaze Target Estimation Anywhere with Concepts** | CVPR 2026 | Current SOTA direction for gaze target estimation. PDF free on CVF open access | Found, unread |
| **GazeVLM: A Vision-Language Model for Multi-Task Gaze Understanding** | CVPRW 2026 | Vision language models applied to gaze, same family as AGT's MLLM gate | Found, unread |
| **PAGE: Towards Practical Human-level Gaze Target Estimation** | arXiv:2607.04860 | Explicitly targets human-level performance, which is the bar ChildPlay showed is still unmet on distance | Found, unread |

## Task 3, verified reads

### AOI-Net — VERIFIED, and it is a different task than ours

**AOI-Net: Structural Face AOI-Guided Eye-Gaze Track Representation Learning for ASD Detection.**
Huang, Sun, Chen, Wang, Chen, Ji, Zhang, Cheung. **IEEE Computational Intelligence Magazine, 2026.**
arXiv:2608.29289, 29 Aug 2026.

**Important distinction.** This is **not** gaze target detection from video. It takes **eye tracker
output** (gaze tracks) and classifies **ASD versus TD**. Different input, different output, different
problem. Useful as context, not as a baseline for us.

- Data: a **proprietary clinical eye-tracking database, 8 stimulus subsets, over 1,300 participants.**
  That is by far the largest participant count in this document. Not public.
- Method: models short-term temporal dynamics plus AOI-level structure (which facial region is being
  looked at), fused by a gating mechanism.
- **Recurring theme worth noting:** they also use "class-distribution-aware learning" to handle ASD
  versus TD class imbalance. That is the third paper in this document whose central move is handling
  imbalance.

### ChildGaze — VERIFIED, and the tracker description was wrong

**ChildGaze: A Benchmark Dataset for Collaborative Behavior Understanding in Children.**
Penchala, Kontham, Bhattacharjee, Mahmoodi, Fonseca, Karami, Garemani, Mittal, Rahimi, Amiri Golilarz.
arXiv:2609.06353, 6 Sep 2026. **CC BY 4.0.**

The tracker called this "video, child gaze behavior, general child population, useful as general
pretraining baseline". That undersells it and misdescribes it.

- **It is built on top of the ChildPlay video collection**, so it is the same footage with new labels.
- Labels are **collaborative versus non-collaborative**, per child, per frame.
- Provides **face, left-hand and right-hand bounding boxes for children and adults.**
- 27 annotated videos, 10,641 frames, 73,268 annotation rows.
- Reliability: 1,187 frames double annotated, **93.16% raw agreement, Cohen's κ 0.8631**, bounding
  box mean IoU 0.808.
- Baselines: pretrained ViT and Swin, up to 97.44% child-person-level accuracy.
- **Not autism specific.**

**Why this is actually important for us.** Their motivating sentence is the exact gap between layer 2
and layer 3 of our pipeline: *"estimating where a child is looking does not necessarily reveal
whether the child is actively participating in a shared activity."* That is the joint attention
problem stated plainly.

**And it has hand boxes.** ChildPlay gives gaze on this footage, ChildGaze gives hands on the same
footage. Together that is **gaze plus gesture on one video collection**, which is rare and worth
raising with the professor.

### "Diagnosing ASD based on eye tracking using deep learning" — VERIFIED, and the 99.78% does not hold up

**Al-Adhaileh, Alsubari, Al-Nefaie, Ahmad, Alhamadi. Frontiers in Medicine, 9 Oct 2025.**

The first pass flagged this as "verify methodology / overfitting risk". That instinct was correct.

- Data: public benchmark, **59 children** (29 ASD, 30 TD, mean age 7.88), RED mobile eye tracker at
  60 Hz, roughly **1,048,575 instances**.
- Models: LSTM (99.70%) and CNN-LSTM (**99.78%**), stratified 5-fold cross validation.
- **The problem is arithmetic.** 1,048,575 samples from 59 children is about **17,773 samples per
  child**. If the folds are split per **sample** rather than per **participant**, every child appears
  in both training and test, and the model can score by recognising individuals rather than by
  recognising autism. That is textbook data leakage and it is the standard explanation for a 99.8%
  medical classifier.
- **Confidence level, stated honestly.** The participant and sample counts are verified. The claim
  that the split was per sample came from an automated read of the paper and **should be confirmed by
  reading the methods section directly before repeating it to anyone.** The arithmetic concern stands
  either way and is worth raising as a question.
- **Use this paper as a cautionary example in the review, not as a result to build on.**

### Image Transforms for Progressive Autism Diagnosis — read, low value

Copiaco, Ritz, Himeur, Eapen, Albanna, Mansoor. arXiv:2506.09065, 7 Jun 2025. The abstract is
promotional and names no dataset, no participant count and no accuracy. Would need the full PDF to be
worth anything. **Deprioritise.**

### Still unread, blocked

- **"An image-based analytics framework for early autism detection using eye movements"**,
  ScienceDirect S2772442525000589. **Paywalled, returns HTTP 403.** Needs university library access.
- **"Explaining Autism Detection by Deep Learning Through Eye Gaze Patterns and Integrated
  Gradients"**, Springer Feb 2026. Not yet attempted.
- **GNNs and sequential architectures, multi-site study**, Springer. Not yet attempted. Worth
  prioritising because cross-site generalisation is the honest test these datasets usually fail.

## Task 1, dataset verification updates

**Saliency4ASD — DISCREPANCY, do not quote the tracker's numbers.**
This document's table says 27 children (12 ASD, 15 TD), ages 3 to 10. Published descriptions say
**14 ASD and 14 TD, ages 5 to 12**, Tobii T120, 300 images, 3 seconds each, free viewing.
**Someone needs to open the source paper and settle it.** Publicly available at
https://doi.org/10.5281/zenodo.2647418 and https://saliency4asd.ls2n.fr/datasets/
Note it is **free-viewing of static images**, so it is a saliency dataset, not a joint attention one.

## The dataset table, reorganised by what it is actually for

Our professor asked for **gaze and gesture**. Almost nothing covers both. Proposed split:

**Gaze, autistic children** — AGT (IRB only, must email authors). This is the only one.
**Gaze, neurotypical children** — ChildPlay (public), GazeFollow (public, adults).
**Gaze, eye-tracker based, not video** — Saliency4ASD (public), the AOI-Net database (private),
the Frontiers 59-child set (public).
**Gesture and body, autistic children** — MMASD (public, CC BY NC SA, no DUA, but **no gaze**),
the Kinect gait set.
**Gesture and collaboration, neurotypical children** — ChildGaze (public, hand boxes, on ChildPlay
footage).

**The gap, which is itself a finding worth reporting:** there is **no public dataset with both gaze
and gesture annotations for autistic children**. AGT has gaze but is gated and has no gesture.
MMASD has gesture but no gaze. ChildPlay plus ChildGaze has both but no autistic children.

