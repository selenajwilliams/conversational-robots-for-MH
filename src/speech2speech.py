import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
import os



openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]


transcriber = None
full_transcript = [
    {
        "role": "system",
        "content": "You're a highly skilled AI assistant. Answer in <1 sentence",
    },
]


def start_transcription():
    transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=96000,
        end_utterance_silence_threshold=1000,
    )

    # Start the connection
    transcriber.connect()

    # Open  the microphone stream
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=96000)

    # Stream audio from the microphone
    transcriber.stream(microphone_stream)


def stop_transcription(transcriber):
    if transcriber:
        transcriber.close()
        transcriber = None


def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        get_gpt_response(transcript.text)
    else:
        print(transcript.text, end="\r")


def on_error(error: aai.RealtimeError):
    print("An error occured:", error)


def get_gpt_response(user_speech):
    stop_transcription(transcriber)

    full_transcript.append({"role": "user", "content": user_speech})
    print(f"\nUser: {user_speech}", end="\r\n")

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=full_transcript
    )

    ai_response = completion.choices[0].message.content

    generate_audio(ai_response)

    start_transcription()
    print(f"\nReal-time transcription: ", end="\r\n")


def generate_audio(text):
    full_transcript.append({"role": "assistant", "content": text})
    print(f"\nAI Assistant: {text}")

    audio_stream = generate(
        api_key=elevenlabs_api_key, text=text, voice="Rachel", stream=True
    )

    stream(audio_stream)


initial_ai_message = "How have you been feeling lately?"
generate_audio(initial_ai_message)
start_transcription()