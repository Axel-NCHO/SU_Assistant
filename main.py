from HumanMachineInterface.InputInterface import InputInterface as In
from HumanMachineInterface.OutputInterface import OutputInterface as Out

input_device = In()
output_device = Out()


while True:
    saying = input_device.listen()
    print(saying)
    output_device.speak(saying)
