# Papers

PDFs are in `papers/`. The wider literature review (datasets, 2025 and 2026 autism gaze papers, GAZE workshop) is in `../literature_tracking.md`.

**Rule.** Every number here was read from the PDF. Never add a number from a search summary. The reason is in the process warning at the top of `literature_tracking.md`.

## GazeTransformer

**Temporal Understanding of Gaze Communication with GazeTransformer.** de Belen, Mohammadi, Sowmya. UNSW Sydney. NeurIPS 2023 Gaze Meets ML workshop (PMLR). File `papers/Gaze Transformer.pdf`. Code promised at github.com/gazetransformer/gazetransformer.

**Why it matters.** It is a full pipeline from a frame to a Joint Attention event, which is the shape of our whiteboard. It is on adults in social videos, not children.

**Two stages**

1. **Atomic level, per frame.** A backbone (ResNet50 or ResNet101) feeds a transformer encoder and decoder (similar to DETR). Each query predicts a human target interaction (HTI), meaning human box, target box, and a looking or not looking class. These fill an adjacency matrix where A[i,j] = 1 means i looks at j.
2. **Event level, per video.** An LSTM plus a fully connected layer reads the unique atomic labels in a video and classifies the event.

**Labels**

| Level | Classes |
|---|---|
| Atomic, per frame | Single, Mutual, Share |
| Event, per video | Non communicative, Mutual Gaze, Gaze Aversion, Gaze Following, Joint Attention |

They dropped VACATION's Avert, Refer and Follow atomic labels because those need time to judge, so they are not truly per frame. Labels come straight out of the matrix. Mutual when A[i,j] and A[j,i] are both 1. Share when column j has more than one 1. Single otherwise.

**Dataset.** (M)VACATION, their modified version of VACATION (Fan et al. 2019, 300 videos of social scenes). Atomic counts after the change are Single 87,998, Mutual 40,497, Share 33,452.

**Selling point.** It does not need head or object boxes as input. It predicts them itself, end to end.

**Used in our base.** The adjacency matrix and the Single, Mutual, Share rule (`base/jabase/scene_graph.py`). The LSTM event stage is the kind of model the research layer could use.

**Results (read in full 2026-11-18).** Training samples every 10th frame, Hungarian matching, 250 epochs, DETR or Deformable DETR pretrained on COCO. Event module input is up to 5 unique adjacency matrices (key frames where the matrix changes), max 7 nodes.

- Head and object localisation. ResNet50 P 92.29, R 76.38, F 83.58. Misses small objects
- Atomic (DETR R50). Single F 86.28, Mutual F 66.38, Share F 60.06, top 1 accuracy 88.40. Baseline Chong 2020 (given true boxes) 78.92
- Event (DETR R50). Non comm F 62.69, Mutual Gaze 65.00, Gaze Aversion 33.33, Gaze Following 18.00, Joint Attention 46.67 (best variant R101 58.82), top 1 accuracy about 85
- Event with true matrices as input. Gaze Following F 72.73, Joint Attention 57.89, accuracy 91.90. So errors cascade from the atomic stage
- Their limits. Small objects, cascade dependence, the two stages trained separately

**Notes for us.** The dropped Refer and Follow labels are close to IJA and RJA, and Gaze Following is the weakest event (F 18). Keeping only unique matrices throws away timing, so response latency cannot be measured this way. First author de Belen also publishes on autism (eye tracking RJA in preschool ASD, CV in ASD review).

## AGT

**Toward Gaze Target Detection in Young Autistic Children.** Deng et al., UT Dallas. arXiv 2511.11244, AAAI 2026. File `papers/Toward Gaze(2025).pdf`. Code github.com/ShijianDeng/AGT. The full deep read is the AGT section of `../literature_tracking.md`.

**Key points**

- First autism specific gaze target dataset. 16,582 frames from 59 recordings of CSBS DP sessions, 1 fps. Not public, IRB gated, must ask the authors
- Only 6.6% of child gaze targets are a face, against 69.0% in VideoAttentionTarget. Models trained on adults learn "look for a face" and miss the rare social moments
- Method SACF. A fine tuned Qwen2.5 VL 7B decides "is the child looking at a face?", then routes to one of two expert gaze models. Base gaze models are Gaze LLE and Sharingan
- Gaze LLE F1 goes 0.4865 off the shelf, 0.6684 fine tuned, 0.6866 with SACF, 0.9903 with a perfect router. **The router is the bottleneck**

**Used in our base.** Gaze LLE as the gaze model, and the rule that a gaze point inside a face box means looking at that person.

## ViTGaze

**ViTGaze, Gaze Following with Interaction Features in Vision Transformers.** Song, Wang, Yao, Liu, Zhang, Xu. Huazhong University of Science and Technology (plus Shandong University and South China University of Technology). Visual Intelligence journal, arXiv 2403.12778 (v2, 14 Nov 2024). File `papers/ViTGaze(2024).pdf`. No code link found in the paper text.

**Why it matters.** A candidate for the same gaze slot Gaze LLE fills in the base. Added 2026-11-17 at Lakshya's request. Not used by AGT.

**Idea.** Inside a vision transformer every image patch attends to every other patch. ViTGaze reads those self attention maps directly. The attention from the patch on a person's head to the rest of the image already says how the head relates to the scene, which is what gaze following needs.

**Parts**
- Encoder is a plain ViT S (12 blocks, 6 heads), initialised from DINOv2
- A 4D interaction encoder takes attention maps from blocks 3, 6, 9 and 12
- A 2D spatial guidance module uses the head position to pick out that person's interactions
- Two small heads predict the gaze heatmap and whether the target is in or out of frame
- Decoder parameters are under 1% of the model. Whole model is 22 M parameters and 4.62 GFLOPs

**Training.** GazeFollow for 15 epochs (AdamW, batch 48), then 1 epoch on VideoAttentionTarget. Both datasets are mostly adults.

**Claims, from the paper's own text.** Best single modality method, with AUC up 3.4% on GazeFollow and AP up 5.1% on VideoAttentionTarget. Comparable to multi modality methods with 59% fewer parameters.

**Compared with Gaze LLE.** Both sit on a DINOv2 ViT. Gaze LLE uses the ViT's output features plus a head prompt and a small decoder. ViTGaze uses the attention maps inside the ViT. ViTGaze uses the small ViT (S), our Gaze LLE setup uses the base one (B).

**Not read yet.** The full results table did not extract cleanly from the PDF, so per method numbers are not recorded here. Read Table 1 in the PDF before quoting any.

## Kosmydel 2026, dual camera joint attention

**Automated Detection of Mutual Gaze and Joint Attention in Dual Camera Settings via Dual Stream Transformers.** Kosmydel, Gajewski (AGH University, Krakow), Białek (Jagiellonian University, Krakow). arXiv 2604.27105v1, 29 Apr 2026. File `papers/Kosmydel Dual Camera JA(2026).pdf`. Read in full 2026-11-17.

**Open source.** Code github.com/child-lab-uj/child-lab-nn, weights zenodo.org/uploads/19707957, test set zenodo.org/uploads/19706512.

**What it does.** Frame level **binary** classification, MG vs not MG and JA vs not JA, from two synced cameras (one on the infant, one on the parent). Separate models for MG and JA.

**Model.** Two frozen Gaze LLE backbones (`gazelle_dinov2_vitl14_inout`, shared weights), detection head removed. Tokens projected to 512, concatenated, a CLS token added, 3 layer transformer encoder (4 heads), MLP head, sigmoid. Head boxes from RetinaFace.

**Data.** 13 caregiver and infant dyads, 7 sessions each, free play, typical infants (not autism). Cameras synced by audio cross correlation. Frames at **1 fps**. Frames without a confident face for both people dropped. Test set is 2 held out sessions, **downsampled to about 50/50**.

**Results (test, mean of 5 runs)**

| Task | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| Mutual gaze | 0.808 | 0.752 | 0.915 | 0.825 | 0.834 |
| Joint attention | 0.776 | 0.795 | 0.745 | 0.767 | 0.862 |

CNN baseline and Llama 4 (16x17B) baseline both far worse (JA F1 0.589 and 0.610).

**Their stated limits.** Depends on face detection, 1 fps misses fast behaviour, only 13 dyads.

**What it does NOT do (our openings).** No temporal model across frames, each frame judged alone. No RJA vs IJA, it cannot say who started the joint attention or how fast the other responded. JA here is only the earliest "ecological" form. No gesture. No autism. No gaze target or object identity, only a yes or no per frame.

**For us.** The closest existing system to the whiteboard. Same Gaze LLE backbone. Usable as a **baseline or starting point**, not a competitor to hide from. Their labelling tool and audio sync method are reusable ideas.

## Ko 2023, JA deep learning for autism

**Development and Validation of a Joint Attention Based Deep Learning System for Detection and Symptom Severity Assessment of Autism Spectrum Disorder.** Ko, Lim, Hong, Hong, Park. Yonsei University, Seoul National University, LumanLab. JAMA Network Open 2023, doi 10.1001/jamanetworkopen.2023.15174. Full text saved as `papers/Ko JA Deep Learning(2023).md` (the PDF could not be downloaded by script). Read in full 2026-11-17.

**Setup.** 95 children (45 ASD, 50 TD), 24 to 72 months, South Korea. A structured 10 minute protocol from the ESCS with a live examiner eliciting IJA, low level RJA (pointing near) and high level RJA (pointing at a poster across the room). One front facing camera, 1920 by 1080, 30 fps.

**Model.** CNN plus LSTM plus attention on raw clips. IJA clips 10 s (300 frames), RJA clips 5 s. 10 fold cross validation **grouped by child** (no child in both train and test). Grad CAM and attention plots for explanation.

**Results.** ASD vs TD AUROC 99.6% (IJA), 99.8% (low RJA), 99.5% (high RJA). Severity AUROC 90.3% (IJA), 84.4% and 84.2% (RJA). IJA best for severity.

**Caveats we spotted.**
- Large IQ gap. ASD best estimate IQ means about 55 to 60, TD about 104 to 105. The authors list it as a limitation. The model may partly learn general development, not joint attention.
- ASD children recruited from a hospital, TD children from day care centres. Different recruitment sources can leak in through setting or behaviour, worth asking about.
- Small sample, no external validation.

**What it does NOT do (our openings).** It never detects gaze targets, pointing, or RJA and IJA events. It classifies whole task clips as ASD or TD. The behaviour (triadic gaze, delayed head turn) is only seen afterwards through Grad CAM, not measured.

**For us.** Shows the clinical value of IJA and RJA tasks and that IJA tracks severity best. Our angle, measuring the events explicitly and interpretably, is exactly what this paper leaves to post hoc visualisation.

## Prakash 2023 (unverified contents)

**Computer Vision Based Assessment of Autistic Children, Analyzing Interactions, Emotions, Human Pose, and Life Skills.** Prakash, Kohli, Kohli, Prathosh, Wadhera, Das, Panigrahi, Kommu. IEEE Access 2023, doi 10.1109/access.2023.3269027. Existence and authors confirmed via Crossref. Full text not obtained. Search snippets say 300 videos, pose based gaze following and pointing models. **Do not quote numbers until the PDF is read.**
