# ------------- MODULES -----------------
# Modules for abstract class
from abc import ABC, abstractmethod

# Modules for file management
import os

# Modules for recognition and synthesis alias senses
import speech_recognition as sr
import pyttsx3
import cv2 as cv

# In-project modules
from Exceptions.IOException import ModeException


# ------------ END MODULES ----------------
# ------------ STATIC FUNCTIONS -------------------
def check_mode(mode1, mode2):
    if mode1 != mode2:
        raise ModeException()

def show_image(image, title="Image"):
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyWindow(title)

# ------------ END STATIC FUNCTIONS -------------------


class IOInterface(ABC):

    def __init__(self, mode, language="fr-FR"):
        self.IOLanguage = language
        self.mode = mode
        if mode.value == "Input":
            # ears
            self.Recognizer = sr.Recognizer()
            # eyes
            self.Camera = None
            # default
            self.defaultImageName = "image.jpg"
            self.defaultVideoName = "video.avi"
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


    def open_camera(self, input=None):
        if input is None:
            self.Camera = cv.VideoCapture(0)
        else:
            self.Camera = cv.VideoCapture(input)

        if (self.Camera is None) or (not self.Camera.isOpened()):
            print("Impossible d'ouvrir la caméra")
            exit(1)

    def capture_image(self):
        try:
            check_mode(self.mode.value, "Input")
            self.open_camera()

            exit_state, image = self.Camera.read()
            if exit_state:
                cv.imwrite(self.defaultImageName, image)
                show_image(image)
                self.Camera.release()
                return self.defaultImageName

        except ModeException as e:
            print(e.message)

    def play_video(self, videoPath):
        try:

            check_mode(self.mode.value, "Output")
            self.open_camera(videoPath)

            while self.Camera.isOpened():
                exit_state, frame = self.Camera.read()
                cv.imshow('frame', frame)
                if cv.waitKey(25) == ord('q'):
                    break
            self.Camera.release()
            cv.destroyAllWindows()

        except ModeException as e:
            print(e.message)


    def capture_video(self):
        try:
            check_mode(self.mode.value, "Input")
            self.open_camera()

            fourcc = cv.VideoWriter_fourcc(*'XVID')
            out = cv.VideoWriter(self.defaultVideoName, fourcc, 30.0, (640, 480))

            while self.Camera.isOpened():
                exit_state, frame = self.Camera.read()
                if exit_state:
                    out.write(frame)
                    cv.imshow('frame', frame)
                    if cv.waitKey(1) == ord('q'):
                        break

            self.Camera.release()
            out.release()
            cv.destroyAllWindows()
            return self.defaultVideoName

        except ModeException as e:
            print(e.message)


    def speak(self, text):
        try:
            check_mode(self.mode.value, "Output")
            self.Speaker.say("J'ai entendu " + text)
            self.Speaker.runAndWait()

        except ModeException as e:
            print(e.message)