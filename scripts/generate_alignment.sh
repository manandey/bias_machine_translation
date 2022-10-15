#!/bin/bash
# Usage:
#   evaluate_language.sh <corpus> <lang-code> <translation system>
#
# e.g.,
# ../scripts/evaluate_language.sh ../data/agg/en.txt es google

set -e

mkdir -p ../gi/alignments/
# Parse parameters
trans_dataset=$1
lang=$2
align_sys=$3
prefix=en-$lang
align_fn=$align_sys/forward.$prefix.align
dest=../gi/alignments/$align_sys/$trans_sys/
# Align

if [ $3 = "fast_align" ]; then
    align_fn=forward.$prefix.align
    <path_to_fast_align>/build/fast_align -i $trans_dataset -d -o -v > $align_fn
    mv -i $align_fn $dest
else
    awesome-align \
    --output_file=$dest/$align_fn \
    --model_name_or_path=bert-base-multilingual-cased \
    --data_file=$trans_dataset \
    --extraction 'softmax' \
    --cache_dir ../cache/ \
    --batch_size 32 
fi;