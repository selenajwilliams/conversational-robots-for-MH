""" FULL MEMORY VERSION
    This version of the system works by saving the full conversation and 
    sending that to the API every time.
"""

# imports
import os
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

def init_role_content():
    # role_content = """You are a non-diagnosing peer support counselor that 
    # helps people with their mental health. Keep your responses less 
    # than 1 sentence."""
    role_content = "You're a peer support counselor."
    return role_content

def formatt_msg(role: str, content: str):
    return {"role": role, "content": content}

def ask_check_in_prompt():
    check_in_prompts = ["How are you?", "Have you been stressed lately?"]
    check_in_prompt = random.choice(check_in_prompts)
    return check_in_prompt

def end_session(user_input: str):
    if "end session" in user_input.lower():
        return True
    else: 
        return False

# we only write out the response when we receive the LLM's response, so we
# always save it to the same file called LLM_response.txt
def write_out(LLM_response: str):
    with open('LLM_response.txt', 'w') as file:
        file.write(LLM_response)

def save_to_conversation_file(role: str, content: str):
    with open("conversation.txt", "a") as file:
        formatted_data = f"{role.upper()}: \n{content}\n\n"
        file.write(formatted_data)

# reads user input file to get user input
def get_user_response():
    with open('user_input.txt', 'r') as file:
        user_input = file.read()
    
    return user_input

# takes in messages array with user response, returns LLM response based on
# conversation thus far
def get_LLM_response(messages: list):
    # query the LLM
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    
    # parse the LLM response
    LLM_response = completion.choices[0].message["content"]

    return LLM_response


if __name__ == "__main__":
    print("running appSimply.py ... ")

    # clear the conversation.txt file each time it is re-run
    with open("conversation.txt", "w"):
        pass

    messages = [] # initialize messages w/ role content & check in prompt

    # get the role content
    # save to messages array
    formatted_role_content = formatt_msg(role="system", content=init_role_content())
    messages.append(formatted_role_content)

    # get the check in prompt 
    # save to messages array, write to out file, save to conversation
    check_in_prompt = ask_check_in_prompt()
    formatted_check_in_prompt = formatt_msg(role="assistant", content=check_in_prompt)
    messages.append(formatted_check_in_prompt)
    write_out(check_in_prompt)
    save_to_conversation_file(role="assistant", content=check_in_prompt)
    print(f"Role: assistant\n Content: {check_in_prompt}")

    # initialize user input
    user_input = ""
    prev_user_input = ""
    counter = 0
     
    while not end_session(user_input):

        # continually get user input
        user_input = get_user_response()

        # if the user input is new
        if user_input != prev_user_input and user_input != "":
            counter += 1
            # save to messages array, add to conversation file
            formatted_user_input = formatt_msg(role="user", content=user_input)
            messages.append(formatted_user_input)
            save_to_conversation_file(role="user", content=user_input)
            print(f"Role: user\n Content:{user_input}")

            # send user response to LLM, get LLM response
            LLM_response = get_LLM_response(messages=messages)

            # write to LLM_response.txt, save to messages array, add to conversation file
            write_out(LLM_response)
            formatted_LLM_response = formatt_msg(role="assistant", content=LLM_response)
            messages.append(formatted_LLM_response)
            save_to_conversation_file(role="assistant", content=LLM_response)
            print(f"Role: assistant\n Content: {LLM_response}")

            print(f"prev_user_input was: {prev_user_input}")
            prev_user_input = user_input
            print(f"prev user input is now: {prev_user_input}")