# Detection of Depression Signs on Social Media

> Comparison of NLP approaches for automatically identifying depressive symptoms in Brazilian Portuguese social media posts.

This repository contains the code, notebooks, and prompts used in the paper **"Detecção de Sinais de Depressão em Redes Sociais por Meio de Modelos de Linguagem e Recursos de Análise de Sentimentos para o Português Brasileiro"**.

## Background

Depression is one of the most prevalent mental disorders worldwide, and social media has become a space for emotional expression that allows researchers to investigate signs of this disorder at scale. This work compares three Natural Language Processing (NLP) approaches for automatically identifying depressive symptoms in Brazilian Portuguese posts, using the corpus from the [AMIVE project](https://www.amive.ufscar.br/).

## Corpus

The AMIVE project corpus consists of 780 posts collected from public Facebook "Segredos Universitários" (University Secrets) pages. The posts were annotated by mental health specialists according to 21 signs of depression. In this work, only classes with a minimum frequency of 140 occurrences were considered, resulting in 9 symptoms:

| Symptom | Occurrences |
|---------|-------------|
| Sadness/Depressed mood | 446 |
| Helplessness/Social impairment/Loneliness | 333 |
| Suicide/Self-harm | 262 |
| Worthlessness/Low self-esteem | 212 |
| Worry/Fear/Anxiety | 203 |
| Hopelessness | 161 |
| Change in efficiency/functionality | 146 |
| Irritability/Aggressiveness | 142 |
| Tiredness/Listlessness/Fatigue/Loss of energy | 141 |

## Approaches Evaluated

### 1. BERTimbau (fine-tuning)
Fine-tuning of [BERTimbau](https://huggingface.co/neuralmind/bert-base-portuguese-cased) for multilabel classification of the 9 symptoms. Split: 65% train / 20% test / 15% validation.

### 2. AutoML with AutoGluon
Automated training with the [AutoGluon](https://auto.gluon.ai/) library, enriched with affective features derived from sentiment lexicons and the GoEmotions model adapted for Portuguese. Split: 65% train / 20% test / 15% validation.

Five independent feature configurations were evaluated:

| Configuration | Description |
|---|---|
| Baseline | Preprocessed text only |
| GE | Full vector of GoEmotions probabilities (27 emotions) |
| GEP | Aggregated polarity derived from GoEmotions |
| Lex | Proportions of negative, positive, and neutral terms (BP-LIWC2015, SentiLex-PT, WordNetAffectBR) |
| MI80 | Combination of GE + GEP + Lex filtered by mutual information (21 selected features) |

### 3. Qwen 2.5 72B (LLM)
Inference with the [Qwen 2.5](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct-AWQ) model (72B parameters, 4-bit quantized via AWQ) in zero-shot and few-shot regimes, evaluated on the full corpus.

## Results

Detailed results by symptom and approach are available in [`results/README.md`](results/README.md).

Comparative summary (macro-F):

| Approach | Precision | Recall | F1 | Computational cost |
|---|---|---|---|---|
| BERTimbau (fine-tuning) | 0.78 | 0.64 | 0.69 | Medium |
| AutoGluon (GEP — best config.) | 0.71 | 0.69 | 0.69 | Low |
| Qwen 2.5 72B (zero-shot) | 0.57 | 0.71 | 0.58 | High |
| Qwen 2.5 72B (few-shot) | 0.63 | 0.70 | 0.63 | High |


## Repository Structure

```
.
├── data/
│   └── lexicons/
│       ├── liwc.csv              # BP-LIWC2015 — psycholinguistic lexicon for Brazilian Portuguese
│       ├── sentilex.csv          # SentiLex-PT — polarity lexicon for Portuguese
│       └── wordnetaffect.csv     # WordNetAffectBR — emotion lexicon for Portuguese
│
├── notebooks/
│   ├── 1_eda.ipynb               # Exploratory analysis of the corpus
│   ├── 2_preprocessing.ipynb     # Text preprocessing
│   ├── 3a_feat_lexicons.ipynb    # Feature extraction with lexicons (Lex)
│   ├── 3b_feat_ge.ipynb          # Feature extraction with GoEmotions (GE and GEP)
│   ├── 3c_feat_selection.ipynb   # Feature selection by mutual information (MI80)
│   ├── 4a_automl.ipynb           # Training and evaluation with AutoGluon
│   ├── 4b_bert.ipynb             # Fine-tuning and evaluation of BERTimbau
│   └── 4c_qwen_2.5_72B.ipynb     # Inference with Qwen 2.5 72B
│
├── prompts/
│   ├── few_shot.txt              # Prompt for the few-shot regime
│   └── zero_shot.txt             # Prompt for the zero-shot regime
│
├── results/
│   └── README.md                 # Full tabular results by approach and symptom
│
├── src/
│   ├── models/
│   │   ├── automl.py             # AutoGluon model class
│   │   └── bert.py               # BERTimbau model class
│   ├── pipeline/
│   │   ├── automl.py             # AutoGluon training and evaluation pipeline
│   │   ├── bert.py               # BERTimbau training and evaluation pipeline
│   │   └── llm.py                # LLM inference pipeline
│   └── utils/
│       ├── features.py           # Loading and merging features with the base corpus
│       ├── map.py                # Class and label mapping
│       ├── prompt.py             # Prompt-building utilities
│       └── split.py              # Train/test/validation split
│
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/leomsfreitas/DepressiveSymptoms.git
cd DepressiveSymptoms
pip install -r requirements.txt
```

## How to Run

The notebooks are numbered in the recommended order of execution:

```
2_preprocessing → 3a/3b/3c (features) → 4a/4b/4c (models)
```
The `1_eda.ipynb` notebook is exploratory and served as a basis for building the pipeline; it is not required to reproduce the experiments.

Access to the AMIVE project corpus is required to reproduce the experiments. For corpus access requests, see the [project page](https://www.amive.ufscar.br/).

## Available Models

The trained models are available for download on Google Drive:

| Model | Configuration | Download |
|--------|-------------|----------|
| BERTimbau (fine-tuning) | Multilabel classification of the 9 symptoms | [Download](https://drive.google.com/file/d/1-3XRIsFIGMXtkOcY8TbGL8SkpbT3Fw3r/view?usp=sharing) |
| AutoGluon | GEP configuration | [Download](https://drive.google.com/file/d/1vOvNS482qOvEnAwWUederzFYG4Z2KrE3/view?usp=sharing) |

> **Note:** to use the AutoGluon model with GEP, the GEP feature must be extracted beforehand. The [`3b_feat_ge.ipynb`](notebooks/3b_feat_ge.ipynb) notebook contains the full extraction pipeline. The model expects a DataFrame with the columns generated by that notebook as input.

## Citation

```
@misc{freitas2026depressao,
  title  = {Detecção de Sinais de Depressão em Redes Sociais por Meio de Modelos
            de Linguagem e Recursos de Análise de Sentimentos para o Português Brasileiro},
  author = {Freitas, Leo Marques Sabino de and Braga, Filipe Gioannini},
  year   = {2026},
  url    = {https://github.com/leomsfreitas/DepressiveSymptoms}
}
```

## Authors

- **Leo Marques Sabino de Freitas** — [@leomsfreitas](https://github.com/leomsfreitas)
- **Filipe Gioannini Braga** — [@FilipeBrag](https://github.com/FilipeBrag)

## Acknowledgments

The authors thank Prof. Dr. Helena Caseli (UFSCar) and Prof. Dr. Eloize Seno (IFSP) for access to the AMIVE project servers, an essential resource for carrying out the experiments.
