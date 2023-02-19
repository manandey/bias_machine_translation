# Gender bias in Machine Translation
This repository contains the code and data of the paper [How sensitive are translation systems to extra contexts? Mitigating gender bias in Neural Machine Translation models through relevant contexts.](https://aclanthology.org/2022.findings-emnlp.143/)

## Overview
In this work, we investigate whether NMT models can be instructed to fix their bias during inference using targeted, guided instructions as contexts. By translating relevant contextual sentences during inference along with the input, we observe large improvements in reducing the gender bias in translations, across three popular test suites (WinoMT, BUG, SimpleGen). We further propose a novel metric to assess several large pre-trained models (OPUS-MT, M2M-100) on their sensitivity towards using contexts during translation to correct their biases. Our approach requires no fine-tuning and thus can be used easily in production systems to de-bias translations from stereotypical gender-occupation bias. We hope our method, along with our metric, can be used to build better, bias-free translation systems.

<p align="center">
  <img src="https://user-images.githubusercontent.com/6687858/196017253-6aa39e86-40ec-46f4-bbef-0ef0a638b486.png" width="80%"/>
</p>

## Results

We find that by the application of greedy strategy, the accuracy Ac is significantly high in the Table below, with the highest performance improvement in BUG dataset (87.36% for M2M-100 (German) compared with baseline 58.13%). This is a promising result, as even accounting for morphological and heuristic gender detection approximation, it is possible to effectively de-bias a gender stereotype of a profession in translation by adding extra context. <b>Therefore, for most sentences, there exists at least one template which is able to correct the bias</b>.

<p align="center">
  <img src="https://user-images.githubusercontent.com/6687858/196017483-98407192-1535-49c8-8bd9-96ef234c38fb.png" width="100%"/>
</p>

## Details of the data and code used in our experiments.
### Data:
Currently we use the following three datasets in our experiments: [WinoMT](https://github.com/gabrielStanovsky/mt_gender), [BUG](https://github.com/slab-nlp/bug) and [SimpleGEN](https://github.com/arendu-zz/SimpleGEN)

The data used in our experiments can be found here:
* Evaluation datasets are available in: `/data/base/`
* Context added datasets (eg.  "My nurse is a funny man" -> "My nurse is a funny man. Nurse is a male occupation") are available in: `/data/context/`

### Types of Context considered:
Currently, we consider the following combinations of contexts:
* Context Type - 1 (Factual)
  -> [occupation] is a [Male/Female] occupation.
* Context Type - 2 (Counterfactual)
 -> [occupation] is a [~ Male/Female] occupation.


### Translation Models:
The NMT models used in our experiments currently are:
* [Facebook M2M_100_418M](https://github.com/pytorch/fairseq/tree/master/examples/m2m_100)
* [Helsinki OPUS-MT](https://github.com/Helsinki-NLP/OPUS-MT-train)

The code for translation is available here: `/src/translate.py/`
The files containing the translations of all the datasets (WinoMT, BUG, SimpleGEN) in German, French and Spanish are available here:  `/translations`

### Word Aligners:
Currently we support the following word alligners:
* [fast_align](https://github.com/clab/fast_align)
* [awesome-align](https://github.com/neulab/awesome-align)

Install the above and use the path to its root in `/scripts/run_pipeline.sh`

### Morphological Taggers:
Currently we support the following morphological taggers:
* [Spacy - de_core_news_sm](https://spacy.io/models/de) 
* [Stanza](https://stanfordnlp.github.io/stanza/)

### Running the experiments:
The whole evaluation pipeline can be executed using the following command: 
`../scripts/run_pipeline.sh <path/to/input/file> <tgt_lang> <trans_function> <align_function> <morph_tagger>`

To calculate the final scores, the following scripts needs to be executed:
* `/src/post_processing.py` : Executing the script would generate the required CSV files used for analysis.
* `/src/calculate_scores.py`: Thereafter, executing this script would generate the relevant scores.

### Results:
The evaluation results are available here: `/results/`

## Citation
If you find this work useful, please cite the following reference:
```
@inproceedings{sharma-etal-2022-sensitive,
    title = "How sensitive are translation systems to extra contexts? Mitigating gender bias in Neural Machine Translation models through relevant contexts.",
    author = "Sharma, Shanya  and
      Dey, Manan  and
      Sinha, Koustuv",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2022",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.findings-emnlp.143",
    pages = "1968--1984",
    abstract = "Neural Machine Translation systems built on top of Transformer-based architectures are routinely improving the state-of-the-art in translation quality according to word-overlap metrics. However, a growing number of studies also highlight the inherent gender bias that these models incorporate during training, which reflects poorly in their translations. In this work, we investigate whether these models can be instructed to fix their bias during inference using targeted, guided instructions as contexts. By translating relevant contextual sentences during inference along with the input, we observe large improvements in reducing the gender bias in translations, across three popular test suites (WinoMT, BUG, SimpleGen). We further propose a novel metric to assess several large pre-trained models (OPUS-MT, M2M-100) on their sensitivity towards using contexts during translation to correct their biases. Our approach requires no fine-tuning, and thus can be used easily in production systems to de-bias translations from stereotypical gender-occupation bias. We hope our method, along with our metric, can be used to build better, bias-free translation systems.",
}
```
