# Resultados


## Overview


### Resumo Geral

| Abordagem | Precisão | Recall | F1 |
|:----------|:--------:|:------:|:--:|
| AutoGluon (Baseline) | 0.6937 | 0.6741 | 0.6798 |
| AutoGluon (Lex) | 0.6912 | 0.6663 | 0.6614 |
| AutoGluon (GE) | 0.6896 | 0.6552 | 0.6526 |
| AutoGluon (GEP) | **0.7063** | **0.6864** | **0.6882** |
| AutoGluon (MI80) | 0.7058 | 0.6874 | 0.6867 |
| BERTimbau (Fine-tuning) | **0.7801** | 0.6401 | 0.6867 |
| Qwen 2.5 72B (Zero-shot) | 0.5700 | 0.7100 | 0.5800 |
| Qwen 2.5 72B (Few-shot) | 0.6300 | 0.7000 | 0.6300 |


### F1 por Label

| Label | Baseline | Lex | GE | GEP | MI80 | BERT | Zero-shot | Few-shot |
|------:|---------:|----:|---:|----:|-----:|-----:|----------:|---------:|
| Tristeza/Humor depressivo | 0.7417 | 0.7432 | 0.7428 | 0.7519 | 0.7421 | 0.7838 | 0.67 | 0.77 |
| Desamparo/Solidão | 0.6930 | 0.7646 | 0.6799 | 0.7116 | **0.7763** | **0.8247** | 0.70 | 0.79 |
| Suicídio/Auto-extermínio | 0.7827 | 0.7824 | **0.8175** | 0.7885 | 0.7824 | 0.8000 | **0.87** | **0.87** |
| Desvalia/Baixa autoestima | 0.6910 | 0.6083 | 0.5744 | 0.6609 | **0.7287** | 0.7241 | 0.67 | 0.68 |
| Preocupação/Medo/Ansiedade | **0.8785** | 0.8486 | **0.8785** | 0.8745 | 0.8745 | 0.8475 | 0.79 | 0.76 |
| Desesperança | 0.5992 | 0.6298 | 0.5298 | 0.5945 | **0.6351** | 0.4615 | 0.46 | 0.51 |
| Alteração na eficiência/funcionalidade | **0.6291** | 0.5338 | 0.5445 | 0.6040 | 0.5833 | 0.4242 | 0.36 | 0.35 |
| Irritação/Agressividade | 0.6238 | 0.5727 | 0.5912 | **0.6626** | 0.5919 | 0.6000 | 0.39 | 0.52 |
| Cansaço/Fadiga/Perda de energia | 0.4794 | 0.4695 | 0.5144 | **0.5454** | 0.4659 | 0.7143 | 0.32 | 0.42 |
| **Macro** | 0.6798 | 0.6614 | 0.6526 | **0.6882** | 0.6867 | 0.6867 | 0.5800 | 0.6300 |


## Macro Average

### AutoGluon (Baseline)

| label | precision | recall | f1-score | support |
|------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.7799 | 0.7230 | 0.7417 | 237 |
| Desamparo/Solidão | 0.7191 | 0.6772 | 0.6930 | 237 |
| Suicídio/Auto-extermínio | 0.8319 | 0.7516 | 0.7827 | 237 |
| Desvalia/Baixa autoestima | 0.6824 | 0.7012 | 0.6910 | 237 |
| Preocupação/Medo/Ansiedade | 0.9041 | 0.8570 | 0.8785 | 237 |
| Desesperança | 0.6085 | 0.5921 | 0.5992 | 237 |
| Alteração na eficiência/funcionalidade | 0.6319 | 0.6265 | 0.6291 | 237 |
| Irritação/Agressividade | 0.6070 | 0.6587 | 0.6238 | 237 |
| Cansaço/Fadiga/Perda de energia | 0.4789 | 0.4798 | 0.4794 | 237 |


### AutoGluon (Lex)

| label | precision | recall | f1-score | support |
|------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.8048 | 0.7195 | 0.7432 | 235 |
| Desamparo/Solidão | 0.8777 | 0.7219 | 0.7646 | 235 |
| Suicídio/Auto-extermínio | 0.8315 | 0.7514 | 0.7824 | 235 |
| Desvalia/Baixa autoestima | 0.6043 | 0.6869 | 0.6083 | 235 |
| Preocupação/Medo/Ansiedade | 0.9060 | 0.8093 | 0.8486 | 235 |
| Desesperança | 0.6118 | 0.6789 | 0.6298 | 235 |
| Alteração na eficiência/funcionalidade | 0.5669 | 0.5290 | 0.5338 | 235 |
| Irritação/Agressividade | 0.5641 | 0.6134 | 0.5727 | 235 |
| Cansaço/Fadiga/Perda de energia | 0.4541 | 0.4860 | 0.4695 | 235 |


### AutoGluon (GE)

| label | precision | recall | f1-score | support |
|------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.7918 | 0.7214 | 0.7428 | 237 |
| Desamparo/Solidão | 0.7312 | 0.6579 | 0.6799 | 237 |
| Suicídio/Auto-extermínio | 0.8724 | 0.7822 | 0.8175 | 237 |
| Desvalia/Baixa autoestima | 0.5873 | 0.6720 | 0.5744 | 237 |
| Preocupação/Medo/Ansiedade | 0.9041 | 0.8570 | 0.8785 | 237 |
| Desesperança | 0.5354 | 0.5273 | 0.5298 | 237 |
| Alteração na eficiência/funcionalidade | 0.6234 | 0.5362 | 0.5445 | 237 |
| Irritação/Agressividade | 0.5788 | 0.6257 | 0.5912 | 237 |
| Cansaço/Fadiga/Perda de energia | 0.5821 | 0.5169 | 0.5144 | 237 |


### AutoGluon (GEP)

| label | precision | recall | f1-score | support |
|------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.8253 | 0.7254 | 0.7519 | 235 |
| Desamparo/Solidão | 0.6988 | 0.7711 | 0.7116 | 235 |
| Suicídio/Auto-extermínio | 0.8456 | 0.7539 | 0.7885 | 235 |
| Desvalia/Baixa autoestima | 0.6631 | 0.6588 | 0.6609 | 235 |
| Preocupação/Medo/Ansiedade | 0.9162 | 0.8427 | 0.8745 | 235 |
| Desesperança | 0.5856 | 0.6098 | 0.5945 | 235 |
| Alteração na eficiência/funcionalidade | 0.6280 | 0.5902 | 0.6040 | 235 |
| Irritação/Agressividade | 0.6514 | 0.6769 | 0.6626 | 235 |
| Cansaço/Fadiga/Perda de energia | 0.5430 | 0.5485 | 0.5454 | 235 |


### AutoGluon (MI80)

| label | precision | recall | f1-score | support |
|------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.7909 | 0.7210 | 0.7421 | 235 |
| Desamparo/Solidão | 0.8126 | 0.7530 | 0.7763 | 235 |
| Suicídio/Auto-extermínio | 0.8315 | 0.7514 | 0.7824 | 235 |
| Desvalia/Baixa autoestima | 0.7287 | 0.7287 | 0.7287 | 235 |
| Preocupação/Medo/Ansiedade | 0.9162 | 0.8427 | 0.8745 | 235 |
| Desesperança | 0.6218 | 0.6562 | 0.6351 | 235 |
| Alteração na eficiência/funcionalidade | 0.6133 | 0.5698 | 0.5833 | 235 |
| Irritação/Agressividade | 0.5841 | 0.6852 | 0.5919 | 235 |
| Cansaço/Fadiga/Perda de energia | 0.4535 | 0.4790 | 0.4659 | 235 |


### BERTimbau (Fine-tuning)

| classe | precision | recall | f1-score | support |
|-------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.7160 | 0.8657 | 0.7838 | 67 |
| Desamparo/Solidão | 0.8511 | 0.8000 | 0.8247 | 50 |
| Suicídio/Auto-extermínio | 0.8333 | 0.7692 | 0.8000 | 39 |
| Desvalia/Baixa autoestima | 0.8077 | 0.6562 | 0.7241 | 32 |
| Preocupação/Medo/Ansiedade | 0.8621 | 0.8333 | 0.8475 | 30 |
| Desesperança | 0.6000 | 0.3750 | 0.4615 | 24 |
| Alteração na eficiência/funcionalidade | 0.6364 | 0.3182 | 0.4242 | 22 |
| Irritação/Agressividade | 1.0000 | 0.4286 | 0.6000 | 21 |
| Cansaço/Fadiga/Perda de energia | 0.7143 | 0.7143 | 0.7143 | 21 |
| **macro avg** | **0.7801** | **0.6401** | **0.6867** | **306** |

### Qwen 2.5 72B (Zero shot)

| classe | precision | recall | f1-score | support |
|-------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.54 | 0.88 | 0.67 | 446 |
| Desamparo/Solidão | 0.57 | 0.90 | 0.70 | 333 |
| Suicídio/Auto-extermínio | 0.83 | 0.91 | 0.87 | 262 |
| Desvalia/Baixa autoestima | 0.61 | 0.76 | 0.67 | 212 |
| Preocupação/Medo/Ansiedade | 0.70 | 0.91 | 0.79 | 203 |
| Desesperança | 0.36 | 0.63 | 0.46 | 161 |
| Alteração na eficiência/funcionalidade | 0.46 | 0.30 | 0.36 | 146 |
| Irritação/Agressividade | 0.88 | 0.25 | 0.39 | 142 |
| Cansaço/Fadiga/Perda de energia | 0.20 | 0.87 | 0.32 | 141 |
| **macro avg** | **0.57** | **0.71** | **0.58** | **2046** |


### Qwen 2.5 72B (Few shot)

| classe | precision | recall | f1-score | support |
|-------:|----------:|-------:|---------:|--------:|
| Tristeza/Humor depressivo | 0.75 | 0.79 | 0.77 | 446 |
| Desamparo/Solidão | 0.79 | 0.79 | 0.79 | 333 |
| Suicídio/Auto-extermínio | 0.82 | 0.92 | 0.87 | 262 |
| Desvalia/Baixa autoestima | 0.61 | 0.76 | 0.68 | 212 |
| Preocupação/Medo/Ansiedade | 0.66 | 0.89 | 0.76 | 203 |
| Desesperança | 0.43 | 0.64 | 0.51 | 161 |
| Alteração na eficiência/funcionalidade | 0.55 | 0.26 | 0.35 | 146 |
| Irritação/Agressividade | 0.77 | 0.39 | 0.52 | 142 |
| Cansaço/Fadiga/Perda de energia | 0.28 | 0.84 | 0.42 | 141 |
| **macro avg** | **0.63** | **0.70** | **0.63** | **2046** |