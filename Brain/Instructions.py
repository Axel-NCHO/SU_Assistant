from abc import ABC
from Brain.InstructionArgument import Group, Task


class Instruction(ABC):

    def __init__(self, group: Group, task: Task, entry_data, output_data):
        self.Group = group
        self.Task = task
        self.Entry = entry_data
        self.Output = output_data

    def __eq__(self, other):
        if other is None:
            return False
        return self.Group.value == other.Group.value and self.Task.value == other.Task.value and self.Entry == other.Entry and self.Output == other.Output


class MediaInstruction(Instruction):

    def __init__(self, task: Task, entry_data, output_data):
        super(MediaInstruction, self).__init__(Group.MEDIA, task, entry_data, output_data)

    def __eq__(self, other):
        return isinstance(other, MediaInstruction) and super(MediaInstruction, self).__eq__(other)


class SystemInstruction(Instruction):

    def __init__(self, task: Task, entry_data, output_data):
        super(SystemInstruction, self).__init__(Group.SYSTEM, task, entry_data, output_data)

    def __eq__(self, other):
        return isinstance(other, SystemInstruction) and super(SystemInstruction, self).__eq__(other)


class MemoryInstruction(Instruction):

    def __init__(self, task: Task, entry_data, output_data):
        super(MemoryInstruction, self).__init__(Group.MEMORY, task, entry_data, output_data)

    def __eq__(self, other):
        return isinstance(other, MemoryInstruction) and super(MemoryInstruction, self).__eq__(other)


class NetInstruction(Instruction):

    def __init__(self, task: Task, entry_data, output_data):
        super(NetInstruction, self).__init__(Group.NET, task, entry_data, output_data)

    def __eq__(self, other):
        return isinstance(other, NetInstruction) and super(NetInstruction, self).__eq__(other)


class ConverseInstruction(Instruction):

    def __init__(self, task: Task, entry_data, output_data):
        super(ConverseInstruction, self).__init__(Group.CONVERSE, task, entry_data, output_data)

    def __eq__(self, other):
        return isinstance(other, ConverseInstruction) and super(ConverseInstruction, self).__eq__(other)
