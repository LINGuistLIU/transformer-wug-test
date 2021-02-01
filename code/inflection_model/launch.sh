#!/bin/bash

set -euo pipefail

SAVE=10
MAX_UPDATES=20000
BATCH=400

CURRENT_DIR=PATH_TO_CURRENT_WORKING_DIRECTORY
SEED=1

#for SEED in 1 2 3 4 5;
for FOLD in 1 2 3 4 5;
do
	DATADIR=$CURRENT_DIR/data_niger_congo_fulltable/data_niger_congo$FOLD
#	for LANG in czech finnish german russian spanish turkish;
	for LANG in aka nya swa gaa lin sot;
	do
		LANGUAGE=$LANG$FOLD
	    $CURRENT_DIR/src/pipeline_inflection.sh $LANGUAGE $SAVE $MAX_UPDATES $BATCH $SEED $DATADIR/$LANGUAGE $CURRENT_DIR
		mv $CURRENT_DIR/checkpoints/$LANGUAGE-models $CURRENT_DIR/checkpoints/$LANGUAGE-models$FOLD
		mv $CURRENT_DIR/checkpoints/$LANGUAGE-predictions $CURRENT_DIR/checkpoints/$LANGUAGE-predictions$FOLD
		
		mv $CURRENT_DIR/data-bin/$LANGUAGE $CURRENT_DIR/data-bin/$LANGUAGE$FOLD
	done
done

