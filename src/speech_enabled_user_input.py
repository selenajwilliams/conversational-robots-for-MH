""" This file just saves a version of get_user_response() that can
    verbal user responses by listening for speech and converting 
    that to text.

    It can be used in place of the get_user_response() function in
    app.py which gets the user response by reading in a text file.

    The logic outside of both of these functions remains the same. 
    Both functions return the user input as text, and from there 
    that user_input is checked to see if it is new & non-empty. 
    If so, it is processed from there.

    BUGS:
    I have a bug with this being sent to the whisper api - something in
    the syntax isn't right. For this function to work that will need to
    be fixed.

    TO USE:
    Swap this out with the get_user_response() function in app.py and
    fix the bug mentioned above :)

"""

# this part below has to do with real time speech recognition & speech to text using the whisper API, 
# which will enable the get_user_response function above
def get_user_response():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Listening for speech...")

    with microphone as source:
        try:
            print("Start speaking!")
            recognizer.adjust_for_ambient_noise(source) # optional
            # save the audio data
            # params: 
                # timeout: if no speech is detected within 10 seconds, sr will throw an error or not record
                # phrase_time_limit: audio stops listening after speech is not detected for 3 seconds 
                #                    (end of speech detection) ^
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)  # Listen for up to 3 seconds of speech
            
            # save audio to file 
            with open("user_speech.wav", "wb") as audio_file:
                audio_file.write(audio.get_wav_data())
            
            # send audio file to whisper api to be transcribed
            transcript = openai.Audio.transcribe("whisper-1", audio_file.read())
            print(f"\n***SPEECH TRANSCRIPTION***\n{transcript}")
            return transcript
        
        except Exception as e:
            # if any exception occurs, print it to see what it is
            print(f"error encountered: {e}")