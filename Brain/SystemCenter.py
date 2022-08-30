import os
from Brain.DataManagementCenter import DataManagementCenter
from Brain.Instructions import SystemInstruction
from Brain.InstructionArgument import Task
from HumanMachineInterface.InputInterface import InputInterface


class SystemCenter(DataManagementCenter):

    def __init__(self, input_device: InputInterface):
        super(SystemCenter, self).__init__(SystemInstruction)
        self.__Input_Device = input_device

    def process_instructions(self):
        if not self.is_busy():
            self.set_busy()

            instruction = self.get_next_instruction()
            instruction_task, entry, out = self.parse_instruction(instruction)

            if instruction_task is Task.OPEN:
                if entry is not None:
                    entry = entry.upper()
                    if "OPERA" in entry:
                        os.system("start opera")

            self.set_not_busy()
            self.start_watch()
