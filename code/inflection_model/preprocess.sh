#!/bin/bash

LANGUAGE=$1
DATADIR=$2
CURRENT_DIR=$3

fairseq-preprocess \
    --source-lang="${LANGUAGE}.input" \
    --target-lang="${LANGUAGE}.output" \
    --trainpref="${DATADIR}/train" \
    --validpref="${DATADIR}/dev" \
    --testpref="${DATADIR}/test" \
    --tokenizer=space \
    --thresholdsrc=1 \
    --thresholdtgt=1 \
    --workers=20 \
    --destdir="${CURRENT_DIR}/data-bin/${LANGUAGE}/"