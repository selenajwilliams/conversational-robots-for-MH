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

# initializes LLM & initializes messages list which is a key piece of state / variable throughout the system
def init_system():
    messages = [] 

    role_content = """You are a non-diagnosing peer support counselor that 
        helps people with their mental health. Keep your responses less 
        than 1 sentence."""
    msg_record = {"role": "system", "content": role_content}
    messages.append(msg_record)

    return messages

def ask_check_in_prompt(messages: list):
    check_in_prompts = ["How are you?", "Have you been stressed lately?"]
    check_in_prompt = random.choice(check_in_prompts)
    
    # update the messages array
    msg_record = {"role": "assistant", "content": check_in_prompt}

    print(f"check in prompt: {check_in_prompt}")

    record("LLM", check_in_prompt)
    messages.append(msg_record)

    # write the check in prompt to a txt file for Kuri
    # Kuri will be listening for new files via a ROS subscriber node
    with open('check_in_prompt.txt', 'w') as file:
        file.write(check_in_prompt)

    return messages


def end_session(user_input: str):
    if "end session" in user_input.lower():
        return True
    else: 
        return False


def respond_to_user(messages: list): 
    print('responding to user...')
    # takes the list of messages, sends to LLM to get response
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    # parse the response
    LLM_response = completion.choices[0].message["content"]
    print(f"LLM response: {LLM_response}")

    LLM_record = {"role":"assistant", "content": LLM_response}

    record("LLM", LLM_response)
    messages.append(LLM_record)

    num_tokens = completion.usage["total_tokens"]


def get_user_input():
    with open('user_input.txt', 'r') as file:
        user_input = file.read()
    
    return user_input

def record(role: str, data: str):
    with open("conversation.txt","a") as file:
        formatted_data = f"{role.upper()}: \n {data}\n\n"
        file.write(formatted_data)



if __name__ == "__main__":
    print("running appSimply.py ... ")

    messages = init_system()

    # in check_in_prompt we want to save it as a txt file and send to Kuri to ask via ROS node
    ask_check_in_prompt(messages) # pass in messages so that messages can be appended

    print(f"messages is: {messages}")

    print("having conversation ...")

    user_input = ""
    prev_user_input = ""

    counter = 0

    while not end_session(user_input):

        user_input = get_user_input() # continually read from file

    # if user input is new & non-empty, process it
        if user_input != prev_user_input and user_input != "":
            counter += 1 
            print(f"user input: {user_input}")

            record("USER", user_input)
            formatted_input = {"role": "user", "content": user_input}
            messages.append(formatted_input)

            respond_to_user(messages)

            prev_user_input = user_input

    print(f"final messages is \n\n\n{messages}")
    print("WHILE LOOP HAS ENDED!!!!!!")
    