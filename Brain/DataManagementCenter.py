from abc import ABC, abstractmethod
from Brain.Instructions import Instruction
from Brain.DataStructures import Queue
from Brain.Threading import Threading
from time import sleep


class DataManagementCenter(ABC):

    def __init__(self, instructions_type: type):
        self.__Queue = Queue(instructions_type)
        self.__Busy = False
        self.start_watch()

    def get_instruction(self, instruction: Instruction):
        self.await_instruction(instruction)

    def get_external_instruction(self, instruction: Instruction):
        pass

    def parse_instruction(self, instruction: Instruction):
        return instruction.Task, instruction.Entry, instruction.Output

    @abstractmethod
    def process_instructions(self):
        pass

    def parse_entry(self, entry: str):
        args = entry[1:len(entry)-1]
        args = args.split("'")
        pos = 0
        while pos != len(args):
            if not (args[pos].isalpha() or args[pos].isnumeric()):
                del args[pos]
                pos = 0
            else:
                pos += 1
        return args

    def await_instruction(self, instruction: Instruction):
        self.__Queue.enqueue(instruction)

    def get_next_instruction(self) -> Instruction:
        return self.__Queue.dequeue()

    def is_busy(self):
        return self.__Busy

    def get_queue(self):
        return self.__Queue

    def set_busy(self):
        self.__Busy = True

    def set_not_busy(self):
        self.__Busy = False

    def watch(self):
        while self.__Queue.is_empty():
            sleep(1)
        self.process_instructions()

    def start_watch(self):
        Threading.start_thread(target=self.watch, daemon=True)
