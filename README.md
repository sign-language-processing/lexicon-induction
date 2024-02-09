# Lexicon Induction from Continuous Sign Language Corpus

## Overview
`lexicon-induction` is a project aimed at inducing a lexicon from continuous sign language corpora. The project leverages large datasets of sign language videos, pose estimation technologies, sign language segmentation tools, and machine learning models to analyze and categorize sign language data.

### Datasets Used
- [**DGS Corpus**](https://www.idgs.uni-hamburg.de/en/forschung/forschungsprojekte/dgs-korpus.html)[^1] - Development of a corpus-based electronic dictionary German Sign Language/German.
- **Corpus NGT**[^2] - An online corpus for professionals and laymen in Dutch Sign Language (NGT).
- **BSL Corpus**[^3] - Building the British Sign Language Corpus. 

## Workflow

### 1. Pose Estimation
For each video in `corpus/videos`, we run pose estimation:
```bash
video_to_pose -i sign.mp4 --format mediapipe -o sign.pose
```
Output pose files are stored in `poses`.

### 2. Segmentation
Pose sequences are automatically segmented using the sign language segmentation tool:
```
pose_to_segments -i sign.pose -o sign.eaf --video sign.mp4
```
Segmentation outputs (ELAN files) are stored in `segments`.

### 3. Sign Language Recognition
For each segment in the ELAN file:
- Crop the corresponding pose.
- Run through a sign language recognition model.

We focus on the softmax layer output for label distributions.

### 4. Clustering
- Signs are clustered based on softmax output vectors.
- Assumes a Zipfian distribution over sign usage.
- Cluster sizes reflect this distribution.

### 5. Evaluation
- Evaluated on the pre-annotated DGS Corpus.
- Metrics relevant for clustering under a Zipfian distribution are used.

## References
[^1]: Prillwitz, Siegmund, et al. "DGS Corpus project--development of a corpus based electronic dictionary German Sign Language/German." Sign-lang at LREC. 2008.
[^2]: Crasborn, Onno, and Inge Zwitserlood. "The Corpus NGT: An online corpus for professionals and laymen." 2008.
[^3]: Schembri, Adam, et al. "Building the British sign language corpus." Language Documentation & Conservation, vol. 7, 2013, pp. 136-154.
