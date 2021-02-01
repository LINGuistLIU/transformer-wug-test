#!/bin/bash

locale -a

set -euo pipefail

LANGUAGE=$1
TYPE=$2 # dev or test
CURRENT_DIR=$3

DATABIN="${CURRENT_DIR}/data-bin"
CKPTS="${CURRENT_DIR}/checkpoints"

CHECKPOINT_DIR="${CKPTS}/${LANGUAGE}-models"
PRED="${CKPTS}/${LANGUAGE}-predictions/test"

mkdir -p "${CKPTS}/${LANGUAGE}-predictions"

if [[ "${TYPE}" == "dev" ]]; then
    TYPE=valid
    PRED="${CKPTS}/${LANGUAGE}-predictions/dev"
fi

MODEL=checkpoint_best.pt

LC_ALL=en_US.UTF-8 fairseq-generate \
      "${DATABIN}/${LANGUAGE}" \
      --gen-subset="${TYPE}" \
      --source-lang="${LANGUAGE}.input" \
      --target-lang="${LANGUAGE}.output" \
      --path="${CHECKPOINT_DIR}/${MODEL}" \
      --batch-size=128 \
      --beam=5 \
      > "${PRED}-${MODEL}.txt"
