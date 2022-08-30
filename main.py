from Brain.SystemCenter import SystemCenter, SystemInstruction
from Brain.InstructionArgument import Task
from HumanMachineInterface.InputInterface import InputInterface
from HumanMachineInterface.OutputInterface import OutputInterface
import threading

input_device = InputInterface()
output_device = OutputInterface()

system_center = SystemCenter(input_device)
instruction = SystemInstruction(Task.OPEN, "opera", None)


def f1():
    system_center.get_instruction(instruction)


t1 = threading.Thread(target=f1)
t1.start()
output_device.speak("J'ouvre le navigateur opera")
