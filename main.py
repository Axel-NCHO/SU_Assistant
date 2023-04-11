import threading
import selectors
import traceback
import socket

import Global
from Global import get_username, get_language, reformat_lang, ET

import HumanMachineInterface.OutputInterface
from Brain.Network import Network, MediaCenter, SystemCenter, NetCenter
from HumanMachineInterface.InputInterface import InputInterface
from HumanMachineInterface.OutputInterface import OutputInterface
import libserver

HOST = "127.0.0.1"  # localhost
PORT = 65432
sel = selectors.DefaultSelector()


def wait_for_request():
    while inp.is_listening():
        speech = inp.listen()
        print(speech)
        net.parse_instruction(speech)
    print("Stopped waiting for request.")


def great_user():
    HumanMachineInterface.OutputInterface.speech = root.find("greeting").find(reformat_lang(lang)).find(
        "start").text + " " + user_name + ", " + root.find("greeting").find(reformat_lang(lang)).find("end").text


def set_server_for_external_components():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print(f"Listening on {(HOST, PORT)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


tree = ET.parse("HumanMachineInterface/StandardSpeech.xml")
root = tree.getroot()
Global.tree = tree
Global.root = root

user_name = get_username()
print("Setting up language")
lang = get_language()  # reformat if not called by In/Out interface
Global.lang = lang
print("Setting up input interface")
inp = InputInterface.get_instance(lang)
print("Setting up output interface")
out = OutputInterface.get_instance(lang)
print("Setting up processing centers")
media_center = MediaCenter.get_instance(inp, out)
system_center = SystemCenter.get_instance(inp)
net_center = NetCenter.get_instance()

print("Setting up central network")
net = Network.get_instance(reformat_lang(lang), media_center, system_center, net_center)

print("Setting up server for external components")
set_server_thread = threading.Thread(name="set_server_thread_@alice", target=set_server_for_external_components)
set_server_thread.setDaemon(True)
set_server_thread.start()

# Great user
print("We are all set")
great_user()

wait_for_request_thread = threading.Thread(target=wait_for_request)
wait_for_request_thread.start()

out.show()

# Executed when out is closed
# As it is the main process, all the other threads will exit too as they are daemons.
# However, the process that listens for new requests is not a daemon. It must be explicitly stopped.
# If all threads are not stopped, the program will continue to run in background even if the main
# process (the Tk window) has exited.
inp.stop_listening()
