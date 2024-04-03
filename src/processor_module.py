# imports
import os
from openai import OpenAI

client = OpenAI(api_key=API_KEY)
# from flask import Flask, redirect, render_template, request, url_for
# speech recongition related imports, will move this to a seperate file soon
import pyaudio
# import speech_recognition as sr
import wave
import random
import os.path
import sys
sys.path.append("..")
sys.path.append("secrets")
from api_keys.OPENAI_API_KEY import API_KEY
# app = Flask(__name__)
import helpers



class ProcessorModule:
    def __init__(self, check_in_prompt):
        self.check_in_prompt = check_in_prompt
        self.messages_full_log = [] # initialize messages w/ role content & check in prompt
        self.working_messages = []
        self.count = 0

        self.setup()

    def get_role_content(self):
        # role_content = """You are a non-diagnosing peer support counselor that 
        # helps people with their mental health. Keep your responses less 
        # than 1 sentence."""
        role_content = "You're a peer support counselor. Keep all reponses <1 sentence."
        return role_content

    def format_msg(self, role: str, content: str):
        return {"role": role, "content": content}
    
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
        completion = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=api_query)
        
        # parse the LLM response
        summary = completion.choices[0].message.content
        
        return summary

    # takes in messages array with user response, returns LLM response based on
    # conversation thus far
    def query_LLM(self, messages: list):
        # query the LLM
        # TODO: add frequency_penalty to discourage repetition 
        completion = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages)
        
        # parse the LLM response
        LLM_response = completion.choices[0].message.content

        return LLM_response
    

    def setup(self):
        """ Sets up info related to api queries & processing user input. Namely, this function saves
            the role_content and check in prompt to the message logs, which are the data structures 
            used to query the LLM. 
            It also saves the check in prompt to a file that will log the conversation

            Returns:
                Nothing
        """

        # save role content & check in prompt to data structures
        self.messages_full_log.append({"role":"system", "content": self.get_role_content()})
        self.working_messages.append({"role":"system", "content": self.get_role_content()})

        self.messages_full_log.append({"role":"assistant", "content": self.check_in_prompt})
        self.working_messages.append({"role":"assistant", "content": self.check_in_prompt})

        # append check in prompt to conversation log
        helpers.append_to_file("assistant", self.check_in_prompt)


    def main(self, user_input: str):
        
        # save to messages array, append to conversation file
        self.messages_full_log.append({"role":"user", "content": user_input})
        self.working_messages.append({"role":"user", "content": user_input})
        helpers.append_to_file("user", user_input)

        # send user response to LLM, get LLM response
        LLM_response = self.query_LLM(messages=self.working_messages)

        # write to LLM_response.txt, save to messages array, add to conversation file
        # write_out(LLM_response) # write out LLM response first since we want to get it to user asap
        # formatted_LLM_response = format_msg(role="assistant", content=LLM_response)

        self.messages_full_log.append({"role":"assistant", "content": LLM_response})
        self.working_messages.append({"role":"assistant", "content": LLM_response})
        helpers.append_to_file("assistant", LLM_response)

        self.count += 1


        # check if it's time to summarize
        # every 5th user input, summarize
        if (self.count % 5) == 0 and self.count != 0:
            user_summary = self.summarize("user")
            LLM_summary = self.summarize("assistant")
            messages_summary = []
            # formatted_role_content = format_msg(role="system", content=get_role_content())
            # formatted_user_summary = format_msg(role="user", content=user_summary)
            # formatted_LLM_summary = format_msg(role="assistant", content=LLM_summary)

            messages_summary.append({"role":"system", "content": self.get_role_content()})
            messages_summary.append({"role":"user", "content": user_summary})
            messages_summary.append({"role":"assistant", "content": LLM_summary})

            # messages_summary.append(formatted_role_content)
            # messages_summary.append(formatted_user_summary)
            # messages_summary.append(formatted_LLM_summary)

            print(f"\n*** Messages Summary ***\nUser Summary: \n{user_summary}\n LLM_summary: \n{LLM_summary}")
            
            working_messages = messages_summary # reset working messages to be the summary 

            # print(f"*** USER SUMMARY: *** \n{user_summary}")
            # print(f"*** LLM SUMMARY: *** \n{LLM_summary}")

        # print(f"\*** Working Messages: ***")
        # [print(x) for x in working_messages if x.get("role") != "role_content"]
        
        return LLM_response
        