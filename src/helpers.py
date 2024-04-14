from typing import List
import random
from openai import OpenAI

client = OpenAI()

""" Contains a variety of helper functions"""

def get_checkin_prompt() -> str:
    """Return a randomly selected check in prompt from the list of check in 
       prmopts

    Returns:
        str: the initial system prmopt to the user
    """

    def load_prompts() -> List[str]:
        """Reads in a .txt file of prompts, saves each prompt to a list of strings

        Returns:
           List[str]: the list of possible check-in prompts
        """
        prompt_list = []
        with open('prompts/prompts.txt', 'r') as file:
            for prompt in file:
                prompt_list.append(prompt.strip('\n'))
        return prompt_list

    prompt_list = load_prompts()

    prompt = random.choice(prompt_list)
    return prompt
    

# inspired by: https://medium.com/muthoni-wanyoike/sentiment-analysis-with-openai-api-a-practical-tutorial-afbe49aef1dd
def extract_emotion(user_input: str):
    """Makes a seperate API call to openai to determine the user emotion based 
       on the content of what the user is saying. 

        Returns: 
            str: the user's emotion
    """
    api_query = []
    system_instruction = "You are a sentiment analysis model to analyze the emotion a user conveys in a conversation with a peer support counselor. Analyze the text from the user and respond with a one-word emotion describing the tone of what they enter."
    role_conent = {"role": "system", "content": system_instruction}
    instruction = {"role": "user", "content": user_input}

    api_query.append(role_conent)
    api_query.append(instruction)

    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=api_query,
    max_tokens=4)
    
    print(completion)
    
    sentiment = completion.choices[0].message.content

    return sentiment


def append_to_file(role: str, content: str):
    """ Appends text to a file
        Used to save conversational responses from the user or LLM to the file

        Args:
            out_file (str): the file to update
            role (str): the role, user or LLM
            content (str): the content to save to the file 
    """
    # if out_file is None:
    out_file = "conversation_logs/body_image_test.txt"
    with open(out_file, "a") as file:
        formatted_data = f"{role.upper()}: \n{content}\n\n"
        file.write(formatted_data)


""" BELOW THIS LINE ARE HELPER FUNCTIONS FOR OLDER PROJECT IMPLEMENTATIONS
    CONTAINING THINGS LIKE READING IN USER INPUT FROM A FILE
"""


def read_in(file_name: str):
    """ Reads in and returns text from a file

        Formally used for reading in user input from a file; obsolete now that 
        we are using STT
    """
    with open(file_name, 'r') as file:
        text = file.read()
    
    return text


def write_out(text: str):
    """ Writes the text passed in to a file.

        Formally used for writing the LLM output to a file; obsolete now that 
        we are using TTS
    """
    with open('LLM_response.txt', 'w') as file:
        file.write(text)
