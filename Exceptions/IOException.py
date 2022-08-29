class ModeException(Exception):
    def __init__(self):
        self.message = "ModeException : Conflict between image __mode and requested service"


class NullReferenceException(Exception):
    def __int__(self):
        self.message = "NullReferenceException : Trying to access NoneType variable"
