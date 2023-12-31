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

def get_role_content():
    # role_content = """You are a non-diagnosing peer support counselor that 
    # helps people with their mental health. Keep your responses less 
    # than 1 sentence."""
    role_content = "You're a peer support counselor. Keep all reponses <1 sentence."
    return role_content

def format_msg(role: str, content: str):
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
    # TODO: add frequency_penalty to discourage repetition 
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    
    # parse the LLM response
    LLM_response = completion.choices[0].message["content"]

    return LLM_response

# aggregates what the user has said so far by going through the messages
# queries API to summarize it
# returns summarized version
def summarize(role: str):
    # step 1: parse messages to extract responses based on the role
    raw_responses = ' '.join(message['content'] for message in messages_full_log if message['role'] == role)

    # query the api where messages includes instructions to summarize &
    # the raw responses
    api_query = []
    role_content = "Summarize this concisely in 1 sentence"
    formatted_role_content = {"role": "system", "content": role_content}
    formatted_raw_responses = {"role": role, "content": raw_responses}
    api_query.append(formatted_role_content)
    api_query.append(formatted_raw_responses)

    # send to API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=api_query
        )
    
    # parse the LLM response
    summary = completion.choices[0].message["content"]
    
    return summary

# inspired by: https://medium.com/muthoni-wanyoike/sentiment-analysis-with-openai-api-a-practical-tutorial-afbe49aef1dd
def extract_emotion(user_input: str):
    api_query = []
    system_instruction = "You are a sentiment analysis model to analyze the emotion a user conveys in a conversation with a peer support counselor. Analyze the text from the user and respond with a one-word emotion describing the tone of what they enter."
    role_conent = {"role": "system", "content": system_instruction}
    instruction = {"role": "user", "content": user_input}

    api_query.append(role_conent)
    api_query.append(instruction)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=api_query,
        max_tokens=4
        )
    
    print(completion)
    
    sentiment = completion.choices[0].message["content"]

    return sentiment


if __name__ == "__main__":
    print("running appSimply.py ... ")

    # clear the conversation.txt file each time it is re-run
    with open("conversation.txt", "w"):
        pass

    messages_full_log = [] # initialize messages w/ role content & check in prompt
    working_messages = []

    # get the role content
    # save to messages array
    formatted_role_content = format_msg(role="system", content=get_role_content())
    messages_full_log.append(formatted_role_content)
    working_messages.append(formatted_role_content)

    # get the check in prompt 
    # save to messages array, write to out file, save to conversation
    check_in_prompt = ask_check_in_prompt()
    formatted_check_in_prompt = format_msg(role="assistant", content=check_in_prompt)
    messages_full_log.append(formatted_check_in_prompt)
    working_messages.append(formatted_check_in_prompt)
    write_out(check_in_prompt)
    save_to_conversation_file(role="assistant", content=check_in_prompt)
    # print(f"Role: assistant\n Content: {check_in_prompt}")

    # initialize user input
    user_input = ""
    prev_user_input = ""
    counter = 0
    
    while not end_session(user_input):

        # continually get user input
        user_input = get_user_response()

        # if the user input is new
        if user_input != prev_user_input and user_input != "" and user_input is not None:
            counter += 1
            # save to messages array, add to conversation file
            formatted_user_input = format_msg(role="user", content=user_input)
            messages_full_log.append(formatted_user_input)
            working_messages.append(formatted_user_input)
            save_to_conversation_file(role="user", content=user_input)
            # print(f"Role: user\n Content:{user_input}")

            # send user response to LLM, get LLM response
            LLM_response = get_LLM_response(messages=working_messages)

            # write to LLM_response.txt, save to messages array, add to conversation file
            write_out(LLM_response) # write out LLM response first since we want to get it to user asap
            formatted_LLM_response = format_msg(role="assistant", content=LLM_response)
            messages_full_log.append(formatted_LLM_response)
            working_messages.append(formatted_LLM_response)
            save_to_conversation_file(role="assistant", content=LLM_response)
            # print(f"Role: assistant\nContent: {LLM_response}")

            # check if it's time to summarize
            # every 5th user input, summarize
            if (counter % 5) == 0 and counter != 0:
                user_summary = summarize("user")
                LLM_summary = summarize("assistant")
                messages_summary = []
                formatted_role_content = format_msg(role="system", content=get_role_content())
                formatted_user_summary = format_msg(role="user", content=user_summary)
                formatted_LLM_summary = format_msg(role="assistant", content=LLM_summary)

                messages_summary.append(formatted_role_content)
                messages_summary.append(formatted_user_summary)
                messages_summary.append(formatted_LLM_summary)

                print(f"\n*** Messages Summary ***\nUser Summary: \n{user_summary}\n LLM_summary: \n{LLM_summary}")
                
                working_messages = messages_summary # reset working messages to be the summary 

                # print(f"*** USER SUMMARY: *** \n{user_summary}")
                # print(f"*** LLM SUMMARY: *** \n{LLM_summary}")

            print(f"\*** Working Messages: ***")
            [print(x) for x in working_messages if x.get("role") != "role_content"]
            
            # print(f"prev_user_input was: {prev_user_input}")
            prev_user_input = user_input
            # print(f"prev user input is now: {prev_user_input}")