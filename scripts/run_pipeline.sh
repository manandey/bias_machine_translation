set -e

# Parse parameters
datapath=$1
dataset=$2
lang=$3
trans_sys=$4
align_sys=$5
morph_fn=$6
prefix=en-$lang

align_fn=forward.$prefix.align
align_dest=../alignments/$dataset/$align_sys/$trans_sys/

# Prepare files for translation
cut -f3 $datapath > ./tmp.in            # Extract sentences
mkdir -p ../translations/$dataset/$trans_sys/
mkdir -p $align_dest

# Translate
trans_fn=../translations/$dataset/$trans_sys/$prefix.txt
echo "!!! $trans_fn"
if [ ! -f $trans_fn ]; then
    python3 translate.py --trans=$trans_sys --in=./tmp.in --src=en --tgt=$2 --out=$trans_fn
else
    echo "Not translating since translation file exists: $trans_fn"
fi

# Align
if [ $4 = "fast_align" ]; then
    align_fn=forward.$prefix.align
    <path_to_fast_align>/fast_align/build/fast_align -i $trans_fn -d -o -v > $align_fn
    mv -i $align_fn $align_dest
else
     if [ -f $align_dest/$align_fn ]; then
        echo "The alignment file already exists. Delete the existing one if you want a new one created"
    else
        awesome-align \
        --output_file=$align_dest/$align_fn \
        --model_name_or_path=bert-base-multilingual-cased \
        --data_file=$trans_fn \
        --extraction 'softmax' \
        --cache_dir ../cache/ \
        --batch_size 32 
    fi
fi;

# Evaluate
mkdir -p ../results/$dataset/$trans_sys/
out_fn=../results/$dataset/$trans_sys/${lang}.pred.csv
python3 load_alignments.py --dsp=$datapath --ds=$dataset --bi=$trans_fn --align=$align_dest$align_fn --lang=$lang --out=$out_fn --morph=$morph_fn --batch_size=1