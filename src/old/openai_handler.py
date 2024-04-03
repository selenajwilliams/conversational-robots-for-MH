import os
import openai_handler
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from flask import Flask, redirect, render_template, request, url_for
# import user_response 

app = Flask(__name__)

# openai.api_key = os.environ["OPENAI_API_KEY"]

print("openai_handler.py running...")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = client.completions.create(model="text-davinci-003",
        prompt=generate_prompt(animal),
        temperature=0.6)
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

def sendResponse():
    pass

def init_conversation():
    return """ 
    Let's roleplay:
    You are a peer-support counselor. You cannot under any circumstances 
    diagnose a disease or illness. You cannot under any circumstance 
    perscribe medication. Instead, as a peer-support counselor, you will
    have a convesration about something that someone is experiencing and
    provide evidence-based, research-backed activities that can help them.
    """





# curl https://api.openai.com/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer os.environ["OPENAI_API_KEY"] \
#   -d '{
#      "model": "gpt-3.5-turbo",
#      "messages": [{"role": "user", "content": "Say this is a test!"}],
#      "temperature": 0.7
#    }'
