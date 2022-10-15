# Gender bias in Machine Translation
This repository contains code and data for our experiments to evaluate gender bias in Machine Translation

## Data:
We use the following data for our experiments:
* The evaluation datasets available in `mt_bias/data/base/`
* Context added to the data. eg.  "My nurse is a funny man" -> "My nurse is a funny man. Nurse is a male occupation" available in `mt_bias/data/context/`

## Types of Context considered:
Currently, we consider the following 6 combinations of context:
* Context Type - 1 (Factual)
  -> [occupation] is a [Male/Female] occupation.
* Context Type - 2 (Counterfactual)
 -> [occupation] is a [~ Male/Female] occupation.


## Translation Models:
Currently, we support two NMT models:
* [Facebook M2M_100_418M](https://github.com/pytorch/fairseq/tree/master/examples/m2m_100)
* [Helsinki OPUS-MT](https://github.com/Helsinki-NLP/OPUS-MT-train)

The code for translation can be found here: `mt_bias/src/translate.py/`
The results from translation will be found in `mt_bias/translations`

## Word Aligners:
Currently we support the following word alligners
* [fast_align](https://github.com/clab/fast_align)
* [awesome-align](https://github.com/neulab/awesome-align)

Install the above and use the path to its root in `mt_bias/scripts/run_pipeline.sh`

## Morphological Taggers:
Currently we support the following morphological taggers
* [Spacy - de_core_news_sm](https://spacy.io/models/de) `python -m spacy download de_core_news_sm`
* [Stanza](https://stanfordnlp.github.io/stanza/)

### Running the experiments:
To execute the whole evaluation pipeline, use the command: 
`../scripts/run_pipeline.sh <path/to/input/file> <tgt_lang> <trans_function> <align_function> <morph_tagger>`

To calculate the scores, use the following scripts:
`mt_bias/src/post_processing.py`
This woud create the required CSVs used for analysis. Post this the following script can be used to find the releavnt scores
`mt_bias/src/calculate_scores.py`


### Results:
You can find the evaluation results at: `mt_bias/results/`
