from gtts import gTTS # Google Text-to-Speech
from dataclasses import dataclass


""" Dataclasses
"""
@dataclass
class cPrompt: # check in prompt
    """ Class representing the check-in prompts that the robot will ask to 
        initiate conversation
    """
    title: str
    prompt: str
    folder: str


""" Contains helper functions to streamline code in main file
"""

def text_to_speech():
    language = "en"
    speech = gTTS(text=cPrompt.prompt, lang=language, slow=False, tld="com.au")
    speech.save(cPrompt.folder + cPrompt.title + ".mp3")
    # speech.save("../out/testAudio.mp3")
    print(f"printing {cPrompt.prompt} to {cPrompt.title}.mp3")
    pass


def speech_to_text(prompt: cPrompt): # use whisper AI for this?
    pass
