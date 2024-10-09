# Repository: features-from-ASR-results

Author: Wieke Harmsen
Date: 9 October 2024

This repository contains scripts to analyse ASR results.
Run uber.sh to run the scripts: `./uber.sh`

`asr-results-to-textgrids.py`
- *Input*: This script reads a directory with json files. Each json file is a [WhisperTimestamped](https://github.com/linto-ai/whisper-timestamped) AsrResult, where disfluency detection was enabled.
- *Output*: Each json file is converted into a TextGrid file with four tiers: wordsDis, words, conf, segments. 

`asr-results-to-file-features.py`
- *Input*: This script reads a directory with json files. Each json file is a [WhisperTimestamped](https://github.com/linto-ai/whisper-timestamped) AsrResult, where disfluency detection was enabled.
- *Output*: Each json file is converted into a list of features, capturing statistics (e.g., min, mean, median, max) of word duration, speech rate, articulation rate, confidence scores, etc. Many features have the suffix "2". This means that disfluencies are not seen as pauses. When inspecting the textgrids generated above, disfluency markers often marked speech of other persons or noise in the background. So, these markers do not capture information about someone's oral reading fluency.

