#!/bin/bash

set -euo pipefail

LANGUAGE=$1

# save-interval
SNT=$2

# Max-update
MXU=$3

# Batch size
BTS=$4

SEED=$5
CURRENT_DIR=$6

DATABIN="${CURRENT_DIR}/data-bin"
CKPTS="${CURRENT_DIR}/checkpoints"

# Encoder embedding dim.
EED=256
#EED=512
# Encoder hidden layer size.
EHS=1024
# Encoder number of layers.
ENL=4
# Encoder number of attention heads.
EAH=4
# Decoder embedding dim.
DED=256
#DED=512
# Decoder hidden layer size.
DHS=1024
# Decoder number of layers.
DNL=4
# Decoder number of attention heads.
DAH=4
# Dropout
DRP=0.3

# Warmup update
WMU=4000
# Learning rate
LRT=0.001
# Label smoothing
LST=0.1
# clip-norm
CNM=1.0


fairseq-train "${DATABIN}/${LANGUAGE}" \
    --task=translation \
    --source-lang="${LANGUAGE}.input" \
    --target-lang="${LANGUAGE}.output" \
    --save-dir="${CKPTS}/${LANGUAGE}-models" \
    --dropout="${DRP}" \
    --attention-dropout="${DRP}" \
    --activation-dropout="${DRP}" \
    --arch=transformer \
    --activation-fn=relu \
    --encoder-embed-dim="${EED}" \
    --encoder-ffn-embed-dim="${EHS}" \
    --encoder-layers="${ENL}" \
    --encoder-attention-heads="${EAH}" \
    --encoder-normalize-before \
    --decoder-embed-dim="${DED}" \
    --decoder-ffn-embed-dim="${DHS}" \
    --decoder-layers="${DNL}" \
    --decoder-attention-heads="${DAH}" \
    --decoder-normalize-before \
    --share-decoder-input-output-embed \
    --optimizer=adam \
    --adam-betas='(0.9, 0.98)' \
    --clip-norm="${CNM}" \
    --lr="${LRT}" \
    --lr-scheduler=inverse_sqrt \
    --warmup-updates="${WMU}" \
    --criterion=label_smoothed_cross_entropy \
    --label-smoothing="${LST}" \
    --batch-size="${BTS}" \
    --max-update="${MXU}" \
    --save-interval="${SNT}" \
    --seed="${SEED}"
