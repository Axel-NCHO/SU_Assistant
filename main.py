from HumanMachineInterface.InputInterface import InputInterface as In
from HumanMachineInterface.OutputInterface import OutputInterface as Out

input_device = In()
output_device = Out()


imagePath = input_device.capture_image()
