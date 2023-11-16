import os
# import openai_handler
import openai
from flask import Flask, redirect, render_template, request, url_for

# speech recongition related imports, will move this to a seperate file soon
import pyaudio
import speech_recognition as sr
import wave
import random

import os.path
import sys
sys.path.append("..")
sys.path.append("secrets")
from api_keys.OPENAI_API_KEY import API_KEY

app = Flask(__name__)
openai.api_key = API_KEY

global_messages = []

    
""" initializes the LLM by letting it know that it is role playing a peer 
support counselor

returns: void. we discard the first response because this functio is just
         to prime the LLM for user responses.
"""
def init_messages():
    role_content = """
                    You are a peer support counselor helping 
                    people with their mental health and wellbeing.
                    You cannot perscribe or diagnose anything. 
                    Keep your responses brief (<3 sentences).
                    You are emotionally intelligent, non-judgemental, 
                    empathetic, and supportive.
                    """
    message = {"role": "system", "content": role_content}

    global_messages.append(message)
    print(global_messages)


def get_user_response():
    print("Getting user response...")
    prev_user_input = "" # define prev_user_input to an empty string

    # in a loop, continually read in the file called user_input.txt
    # if what is in the file differs from what was in there previously,
    # that means the user has said something new (the user has responded)
    # and that response should be sent to the LLM as part of the conversation
    with open('user_input.txt', 'r') as file:
        user_input = file.read()
    
    return user_input, "user"

# format
def add_msg(role: str, message: str):
    return {"role": role, "content": message}


if __name__ == "__main__":
    print("running appSimply.py ... ")

    # clear what is currently in the conversation file
    with open("conversation.txt", "w"):
        pass

    user_input = get_user_response()


    prev_user_input = ""
    # while the session is still in progress
    while True: 
        # if user input is new, send it to LLM & save it to file
        if user_input != prev_user_input and user_input != "":
            print(f"user input: {user_input} \n previous user input: {prev_user_input}")
            # messages, user_response = record(messages=curr_messages, role="USER", data=user_input)
            respond_to_user(messages) 
            prev_user_input = user_input

    print(f"User response: \n{user_response}")
    # respond_to_user(user_response) # this is where we send the wav file to the LLM # not sure if I still need this?
    # respond_to_user(user_response_1)