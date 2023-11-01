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

    LLM_response = completion.choices[0]['content'].message
    return LLM_response

    # note: message can be accessed at: 
    # print(f"totla response is {completion}")
    # print(f"message is {completion.choices[0]['content'].message}")

""" sends user response to LLM and returns support response from the LLM
    returns: support response from LLM

"""
def respond_to_user(user_response: str):
    LLM_role_summary = "non-diagnosing, non-perscriptive, emotionally supportive peer support counselor"
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

    pass

def parse_response(completion):
    return completion.choices[0]['content'].message

def count_tokens(completion):
    tokens_used = completion.usage["total_tokens"]
    return tokens_used






# def tokens_counter(num_tokens): # this is wrong, restart another time
#     prev_tokens += num_tokens
#     print(f'tokens used is now {num_tokens}')
#     return prev_tokens

