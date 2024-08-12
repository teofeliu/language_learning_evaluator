# app/services/audio_processing.py

import aiofiles
import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from fastapi import UploadFile
from pathlib import Path
from tempfile import NamedTemporaryFile
from app.exceptions import InvalidFileTypeException, InvalidFileFormatException
from pydub.exceptions import CouldntDecodeError

async def convert_audio(audio_file: Path, file_type="wav"):
    if not audio_file.exists():
        raise FileNotFoundError(f"The file {audio_file} does not exist.")

    # Check if the file is an audio file
    try:
        audio = AudioSegment.from_file(str(audio_file))
    except Exception as e:
        raise InvalidFileTypeException("The uploaded file is not a valid audio file.") from e

    # Get the current file extension
    current_type = audio_file.suffix[1:].lower()

    # If the current type matches the desired type, just return the path
    if current_type == file_type.lower():
        return audio_file

    # Otherwise, convert the file
    try:
        new_path = audio_file.with_suffix(f".{file_type}")
        audio.export(str(new_path), format=file_type)
        return new_path
    except Exception as e:
        raise InvalidFileFormatException(f"Error processing audio file: {str(e)}") from e


async def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google_cloud(audio)
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"