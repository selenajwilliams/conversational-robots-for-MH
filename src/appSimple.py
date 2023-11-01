import os
import openai_handler
import openai
from flask import Flask, redirect, render_template, request, url_for
import os.path
import sys
sys.path.append("..")
sys.path.append("secrets")
from api_keys.OPENAI_API_KEY import API_KEY

app = Flask(__name__)
openai.api_key = API_KEY


### for context, this query is 163 tokens toal -- 117 fr the prompt + 46 for completion


def init_LLM():
    role_content = """
                    You are a peer support counselor that helps 
                    people with their mental health and wellbeing.
                    As a peer support counselor you cannot perscribe or
                    diagnose anything. Keep your responses brief.
                    You are emotionally intelligent, non-judgemental, 
                    empathetic, and supportive.
                    """
    user_response_1 = """
                    I am okay. I've been struggling with stress and anxiety
                    with school and some friend-group conflicts I'm afraid 
                    to speak up about. 
                    """

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": role_content},
        {"role": "assistant", "content": "How have you been?"},
        {"role": "user", "content": user_response_1}
    ]
    )



# print(f"totla response is {completion}")
# print(f"message is {completion.choices[0]['content'].message}")

