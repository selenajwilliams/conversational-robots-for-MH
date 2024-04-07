# import assemblyai as aai
from elevenlabs import generate, stream
# from openai import OpenAI
import os
import time


# aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]


def generate_audio(text):
    # full_transcript.append({"role": "assistant", "content": text})
    print(f"\nAI Assistant: {text}")

    audio_stream = generate(
        api_key=elevenlabs_api_key, text=text, voice="Rachel", stream=True
    )

    stream(audio_stream)

