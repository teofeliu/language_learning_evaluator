# Language Learning Evaluator

## Overview

The Language Learning Evaluator is a FastAPI-based application that assesses language proficiency from audio inputs. It provides a comprehensive evaluation of accent, vocabulary, grammar, conjugation, cultural knowledge, and expression.

## Key Technologies

- **FastAPI**: High-performance web framework for building APIs with Python 3.6+
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **OpenAI GPT-4o (text-to-text)**: Large Language Model for detailed language assessment
- **Hugging Face `dima806/speech-accent-classification` (audio-to-vec2)**: Used for accent evaluation with a pre-trained model
- **PyDub**: Audio file processing and conversion
- **SpeechRecognition**: Audio transcription using Google Cloud Speech-to-Text

## Unique Features

- **Asynchronous Dual Model Evaluation**: The app makes two separate, asynchronous calls:
  1. To OpenAI's GPT-4 for detailed language assessment
  2. To a Hugging Face model for accent evaluation
- **Custom Accent Score Normalization**: Implements a logistic scaling transformation for accent scores

  [Insert image of the normalization function here]

  Equation: 
<summary>Equation:</summary>

<p align="center" style="color: inherit;">
  <img src="https://latex.codecogs.com/svg.latex?\color{white}f(x)=\begin{cases}-\left(\frac{2}{1+e^{-2955+2992.5x}}\right)+10,&\text{if}x>0.5\\1.6\left(-\frac{5}{1+e^{-320+96500x}}+5\right),&\text{if}x\leq0.5\end{cases}">
</p>

## API Endpoints

- `POST /evaluations/`: Submit an audio file for evaluation
- `GET /evaluations/{evaluation_id}`: Retrieve a specific evaluation result

## Example Output

```json
{
  "accent_score": 6.654727319754656,
  "vocabulary": {
    "score": 6,
    "evaluation": "The vocabulary is simple and appropriate but lacks richness,"
  },
  "grammar": {
    "score": 4,
    "evaluation": "Several grammatical errors and limited complexity in sentence structure,"
  },
  "conjugation": {
    "score": 5,
    "evaluation": "Verb forms are mostly accurate but limited in variety,"
  },
  "culture": {
    "score": 6,
    "evaluation": "The reference to Elvis Presley highlights a significant cultural moment but lacks depth,"
  },
  "expression": {
    "score": 5,
    "evaluation": "The expression is somewhat clear but feels disjointed, and stylistically could be improved,"
  },
  "transcription": "if I had to pick 1 moment to go back to teleport myself it would be 1 of Elvis Presley's first performances seeing a historical movement start and take place right in front of my eyes while surrounded by a crowd that is sweaty and energetic and being a mermaid and a new wave of music that is pure would be a moment like no other ",
  "audio_file_path": "uploads/525 Stockton St, Apt 306 5.mp3"
}
```
