""" Usage:
    <file-name> --in=IN_FILE --out=TRANS_FILE --lang=LANGUAGE [--debug]
"""
# External imports
import logging
import pdb
import json
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
from tqdm import tqdm
from typing import List, Dict
import pandas as pd
import string

# Local imports
from languages.util import GENDER, WB_GENDER_TYPES
#=-----

def calc_f1(precision: float, recall: float) -> float:
    """
    Compute F1 from precision and recall.
    """
    return 2 * (precision * recall) / (precision + recall)


def evaluate_correctness(source_df, trans_df, lang):
    correct_trans_cnt = defaultdict(lambda: 0)
    total_trans_cnt = defaultdict(lambda: 0)
    lang_prefix = 'en-'+str(lang)
    for i,j in trans_df:
        print(i,j)
    dict_sentences = {i.translate(str.maketrans('','',string.punctuation)):j for i,j in trans_df}

    dictionary_df = pd.read_csv('../data/translation dict/'+lang_prefix+'.oc_trans.dict.csv')
    dictionary = {series["Occupation"] : [series["Male"], series["Female"]] for idx, series in dictionary_df.iterrows()}
    none_cnt = 0
    for i, row in source_df.iterrows():
        try:
            if any(str(t_prof).lower().strip() in str(dict_sentences[row[0].translate(str.maketrans('','',string.punctuation))]).lower().replace('á', 'a').replace('é', 'e').replace('ó', 'o').replace("ä", "a").replace('.', '').strip().split(' ') \
                for t_prof in dictionary[row[2]][1-int(row[1]=="male")].split('|')):
                correct_trans_cnt[row[2]]+=1
                total_trans_cnt[row[2]]+=1
            elif any(str(t_prof).lower().strip() in str(dict_sentences[row[0].translate(str.maketrans('','',string.punctuation))]).lower().replace('á', 'a').replace('é', 'e').replace('ó', 'o').replace("ä", "a").replace('.', '').strip().split(' ') \
                for t_prof in dictionary[row[2]][1-int(row[1]=="female")].split('|')):
                    total_trans_cnt[row[2]]+=1
            else:
                # print(row[2])
                # print(str(dict_sentences[row[0].translate(str.maketrans('','',string.punctuation))]).lower().replace("ä", "a").strip().split(' '))
                # print(row[2], dictionary[row[2]][1-int(row[1]=="male")].split('|')) 
                none_cnt+=1
        except Exception as e:
            print(e)
            # print(str(dict_sentences[row[0].translate(str.maketrans('','',string.punctuation))]).lower().strip().split(' '))
            print(row[2], dictionary[row[2]])
            continue
    translation_acc = round(sum(correct_trans_cnt.values()) / sum(total_trans_cnt.values()) * 100, 1)
    output_dict = {"translation_acc": translation_acc}
    print(output_dict, none_cnt)

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    trans_fn = args["--out"]
    lang = args["--lang"]
    debug = args["--debug"]

    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)


    source_df = pd.read_csv(inp_fn, delimiter = '\t', header = None)
    full_bitext = [line.strip().split(" ||| ")
              for line in open(trans_fn, encoding = "utf8")]
    evaluate_correctness(source_df, full_bitext, lang)
    logging.info("DONE")
