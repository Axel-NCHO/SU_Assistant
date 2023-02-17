# ------------- MODULES -----------------
# Modules for abstract class
import os
from abc import ABC, abstractmethod

# Modules for senses
import speech_recognition as sr
import pyttsx3
import keyboard

# Modules for media management
import cv2 as cv
from pyautogui import screenshot

import HumanMachineInterface.OutputInterface
# In-project modules
from Exceptions.IOException import ModeException, NullReferenceException
from HumanMachineInterface.IOMode import IOMode
from HumanMachineInterface.KeyboardKeys import KeyboardKeys
import FileManager
import Global


# ------------ END MODULES ----------------
# ------------ STATIC FUNCTIONS -------------------
def check_mode(mode1: str, mode2: str):
    if mode1 != mode2:
        raise ModeException()

def show_image(image, title: str ="Image"):
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyWindow(title)

# ------------ END STATIC FUNCTIONS -------------------


class IOInterface(ABC):

    def __init__(self, mode: IOMode, language: str ="fr-FR"):
        self.__IOLanguage = language
        self.__mode = mode
        if mode.value == "Input":
            # ears
            self.__Recognizer = sr.Recognizer()
            # eyes
            self.__Camera = None
            # touch
            self.__Keyboard_Key: KeyboardKeys = None
            # states
            self.camera_in_use = False
        else:
            # mouth
            self.__Speaker = pyttsx3.init()
            self.set_voice_language()

    def set_voice_language(self):
        try:
            check_mode(self.__mode.value, "Output")
            gender = "VoiceGenderMale"
            for voice in self.__Speaker.getProperty('voices'):
                if self.__IOLanguage in voice.languages and voice.gender == gender:
                    self.__Speaker.setProperty('voice', voice.id)
                    return
            # raise RuntimeError("Language '{}' for gender '{}' not found".format(self.__IOLanguage, gender))

        except ModeException as e:
            print("Mode exceptio,: ", e.message)

    def listen(self) -> str:
        try:
            check_mode(self.__mode.value, "Input")
            with sr.Microphone() as speech_source:
                self.__Recognizer.adjust_for_ambient_noise(speech_source, duration=0.3)

                print("J'écoute ...")
                speech = self.__Recognizer.listen(speech_source)

                # Using google to recognize audio
                text = self.__Recognizer.recognize_google(speech, language=self.__IOLanguage)
                text = text.lower()

                return text

        except ModeException as e:
            print("Mode exception: ", e.message)
            return ""

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return "Veuillez repéter"

        except sr.UnknownValueError:
            return "Veuillez repéter"

        except Exception as e:
            print("Exception: \n", e)
            return ""


    def open_camera(self, input: str =None):
        try:
            if input is None:
                self.__Camera = cv.VideoCapture(0)
            else:
                self.__Camera = cv.VideoCapture(input)

            if not self.__Camera.isOpened():
                print("Impossible d'ouvrir la caméra")
                HumanMachineInterface.OutputInterface.speech = "Impossible d'ouvrir la caméra."
                # exit(1)
            self.camera_in_use = True
        except Exception as e:
            print(e)

    def close_camera(self):
        self.__Camera.release()
        self.__Camera = None
        self.camera_in_use = False


    def capture_image(self) -> str:
        try:
            check_mode(self.__mode.value, "Input")
            self.open_camera()

            exit_state, image = self.__Camera.read()
            if exit_state:
                fileName = FileManager.save_image(image)
                text_to_say_after = Global.root.find("take_photo").find("after").find(
                    Global.reformat_lang(Global.lang)).text
                HumanMachineInterface.OutputInterface.speech = text_to_say_after
                show_image(image)
                self.close_camera()
                return fileName

        except ModeException as e:
            print(e.message)
            return None

        except Exception as e:
            print(e)
            return None

    def play_video(self, videoPath: str):
        try:
            check_mode(self.__mode.value, "Output")
            self.open_camera(videoPath)

            while self.__Camera.isOpened():
                exit_state, frame = self.__Camera.read()
                cv.imshow('frame', frame)
                if cv.waitKey(25) == ord('q'):
                    break
            self.close_camera()
            cv.destroyAllWindows()

        except ModeException as e:
            print(e.message)

        except Exception as e:
            print(e)


    def capture_video(self) -> str:
        try:
            check_mode(self.__mode.value, "Input")
            self.open_camera()

            FileManager.config_video_saver()

            while self.__Camera.isOpened():
                exit_state, frame = self.__Camera.read()
                if exit_state:
                    FileManager.save_video_frame_by_frame(frame)
                    cv.imshow('frame', frame)
                    if cv.waitKey(1) == ord('q'):
                        break
            text_to_say_after = Global.root.find("record_video").find("after").find(
                Global.reformat_lang(Global.lang)).text
            HumanMachineInterface.OutputInterface.speech = text_to_say_after
            self.close_camera()
            FileManager.reset_video_saver()
            cv.destroyAllWindows()
            return FileManager.video_name

        except ModeException as e:
            print(e.message)

        except NullReferenceException as e:
            print(e.message)

        except Exception as e:
            print(e)

    def capture_screenshot(self) -> str:
        try:
            check_mode(self.__mode.value, "Input")
            screensht = screenshot()
            image = FileManager.convert_img_to_cv_format(screensht)
            text_to_say_after = Global.root.find("take_screenshot").find("after").find(
                Global.reformat_lang(Global.lang)).text
            HumanMachineInterface.OutputInterface.speech = text_to_say_after
            show_image(image, title="screenshot")
            return FileManager.save_image(image)

        except ModeException as e:
            print(e.message)
            return None
        except Exception as e:
            print(e)
            return None

    def open_app(self, app: str):
        """Works only on Windows.
        Opens the specified app if it's installed on the host device"""

        try:
            check_mode(self.__mode.value, "Input")
            os.system(f"start {app}")
        except ModeException as e:
            print(e.message)


    def speak(self, text: str):
        try:
            check_mode(self.__mode.value, "Output")
            self.__Speaker.say(text)
            self.__Speaker.runAndWait()

        except ModeException as e:
            print(e.message)

        except Exception as e:
            print(e)


    def touch(self, keyboardkey: KeyboardKeys):
        try:
            check_mode(self.__mode.value, "Input")
            self.__Keyboard_Key = keyboardkey
            keyboard.press_and_release(self.__Keyboard_Key.value)
            self.__Keyboard_Key = None

        except ModeException as e:
            print(e.message)
        except Exception as e:
            print(e)




