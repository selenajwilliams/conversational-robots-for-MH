# imports
import os
import openai
from flask import Flask, redirect, render_template, request, url_for
# speech recongition related imports, will move this to a seperate file soon
import pyaudio
import speech_recognition as sr
import wave
import random
import io
import os.path
import sys
sys.path.append("..")
sys.path.append("secrets")
from api_keys.OPENAI_API_KEY import API_KEY
app = Flask(__name__)
openai.api_key = API_KEY


# inspired by: https://medium.com/muthoni-wanyoike/sentiment-analysis-with-openai-api-a-practical-tutorial-afbe49aef1dd
def extract_emotion(user_input: str):
    api_query = []
    system_instruction = "You are a sentiment analysis model to analyze the emotion a user conveys in a conversation with a peer support counselor. Analyze the text from the user and respond with a one-word emotion describing the tone of what they enter."
    role_conent = {"role": "system", "content": system_instruction}
    instruction = {"role": "user", "content": f"{user_input}"}

    api_query.append(role_conent)
    api_query.append(instruction)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=api_query,
        max_tokens=2
        )
    
    print(completion)
    
    sentiment = completion.choices[0].message["content"]

    return sentiment

if __name__ == "__main__":
    user_input = "I'm anxious." # anxious
    user_input = "It’s been difficult confronting people at work about how they can grow and I’m afraid to start conflict or be disliked." # fear
    user_input = "I get really nervous before difficult conversations and I don’t know how to approach them." # anxiety
    user_input = "My dog died" # sad
    user_input = "I can't believe they treated me that way! How could they?" # anger
    user_input = "Okay, that makes sense. What kind of breathing techniques can I use to slow my heart rate and regulate my nervous system? I get really panicky and fluttery and feel like I’m losing control sometimes." # anxiety
    user_input = "sounds good. I am feeling better. thanks!" # grateful
    sentiment = extract_emotion(user_input)
    print(sentiment)