import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
import os
import helpers
from processor_module import ProcessorModule
import TTS
import sys


openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
# elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]




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