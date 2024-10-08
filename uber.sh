#!/bin/bash

# Set base dir to the main data directory
basePath=/vol/bigdata3/datasets3/dutch_child_audio/dart/preposttest_final/

audioDir=$basePath/02_audio_renamed
expDir=$basePath/05_asr_experiments/whispert_dis_prompts # choose between whispert_dis_prompts or whispert_dis
asrResultsDir=$expDir/json-asr-results

# python3 ./asr-results-to-file-features.py --jsonAsrResultsDir $asrResultsDir
python3 ./asr-results-to-textgrids.py --jsonAsrResultsDir $asrResultsDir --audioDir $audioDir

