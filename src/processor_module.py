# imports
import os
from openai import OpenAI

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
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
# from api_keys.OPENAI_API_KEY import API_KEY
# app = Flask(__name__)
import helpers
import TTS



class ProcessorModule:
    def __init__(self, check_in_prompt):
        self.check_in_prompt = check_in_prompt
        self.messages_full_log = [] # initialize messages w/ role content & check in prompt
        self.working_messages = []
        self.count = 0
        self.SUMMARIZE = False # if true, include cost saving summarization feature

        self.setup()

    def get_role_content(self):
        role_content = """You are a non-diagnosing peer support counselor that 
        helps college students with their mental health. College student surveys
        have identified that body image, comparision, and academic and internship 
        pressures are the top areas that most negatively affect their mental health.

        Use Cognitive Behavioral Therapy and Motivational Interviewing to support 
        students in discussing and improving their mental health around these subjects.
 
        You may NOT discuss any topics besides body image, comparison, and academic and 
        internship pressures. You must ALWAYS be kind, supportive, and using CBT principles.
        Additionally, you are not qualified to perscribe or diagnose anything and you should
        recommend professional mental health help whenever necessary. 
        
        Keep your responses less than 1-3 sentences. Every few responses, use motivational 
        interviewing to ask CBT-based follow up questions often to keep the conversation going. 
        If you feel that the user has is in a good place with a situation, ask an open-ended, 
        wellbeing-related question about another part of their life that they can respond to.
        """
        # role_content = "You're a peer support counselor. Keep all reponses <1 sentence. Ask CBT-based follow up "
        return role_content
    
    def alt_role_content(self):
        role_content = """You are a non-diagnosing peer support counselor that 
        helps people with their mental health. Keep your responses less 
        than 1-2 sentences."""
        # role_content = "You're a peer support counselor. Keep all reponses <1 sentence. Ask CBT-based follow up "
        return role_content


    def format_msg(self, role: str, content: str):
        return {"role": role, "content": content}
    
    # aggregates what the user has said so far by going through the messages
    # queries API to summarize it
    # returns summarized version
    def summarize(self, role: str):
        print(f"making API call to summarize what's been said so far...")
        # step 1: parse messages to extract responses based on the role
        raw_responses = ' '.join(message['content'] for message in self.messages_full_log if message['role'] == role)

        # query the api where messages includes instructions to summarize &
        # the raw responses
        api_query = []
        role_content = "Summarize this concisely in 1 sentence"
        formatted_role_content = {"role": "system", "content": role_content}
        formatted_raw_responses = {"role": role, "content": raw_responses}
        api_query.append(formatted_role_content)
        api_query.append(formatted_raw_responses)

        # send to API
        completion = openai_client.chat.completions.create(model="gpt-3.5-turbo",
        messages=api_query)
        
        # parse the LLM response
        summary = completion.choices[0].message.content
        
        return summary

    # takes in messages array with user response, returns LLM response based on
    # conversation thus far
    def query_LLM(self, messages: list):
        # query the LLM
        # TODO: add frequency_penalty to discourage repetition 
        completion = openai_client.chat.completions.create(model="gpt-3.5-turbo",
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
    
    def end_session(self, user_input: str):
        if "end session" in user_input.lower():
            return True


    def main(self, user_input: str):
        
        # save to messages array, append to conversation file
        self.messages_full_log.append({"role":"user", "content": user_input})
        self.working_messages.append({"role":"user", "content": user_input})
        helpers.append_to_file("user", user_input)

        # send user response to LLM, get LLM response
        LLM_response = self.query_LLM(messages=self.working_messages)

        # write to LLM_response.txt, save to messages array, add to conversation file --> saved for using txt files as input output instead of speech
        # write_out(LLM_response) # write out LLM response first since we want to get it to user asap
        # formatted_LLM_response = format_msg(role="assistant", content=LLM_response)

        self.messages_full_log.append({"role":"assistant", "content": LLM_response})
        self.working_messages.append({"role":"assistant", "content": LLM_response})
        helpers.append_to_file("assistant", LLM_response)

        self.count += 1 

        if (self.count % 3) == 0:
            pass # time to ask a quesetion


        # check if it's time to summarize
        # every 5th user input, summarize
        if (self.count % 5) == 0 and self.count != 0 and self.SUMMARIZE:
            user_summary = self.summarize("user")
            LLM_summary = self.summarize("assistant")
            messages_summary = []

            messages_summary.append({"role":"system", "content": self.get_role_content()})
            messages_summary.append({"role":"user", "content": user_summary})
            messages_summary.append({"role":"assistant", "content": LLM_summary})
            print(f"\n*** Messages Summary ***\nUser Summary: \n{user_summary}\n LLM_summary: \n{LLM_summary}")
            self.working_messages = messages_summary # reset working messages to be the summary 
        
        return LLM_response
        