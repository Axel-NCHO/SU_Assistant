# In-project modules
from HumanMachineInterface.IOInterface import *
from HumanMachineInterface.IOMode import *


class InputInterface(IOInterface):

    def __init__(self, language="fr-FR"):
        super(InputInterface, self).__init__(IOMode.INPUT, language)

    def listen(self):
        return super(InputInterface, self).listen()
