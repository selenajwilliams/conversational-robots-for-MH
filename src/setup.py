import helpers
from helpers import speech_to_text as STT, text_to_speech as TTS
from helpers import CheckInPrompt as prompt

""" Setup file initializes audio files that the program relies on
"""

def setup():
    init_check_in_prompts()


def init_check_in_prompts():
    print("initiallizing check in prompts")

    prompt1 = "How are you feeling?"
    prompt2 = "How are you doing?"
    prompt3 = "How has your day been?"
    
    prompt_1 = prompt("Feeling", prompt1)
    prompt_2 = prompt("Doing", prompt2)
    prompt_3 = prompt("Day been", prompt3)

    check_in_prompts = [prompt_1, prompt_2, prompt_3]

    [STT(x) for x in check_in_prompts]


def init_activations():
    pass

def init_audio_files():
    pass



if __name__ == "__main__":
    setup()