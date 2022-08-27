# ------------- MODULES -----------------
# Modules for abstract class
from abc import ABC, abstractmethod

# Modules for speech recognition and synthesis
import speech_recognition as sr
import pyttsx3

# In-project modules
from Exceptions.IOException import ModeException


# ------------ END MODULES ----------------
# ------------ STATIC FUNCTIONS -------------------
def check_mode(mode1, mode2):
    if mode1 != mode2:
        raise ModeException()

# ------------ END STATIC FUNCTIONS -------------------


class IOInterface(ABC):

    def __init__(self, mode, language="fr-FR"):
        self.IOLanguage = language
        self.mode = mode
        if mode.value == "Input":
            self.Recognizer = sr.Recognizer()
        else:
            self.Speaker = pyttsx3.init()


    def listen(self):
        try:
            check_mode(self.mode.value, "Input")
            with sr.Microphone() as speech_source:
                self.Recognizer.adjust_for_ambient_noise(speech_source, duration=0.3)

                print("J'écoute ...")
                speech = self.Recognizer.listen(speech_source)

                # Using google to recognize audio
                text = self.Recognizer.recognize_google(speech, language=self.IOLanguage)
                text = text.lower()

                return text

        except ModeException as e:
            print(e.message)
            return ""

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return "Veuillez repéter"

        except sr.UnknownValueError:
            return "Veuillez repéter"


    def speak(self, text):
        try:
            check_mode(self.mode.value, "Output")
            self.Speaker.say("J'ai entendu " + text)
            self.Speaker.runAndWait()

        except ModeException as e:
            print(e.message)