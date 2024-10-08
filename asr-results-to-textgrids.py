import glob
import pandas as pd
import os
import json
import numpy as np
import tgt
import librosa
import argparse

def readWhisperToutputJSON(jsonFile):
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    return data

def obj2interval(obj):
    start = obj['start']
    end = obj['end']
    txt = obj['text']

    return tgt.core.Interval(start, end, text=txt)

def obj2intervalConf(obj):
    start = obj['start']
    end = obj['end']
    txt = str(obj['confidence'])

    return tgt.core.Interval(start, end, text=txt)


def run(args):

    jsonAsrResultsDir = args.jsonAsrResultsDir
    audioDir = args.audioDir

    # List input files
    jsonAsrResultsList = glob.glob(os.path.join(jsonAsrResultsDir, '*.json'))

    # Create output directory
    outputDir = jsonAsrResultsDir.replace('json-asr-results', 'json-asr-results-as-tg')
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Convert each json file to a TextGrid file
    for jsonAsrResult in jsonAsrResultsList:

        # Get basename of file
        basename = os.path.basename(jsonAsrResult).replace('.json', '')

        # Read JSON file
        data = readWhisperToutputJSON(jsonAsrResult)

        # Extract duration of corresponding audio file
        audioPath = os.path.join(audioDir, basename + '.mp3')
        y, sr = librosa.load(audioPath, sr=16000)
        durLibrosa = librosa.get_duration(y=y, sr=sr)

        # Extract features from JSON file
        segments = data['segments']

        try:

            # Create Segment Tier
            segments_intervals = [obj2interval(segment) for segment in segments]
            segmentsTier = tgt.core.IntervalTier(start_time=0.0, end_time=durLibrosa, name='segments', objects=None)
            segmentsTier.add_intervals(segments_intervals)

            # Create Words Tier (with disfluecies)
            items = [segment['words'] for segment in segments]
            items_flatten = [word for words_segment in items for word in words_segment]
            items_flatten_intervals = [obj2interval(obj) for obj in items_flatten]
            wordsDisTier = tgt.core.IntervalTier(start_time=0.0, end_time=durLibrosa, name='wordsDis', objects=None)
            wordsDisTier.add_intervals(items_flatten_intervals)

            # Create Words Tier (without disfluecies)
            words = [item for item in items_flatten if item['text'] != "[*]"]
            words_intervals = [obj2interval(obj) for obj in words]
            wordsTier = tgt.core.IntervalTier(start_time=0.0, end_time=durLibrosa, name='words', objects=None)
            wordsTier.add_intervals(words_intervals)

            # Create words confidence score tier
            conf_intervals = [obj2intervalConf(obj) for obj in words]
            confTier = tgt.core.IntervalTier(start_time=0.0, end_time=durLibrosa, name='conf', objects=None)
            confTier.add_intervals(conf_intervals)

            # Add all tiers to TextGrid
            tg = tgt.core.TextGrid()
            tg.add_tier(wordsDisTier)
            tg.add_tier(wordsTier)
            tg.add_tier(confTier)
            tg.add_tier(segmentsTier)

            # Write TextGrid
            outputFile = os.path.join(outputDir, basename + '.TextGrid')
            tgt.io.write_to_file(tg, outputFile, format='long', encoding='utf-8')

        except:

            print("Creating TextGrid not possible:", basename)

def main():
    parser = argparse.ArgumentParser("Message")
    parser.add_argument("--jsonAsrResultsDir", type=str, help = "Path to json-asr-results directory.")
    parser.add_argument("--audioDir", type=str, help = "Path to audio directory.")

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()