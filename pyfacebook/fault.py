class FacebookException(Exception):

    """
    A custom Facebook Exception class

    """

    def __init__(self, message, code=None):
        custom_message = "Facebook API Error: " + message
        if code:
            custom_message += "\nError Code: " + str(code)

        Exception.__init__(self, custom_message)
