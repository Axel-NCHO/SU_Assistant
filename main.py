import threading
import time

import HumanMachineInterface.Interface
from Brain.Network import Network, MediaCenter, get_language
from HumanMachineInterface.InputInterface import InputInterface
from HumanMachineInterface.OutputInterface import OutputInterface

def wait_for_request():
    while True:
        speech = inp.listen()
        print(speech)
        net.parse_instruction(speech)


lang = ""

print("Setting up language")
set_lang = get_language()
if set_lang == "fr":
    lang = "fr-FR"
elif set_lang == "en":
    lang = "en-US"

print("Setting up input interface")
inp = InputInterface(lang)
print("Setting up output interface")
out = OutputInterface(5, 60, 9, lang)
print("Setting up media center")
media_center = MediaCenter(inp, out)
print("Setting up central network")
net = Network(media_center)

# Créer et afficher l'interface
# create_interface_thread = threading.Thread(target=create_interface)
# create_interface_thread.start()

# Great user
# HumanMachineInterface.OutputInterface.speech = "Bonjour, je suis à vôtre disposition"

wait_for_request_thread = threading.Thread(target=wait_for_request)
wait_for_request_thread.start()

out.show()
