import asyncio
from .. import audio_processing, accent_evaluation
from . import llm_evaluation
from pathlib import Path

#async def evaluate_speech(audio_file):
    # Save audio as MP3 for accent evaluation
    #mp3_path = await audio_processing.save_audio(audio_file, "mp3")

    # Save audio as WAV for speech-to-text
    #wav_path = await audio_processing.save_audio(audio_file, "wav")
    
    # Run evaluations concurrently
    #text_task = asyncio.create_task(audio_processing.audio_to_text(wav_path))
    # accent_task = asyncio.create_task(accent_evaluation.evaluate_accent(mp3_path))

    # Wait for tasks to complete
    #text = await text_task
    #accent_score = await accent_task

    # Evaluate the transcribed text
    #llm_result = await llm_evaluation.evaluate_with_llm(text)
    #return "success"
    #return {
     #   "accent_score": accent_score,
      #  "vocabulary": {"score": llm_result['vocab_score'], "evaluation": llm_result['vocab_eval']},
       # "grammar": {"score": llm_result['grammar_score'], "evaluation": llm_result['grammar_eval']},
    #    "conjugation": {"score": llm_result['conjugation_score'], "evaluation": llm_result['conjugation_eval']},
     #   "culture": {"score": llm_result['cultural_score'], "evaluation": llm_result['cultural_eval']},
      #  "expression": {"score": llm_result['expression_score'], "evaluation": llm_result['expression_eval']},
       # "transcription": text
    #}

async def evaluate_speech(audio_file):
    # Create uploads folder if it doesn't exist
    uploads_folder = Path("uploads")
    uploads_folder.mkdir(exist_ok=True)

    # Save the uploaded file
    file_path = uploads_folder / audio_file.filename
    with open(file_path, "wb") as f:
        f.write(await audio_file.read())

    # Convert to mp3 and wav
    mp3_path = await audio_processing.convert_audio(file_path, "mp3")
    wav_path = await audio_processing.convert_audio(file_path, "wav")

    # Run evaluations concurrently
    text_task = asyncio.create_task(audio_processing.audio_to_text(str(wav_path)))
    accent_task = asyncio.create_task(accent_evaluation.evaluate_accent(str(mp3_path)))

    # Wait for tasks to complete
    text = await text_task
    accent_score = await accent_task

    # Evaluate the transcribed text
    llm_result = await llm_evaluation.evaluate_with_llm(text)
    
    return {
        "accent_score": accent_score,
        "vocabulary": {"score": llm_result['vocab_score'], "evaluation": llm_result['vocab_eval']},
        "grammar": {"score": llm_result['grammar_score'], "evaluation": llm_result['grammar_eval']},
        "conjugation": {"score": llm_result['conjugation_score'], "evaluation": llm_result['conjugation_eval']},
        "culture": {"score": llm_result['cultural_score'], "evaluation": llm_result['cultural_eval']},
        "expression": {"score": llm_result['expression_score'], "evaluation": llm_result['expression_eval']},
        "transcription": text,
        "audio_file_path": str(mp3_path)
    }