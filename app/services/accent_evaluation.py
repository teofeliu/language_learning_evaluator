# app/services/accent_evaluation.py

from transformers import pipeline
from pathlib import Path
import math

# Initialize the pipeline with the audio classification model
pipe = pipeline("audio-classification", model="dima806/speech-accent-classification")

async def evaluate_accent(audio_path):
    if not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if not audio_path.endswith('.mp3'):
        raise ValueError("The audio file must be in MP3 format for accent evaluation.")

    results = pipe(audio_path)

    # Find the score for "Native"
    native_score = next((result['score'] for result in results if result['label'] == 'Native'), None)

    if native_score is None:
        raise ValueError("Unable to determine native accent score.")

    # Convert the score to an integer percentage
    return normalize_accents(native_score)

import math
def normalize_accents(x):
    if x > 0.5:
        return -(2 / (1 + math.exp(-2955 + 2992.5*x))) + 10
    else:  # x <= 5
        return 1.6*(-5 / (1 + math.exp(-320 + 96500*x)) + 5)