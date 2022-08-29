from HumanMachineInterface.InputInterface import InputInterface as In
from HumanMachineInterface.OutputInterface import OutputInterface as Out

input_device = In()
output_device = Out()

input_device.switch_window()
input_device.print()
input()