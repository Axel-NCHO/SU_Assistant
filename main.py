import threading

import Global
from Global import get_username, get_language, reformat_lang, ET

import HumanMachineInterface.OutputInterface
from Brain.Network import Network, MediaCenter, SystemCenter
from HumanMachineInterface.InputInterface import InputInterface
from HumanMachineInterface.OutputInterface import OutputInterface


def wait_for_request():
    while inp.is_listening():
        speech = inp.listen()
        print(speech)
        net.parse_instruction(speech)
    print("Stopped waiting for request.")


def great_user():
    HumanMachineInterface.OutputInterface.speech = root.find("greeting").find(reformat_lang(lang)).find(
        "start").text + " " + user_name + ", " + root.find("greeting").find(reformat_lang(lang)).find("end").text


tree = ET.parse("HumanMachineInterface/StandardSpeech.xml")
root = tree.getroot()
Global.tree = tree
Global.root = root

user_name = get_username()
print("Setting up language")
lang = get_language()  # must be reformatted if not called by In/Out interface
Global.lang = lang
print("Setting up input interface")
inp = InputInterface(lang)
print("Setting up output interface")
out = OutputInterface(lang)
print("Setting up processing centers")
media_center = MediaCenter(inp, out)
system_center = SystemCenter(inp)
print("Setting up central network")
net = Network(reformat_lang(lang), media_center, system_center)

# Great user
great_user()

wait_for_request_thread = threading.Thread(target=wait_for_request)
wait_for_request_thread.start()

out.show()

# Executed when out is closed
# As it's the main process, all the other threads will exit too as they are daemons.
# But the process that listens for new requests is not a daemon. It must be explicitly stopped.
# If all threads are not stopped, the program will continue to run in background even if the main
# process (the Tk window) has exited.
inp.stop_listening()
