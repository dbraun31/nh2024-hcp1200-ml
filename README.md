# Using Machine Learning to Classify Emotional States in the Human Connectome Project - Neurohackademy 2024
<div align=center>
<a src="https://img.shields.io/badge/%F0%9F%93%96-Files-red.svg?style=flat-square" href="https://drive.google.com/drive/folders/1nwBrHzLR1EIHSUA6pEwHI3LDMY2FiI7Q?role=writer">
<img src="https://img.shields.io/badge/%F0%9F%93%96-Files-red.svg?style=flat-square">
</a>

<a src="https://img.shields.io/badge/%F0%9F%8E%A4-Slides-blue.svg?style=flat-square" href="https://docs.google.com/presentation/d/1XuNOPoA5PbUCrv0Y8v3r3WWf204DvEbz/edit?usp=sharing">
<img src="https://img.shields.io/badge/%F0%9F%8E%A4-Slides-blue.svg?style=flat-square">
</a>

</div>

This is the repository of the Neurohackademy 2024 Project "Using Machine Learning to Classify Emotional States in the Human Connectome Project Dataset"


## Machine learning framework

The simplest possible machine learning (ML) framework we want to implement
is something like the following:

```mermaid
graph LR
    A[Brain Features] --> B[ML]
    B[ML] --> C[Emotion]
```

where we use features computed from brain structure / function / diffusion
data to predict emotional state.

### Data organization

We want brain features to be an $N\times M$ matrix of $N$ subjects and $M$
brain features. We want emotion to be a vector of length $N$ with some type
of emotion-relevant target to predict for each subejct (eg, class
label for the analysis clustering subjects according to their responses to
the NIH's emotion-focused toolkit).

We ideally want the data to be used for ML to be in CSVs with a column for
subject identifiers and one or more columns to be used in the ML model
(either features or outcome). For example:

| subject | brain_feature_1 | ... |
| :-----: | :-------------: | :--:|
| 100004 | ... | ... |
| ... | ... | ...|

### Data storage

The data to be used for ML can be stored in `./data/features`. Inside this
directory are subdirectories `iv/` and `dv`.

* Store brain features to be used as predictors in the model in
    `./data/features/ivs`.
* Store emotion-relevant data to be used as outcomes in the model in
    `./data/features/dv`.

It's great to include a text file or json to accompany the data giving a
description of what it is. For example, if the data you're adding is
`./data/features/ivs/brain_feature_1.csv`, add a text file at
`./data/features/ivs/brain_features_1.txt` giving a short description of
how you computed the data.
