
def crisis_monitoring(user_input: str) -> bool:
    """ Checks user_input to see if crisis_words exist 
        If so, return true
    """
    # mocking with non-crisis words to test functionality 
    crisis_words = ["cat", "dog", "bird"]
    ## TODO: fill this in
    pass

def get_crisis_response() -> str:
    """ defines a crisis response tring that is returned 
    """
    crisis_response = ""
    return crisis_response
    pass

# for early testing:
user_response = "I have a dog" # test with this
is_crisis = crisis_monitoring(user_response)
# finish coding here