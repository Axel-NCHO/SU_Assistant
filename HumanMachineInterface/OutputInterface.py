# In-project modules
from HumanMachineInterface.IOInterface import *
from HumanMachineInterface.IOMode import *


class OutputInterface(IOInterface):
    """
    Output Interface: \n
    Performs all machine to human operations: output actions
    """

    def __init__(self, language: str = "fr-FR"):
        super(OutputInterface, self).__init__(IOMode.OUTPUT, language)

    def speak(self, text: str):
        """
        Speak information(s) with installed voices \n
        :param text: Information to be spoken
        """
        super(OutputInterface, self).speak(text)

    def play_video(self, videoPath: str):
        """
        Play a video file \n
        :param videoPath: Path to th video file
        """
        super(OutputInterface, self).play_video(videoPath)
