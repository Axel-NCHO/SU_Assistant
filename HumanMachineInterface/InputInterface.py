# In-project modules
from HumanMachineInterface.IOInterface import IOInterface
from HumanMachineInterface.IOMode import IOMode
from HumanMachineInterface.KeyboardKeys import KeyboardKeys


class InputInterface(IOInterface):
    """
    Input Interface: \n
    Performs all human to machine actions: input_source actions
    """

    __instance = None

    @staticmethod
    def get_instance(lang=None):
        if not InputInterface.__instance:
            if lang:
                InputInterface.__instance = InputInterface(lang)
            else:
                raise RuntimeError("Missing positional argments: language")
        return InputInterface.__instance

    def __init__(self, language: str ="fr-FR"):
        super(InputInterface, self).__init__(IOMode.INPUT, language)
        self.__is_listening = True

    def listen(self) -> str:
        """
        Listen to vocal commands \n
        :return: The text transcript of the vocal command
        """
        return super(InputInterface, self).listen()

    def stop_listening(self):
        self.__is_listening = False

    def is_listening(self):
        return self.__is_listening

    def capture_image(self) -> str:
        """
        Take a photo using default camera \n
        :return: The path to the image
        """
        return super(InputInterface, self).capture_image()

    def capture_video(self) -> str:
        """
        Take a video using default camera \n
        :return: The path to the video
        """
        return super(InputInterface, self).capture_video()

    def capture_screenshot(self) -> str:
        """
        Take a screenshot of the screen \n
        :return: The path to the file
        """
        return super(InputInterface, self).capture_screenshot()

    def save_as(self):
        super(InputInterface, self).touch(KeyboardKeys.SAVE_AS)

    def print(self):
        super(InputInterface, self).touch(KeyboardKeys.PRINT)

    def switch_window(self):
        super(InputInterface, self).touch(KeyboardKeys.SWITCH_WINDOW)

    def switch_tab(self):
        super(InputInterface, self).touch(KeyboardKeys.SWITCH_TAB)

