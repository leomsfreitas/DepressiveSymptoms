# Detecção de Sinais de Depressão em Redes Sociais

> Comparação de abordagens de PLN para identificação automática de sintomas depressivos em publicações de redes sociais em português brasileiro.

Este repositório contém o código, os notebooks e os prompts utilizados no artigo **"Detecção de Sinais de Depressão em Redes Sociais por Meio de Modelos de Linguagem e Recursos de Análise de Sentimentos para o Português Brasileiro"**.

## Contexto

A depressão é um dos transtornos mentais de maior prevalência no mundo, e as redes sociais tornaram-se espaços de expressão emocional que permitem investigar sinais desse transtorno em larga escala. Este trabalho compara três abordagens de Processamento de Linguagem Natural (PLN) para a identificação automática de sintomas depressivos em publicações em português brasileiro, utilizando o corpus do [projeto AMIVE](https://www.amive.ufscar.br/).

## Corpus

O corpus do projeto AMIVE é composto por 780 postagens coletadas de páginas públicas de Segredos Universitários do Facebook. As postagens foram anotadas por especialistas em saúde mental segundo 21 sinais de depressão. Neste trabalho, foram consideradas apenas as classes com frequência mínima de 140 ocorrências, resultando em 9 sintomas:

| ID | Sintoma | Ocorrências |
|----|---------|-------------|
| C1 | Tristeza/Humor depressivo | 446 |
| C2 | Desamparo/Prejuízo social/Solidão | 333 |
| C3 | Suicídio/Auto-extermínio | 262 |
| C4 | Desvalia/Baixa autoestima | 212 |
| C5 | Preocupação/Medo/Ansiedade | 203 |
| C6 | Desesperança | 161 |
| C7 | Alteração na eficiência/funcionalidade | 146 |
| C8 | Irritação/Agressividade | 142 |
| C9 | Cansaço/Desânimo/Fadiga/Perda de energia | 141 |

## Abordagens Avaliadas

### 1. BERTimbau (*fine-tuning*)
*Fine-tuning* do [BERTimbau](https://huggingface.co/neuralmind/bert-base-portuguese-cased) para classificação *multilabel* dos 9 sintomas. Divisão: 65% treino / 20% teste / 15% validação.

### 2. AutoML com AutoGluon
Treinamento automatizado com a biblioteca [AutoGluon](https://auto.gluon.ai/), enriquecido com *features* afetivas derivadas de léxicos de sentimentos e do modelo GoEmotions adaptado para o português. Divisão: 65% treino / 20% teste / 15% validação.

Foram avaliadas cinco configurações independentes de *features*:

| Configuração | Descrição |
|---|---|
| Baseline | Apenas texto preprocessado |
| GE | Vetor completo de probabilidades do GoEmotions (27 emoções) |
| GEP | Polaridade agregada derivada do GoEmotions |
| Lex | Proporções de termos negativos, positivos e neutros (BP-LIWC2015, SentiLex-PT, WordNetAffectBR) |
| MI80 | Combinação de GE + GEP + Lex filtrada por informação mútua (21 *features* selecionadas) |

### 3. Qwen 2.5 14B (LLM)
Inferência com o modelo [Qwen 2.5](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct) (14B parâmetros) em regime *zero-shot* e *few-shot*, avaliado sobre o corpus completo.

## Resultados

Os resultados detalhados por sintoma e por abordagem estão disponíveis em [`results/README.md`](results/README.md).

Resumo comparativo (macro-F):

| Abordagem | Precisão | Cobertura | F1 | Custo computacional |
|---|---|---|---|---|
| BERTimbau (*fine-tuning*) | 0.78 | 0.64 | 0.69 | Medio |
| AutoGluon (GEP — melhor config.) | 0.71 | 0.69 | 0.69 | Baixo |
| Qwen 2.5 14B (*zero-shot*) | 0.63 | 0.68 | 0.59 | Alto |
| Qwen 2.5 14B (*few-shot*) | 0.71 | 0.61 | 0.62 | Alto |


## Estrutura do Repositório

```
.
├── notebooks/
│   ├── 1_eda.ipynb               # Análise exploratória do corpus
│   ├── 2_preprocessing.ipynb     # Pré-processamento textual
│   ├── 3a_feat_lexicons.ipynb    # Extração de features com léxicos (Lex)
│   ├── 3b_feat_ge.ipynb          # Extração de features com GoEmotions (GE e GEP)
│   ├── 3c_feat_selection.ipynb   # Seleção de features por informação mútua (MI80)
│   ├── 4a_automl.ipynb           # Treinamento e avaliação com AutoGluon
│   ├── 4b_bert.ipynb             # Fine-tuning e avaliação do BERTimbau
│   └── 4c_qwen_2.5_14B.ipynb     # Inferência com Qwen 2.5 14B
│
├── prompts/
│   ├── few_shot.txt              # Prompt para regime few-shot
│   └── zero_shot.txt             # Prompt para regime zero-shot
│
├── results/
│   └── README.md                 # Resultados tabulares completos por abordagem e sintoma
│
├── src/
│   ├── models/
│   │   ├── automl.py             # Classe do modelo AutoGluon
│   │   └── bert.py               # Classe do modelo BERTimbau
│   ├── pipeline/
│   │   ├── automl.py             # Pipeline de treino e avaliação AutoGluon
│   │   ├── bert.py               # Pipeline de treino e avaliação BERTimbau
│   │   └── llm.py                # Pipeline de inferência com LLM
│   └── utils/
│       ├── features.py           # Carregamento e merge das features com o corpus base
│       ├── map.py                # Mapeamento de classes e rótulos
│       ├── prompt.py             # Utilitários de construção de prompts
│       └── split.py              # Divisão treino/teste/validação
│
└── requirements.txt
```

## Instalação

```bash
git clone https://github.com/leomsfreitas/DepressiveSymptoms.git
cd DepressiveSymptoms
pip install -r requirements.txt
```

## Como Executar

Os notebooks estão numerados na ordem recomendada de execução:

```
2_preprocessing → 3a/3b/3c (features) → 4a/4b/4c (modelos)
```
O notebook `1_eda.ipynb` é exploratório e serviu como base para a construção do pipeline, não sendo necessário para reprodução dos experimentos.

O acesso ao corpus do projeto AMIVE é necessário para reprodução dos experimentos. Para solicitações de acesso ao corpus, consulte a [página do projeto](https://www.amive.ufscar.br/).

## Modelos Disponíveis

Os modelos treinados estão disponíveis para download no Google Drive:

| Modelo | Configuração | Download |
|--------|-------------|----------|
| BERTimbau (*fine-tuning*) | Classificação *multilabel* dos 9 sintomas | [Download](https://drive.google.com/file/d/1-3XRIsFIGMXtkOcY8TbGL8SkpbT3Fw3r/view?usp=sharing) |
| AutoGluon | Configuração GEP | [Download](https://drive.google.com/file/d/1vOvNS482qOvEnAwWUederzFYG4Z2KrE3/view?usp=sharing) |

> **Atenção:** para utilizar o modelo AutoGluon com GEP, é necessário extrair a *feature* GEP previamente. O notebook [`3b_feat_ge.ipynb`](notebooks/3b_feat_ge.ipynb) contém o pipeline completo de extração. O modelo espera como entrada um DataFrame com as colunas geradas por esse notebook.

## Citação

```
@misc{freitas2026depressao,
  title  = {Detecção de Sinais de Depressão em Redes Sociais por Meio de Modelos
            de Linguagem e Recursos de Análise de Sentimentos para o Português Brasileiro},
  author = {Freitas, Leo Marques Sabino de and Braga, Filipe Gioannini},
  year   = {2026},
  url    = {https://github.com/leomsfreitas/DepressiveSymptoms}
}
```

## Agradecimentos

Os autores agradecem à Prof. Dra. Helena Caseli (UFSCar) e à Prof. Dra. Eloize Seno (IFSP) pelo acesso aos servidores do projeto AMIVE, recurso essencial para a execução dos experimentos.
