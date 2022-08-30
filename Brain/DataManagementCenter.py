from abc import ABC, abstractmethod
from Brain.Instructions import Instruction
from Brain.DataStructures import Queue
import threading
import time


class DataManagementCenter(ABC):

    def __init__(self, instructions_type: type):
        self.__Queue = Queue(instructions_type)
        self.__Busy = False
        self.start_watch()

    def get_instruction(self, instruction: Instruction):
        self.await_instruction(instruction)

    def parse_instruction(self, instruction: Instruction):
        return instruction.Task, instruction.Entry, instruction.Output

    @abstractmethod
    def process_instructions(self):
        pass

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
            time.sleep(1)
        self.process_instructions()

    def start_watch(self):
        watch_man = threading.Thread(target=self.watch)
        watch_man.start()
