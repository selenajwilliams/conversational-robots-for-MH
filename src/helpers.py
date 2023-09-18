from gtts import gTTS


""" Contains helper functions to streamline code in main file
"""

def text_to_speech():
    pass

def speech_to_text(text):
    language = "en"
    speech = gTTS(text=text, lang=language, slow=False, tld="com.au")
    speech.save("testAudio.mp3")
    # speech.save("../out/testAudio.mp3")
    pass