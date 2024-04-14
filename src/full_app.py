import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
import os
import helpers
from processor_module import ProcessorModule
import TTS
import sys


openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]


transcriber = None

def start_transcription(pm: ProcessorModule):
    transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=96000,
        # end_utterance_silence_threshold=1000, # 1000 seems a little fast, let's try 1500
        end_utterance_silence_threshold=2000,

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
        stop_transcription(transcriber)

        # filters out any of the LLM response that was accidentally recorded from TTS module hearing it play on the speakers
        # index = transcript.text.find(saved_LLM_response)  
        # if index != -1:
        #     transcript.text = transcript.text[index + len(saved_LLM_response) +1:]
        #     print(f"after filtering, transcript.text is: {transcript.text}")
        
        LLM_response = pm.main(transcript.text)
        # transcript.text = ""
        TTS.generate_audio(LLM_response)
        start_transcription(pm)

        # saved_LLM_response = ' '.join(LLM_response.lower().split()[3:])


        # if ("end session" in transcript.text.lower()):
        #     stop_transcription(transcriber)
        #     print(f"ending session...")
        #     sys.exit()

        # processor_module.process_input(transcript.text)
        # get_gpt_response(transcript.text)
    else:
        print(transcript.text, end="\r")


def on_error(error: aai.RealtimeError):
    print("An error occured:", error)


""" main script  """

intro = "Hi, I'm Rachel, a peer support counselor here to listen and support your mental health. " 
check_in_prompt = helpers.get_checkin_prompt()
TTS.generate_audio(intro + check_in_prompt)

pm = ProcessorModule(check_in_prompt)

# generate_audio(check_in_prompt)
start_transcription(pm)