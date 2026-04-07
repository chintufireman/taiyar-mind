import uuid
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Any

from dotenv import load_dotenv
from fastapi import UploadFile
from openai import OpenAI
import os

async def load_voice_model(audio_file: UploadFile) -> Any:
    load_dotenv()
    api_key_voice = os.getenv("OPEN_AI_VOICE_API_KEY")
    openai_client = OpenAI(api_key=api_key_voice)

    content = await audio_file.read()
    # read = BytesIO(read)
    # print(read)
    transcript = openai_client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=(audio_file.filename, content),
    )

    return transcript