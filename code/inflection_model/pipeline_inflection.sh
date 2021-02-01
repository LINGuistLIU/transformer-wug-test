#!/bin/bash

set -euo pipefail

LANGUAGE=$1
SAVE=$2
MAX_UPDATES=$3
BATCH=$4
SEED=$5
DATADIR=$6
CURRENT_DIR=$7

TIME_DIR=$CURRENT_DIR/timeinfo
mkdir -p $TIME_DIR
TIME_FILE=$TIME_DIR/$LANGUAGE.time

CKPNT_DIR=$CURRENT_DIR/checkpoints

echo "--------${LANGUAGE}--------" >> $TIME_FILE

convertsecs() {
  ((h=${1}/3600))
  ((m=(${1}%3600)/60))
  ((s=${1}%60))
  printf "%02d:%02d:%02d\n" $h $m $s
 }

STARTLANG=$(date +%s)

$CURRENT_DIR/src/preprocess.sh $LANGUAGE $DATADIR $CURRENT_DIR

STARTTIME=$(date +%s)
$CURRENT_DIR/src/train.sh $LANGUAGE $SAVE $MAX_UPDATES $BATCH $SEED $CURRENT_DIR
ENDTIME=$(date +%s)
((t=ENDTIME-STARTTIME))

echo "Training takes $(convertsecs $t)" >> $TIME_FILE

STARTTIME=$(date +%s)
$CURRENT_DIR/src/generate.sh $LANGUAGE dev $CURRENT_DIR
ENDTIME=$(date +%s)
((t=ENDTIME-STARTTIME))

echo "Generating for dev set takes $(convertsecs $t)" >> $TIME_FILE

STARTTIME=$(date +%s)
$CURRENT_DIR/src/generate.sh $LANGUAGE test $CURRENT_DIR
ENDTIME=$(date +%s)
((t=ENDTIME-STARTTIME))

echo "Generating for test set takes $(convertsecs $t)" >> $TIME_FILE

ENDLANG=$(date +%s)
((t=ENDLANG-STARTLANG))
echo "${LANGUAGE}: In total, it takes $(convertsecs $t)" >> $TIME_FILE

rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint1*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint2*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint3*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint4*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint5*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint6*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint7*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint8*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint9*.pt
rm -rf $CKPNT_DIR/$LANGUAGE-models/checkpoint0*.pt

