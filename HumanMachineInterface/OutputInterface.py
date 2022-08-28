# In-project modules
from HumanMachineInterface.IOInterface import *
from HumanMachineInterface.IOMode import *


class OutputInterface(IOInterface):

    def __init__(self, language="fr-FR"):
        super(OutputInterface, self).__init__(IOMode.OUTPUT, language)

    def speak(self, text):
        super(OutputInterface, self).speak(text)

    def play_video(self, videoPath):
        super(OutputInterface, self).play_video(videoPath)
