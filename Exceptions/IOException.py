class ModeException(Exception):
    def __init__(self):
        self.message = "ModeException : Conflict between object mode and requested service"
