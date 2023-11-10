import os
# import openai_handler
import openai
from flask import Flask, redirect, render_template, request, url_for

# speech recongition related imports, will move this to a seperate file soon
import pyaudio
import speech_recognition as sr
import wave

import os.path
import sys
sys.path.append("..")
sys.path.append("secrets")
from api_keys.OPENAI_API_KEY import API_KEY

app = Flask(__name__)
openai.api_key = API_KEY


### for context, this query is 163 tokens toal -- 117 fr the prompt + 46 for completion

""" Saves the conversation to a file
"""
def record(role: str, data: str):
    with open("conversation.txt","a") as file:
        formatted_data = f"{role.upper()}: \n {data}\n\n"
        file.write(formatted_data)
    
""" initializes the LLM by letting it know that it is role playing a peer 
support counselor

returns: void. we discard the first response because this functio is just
         to prime the LLM for user responses.
"""
def init_LLM():
    role_content = """
                    You are a peer support counselor that helps 
                    people with their mental health and wellbeing.
                    As a peer support counselor you cannot perscribe or
                    diagnose anything. Keep your responses brief.
                    You are emotionally intelligent, non-judgemental, 
                    empathetic, and supportive.
                    """

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": role_content},
        {"role": "assistant", "content": "How have you been?"},
        ]
    )

    LLM_response = completion.choices[0].message["content"]
    num_tokens = count_tokens(completion)
    print(f"tokens used: \n{num_tokens}")
    print(f"init LLM response which we discard: {LLM_response}")
    record("LLM", LLM_response)
    return LLM_response

    # note: message can be accessed at: 
    # print(f"totla response is {completion}")
    # print(f"message is {completion.choices[0]['content'].message}")

""" sends user response to LLM and returns support response from the LLM
    returns: support response from LLM

"""
def respond_to_user(user_response: str):
    LLM_role_summary = "non-diagnosing, non-perscriptive, emotionally supportive peer support counselor, responses 1 paragraph or less"
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": LLM_role_summary},
        # seeing how well this performs w/out this to minimize tokens
        # {"role": "assistant", "content": "How have you been?"}, 
        {"role": "user", "content": user_response}
        ]
    )

    LLM_response = parse_response(completion)
    num_tokens = count_tokens(completion)
    print(f"LLM reponse: \n{LLM_response}")
    print(f"tokens used {num_tokens}")

    record("LLM", LLM_response)
    return LLM_response

def parse_response(completion):
    return completion.choices[0].message["content"]

def count_tokens(completion):
    tokens_used = completion.usage["total_tokens"]
    return tokens_used

def end_session(user_input):
    if "end session" in user_input.lower():
        return True
    else:
        return False
    

def get_user_response():
    print("Getting user response...")
    prev_user_input = "" # define prev_user_input to an empty string

    # in a loop, continually read in the file called user_input.txt
    # if what is in the file differs from what was in there previously,
    # that means the user has said something new (the user has responded)
    # and that response should be sent to the LLM as part of the conversation
    while True:
        with open('user_input.txt', 'r') as file:
            user_input = file.read()

        # if user input is new, send it to LLM & save it to file
        if user_input != prev_user_input and user_input != "":
            print(f"user input: {user_input} \n previous user input: {prev_user_input}")
            record("USER", user_input)
            respond_to_user(user_input) 
            prev_user_input = user_input

# this part below has to do with real time speech recognition & speech to text using the whisper API, 
# which will enable the get_user_response function above
def get_user_response_speech_version():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Listening for speech...")

    with microphone as source:
        try:
            print("Start speaking!")
            recognizer.adjust_for_ambient_noise(source) # optional
            # save the audio data
            # params: 
                # timeout: if no speech is detected within 10 seconds, sr will throw an error or not record
                # phrase_time_limit: audio stops listening after speech is not detected for 3 seconds 
                #                    (end of speech detection) ^
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)  # Listen for up to 3 seconds of speech
            
            # save audio to file 
            with open("user_speech.wav", "wb") as audio_file:
                audio_file.write(audio.get_wav_data())
            
            # TODO: error is happening on line 117
            # send audio file to whisper api to be transcribed
            transcript = openai.Audio.transcribe("whisper-1", audio_file.read())
            print(f"\n***SPEECH TRANSCRIPTION***\n{transcript}")
            return transcript
        
        except Exception as e:
            # if any exception occurs, print it to see what it is
            print(f"error encountered: {e}")


if __name__ == "__main__":
    print("running appSimply.py ... ")

    # clear what is currently in the conversation file
    with open("conversation.txt", "w"):
        pass

    init_LLM() # commented out to save tokens for testing purposes, testing sr currently

    # user_response_1 = "I am worried about my dad's health and the stress that is putting on my family and it's hard not being there with them."
    user_response = get_user_response()
    print(f"User response: \n{user_response}")

    # respond_to_user(user_response) # this is where we send the wav file to the LLM
    # respond_to_user(user_response_1)

    # if not end_session:
    #     user_response = get_user_response()
    #     respond_to_user(user_response) 














# def tokens_counter(num_tokens): # this is wrong, restart another time
#     prev_tokens += num_tokens
#     print(f'tokens used is now {num_tokens}')
#     return prev_tokens

