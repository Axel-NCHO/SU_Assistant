import os

import FileManager
import HumanMachineInterface.OutputInterface
from Brain.DataManagementCenter import DataManagementCenter
from Brain.Instructions import *
from Brain.System import *
from Brain.InstructionArgument import Task
from HumanMachineInterface.InputInterface import InputInterface
from HumanMachineInterface.OutputInterface import OutputInterface
import Global


class MediaCenter(DataManagementCenter):

    def __init__(self, input_device: InputInterface, output_device: OutputInterface):
        super(MediaCenter, self).__init__(MediaInstruction)
        self.__Input_Device = input_device
        self.__Output_Device = output_device

    def process_instructions(self):
        if not self.is_busy():
            self.set_busy()

            instruction = self.get_next_instruction()
            instruction_task, entry, out = self.parse_instruction(instruction)

            if instruction_task is Task.TAKE_IMAGE:
                text_to_say_before = Global.root.find("take_photo").find("before").find(
                    Global.reformat_lang(Global.lang)).text
                HumanMachineInterface.OutputInterface.speech = text_to_say_before
                image = self.__Input_Device.capture_image()
                if out is not None:
                    FileManager.move_file(image, out)
            elif instruction_task is Task.TAKE_SCREENSHOT:
                text_to_say_before = Global.root.find("take_screenshot").find("before").find(
                    Global.reformat_lang(Global.lang)).text
                HumanMachineInterface.OutputInterface.speech = text_to_say_before
                image = self.__Input_Device.capture_screenshot()
                if out is not None:
                    FileManager.move_file(image, out)
            elif instruction_task is Task.RECORD_VIDEO:
                text_to_say_before = Global.root.find("record_video").find("before").find(
                    Global.reformat_lang(Global.lang)).text
                HumanMachineInterface.OutputInterface.speech = text_to_say_before
                video = self.__Input_Device.capture_video()
                if out is not None:
                    FileManager.move_file(video, out)
            elif instruction_task is Task.PLAY_VIDEO:
                if entry is not None:
                    self.__Output_Device.play_video(entry)

            self.set_not_busy()
            self.start_watch()


class SystemCenter(DataManagementCenter):

    def __init__(self, input_device: InputInterface):
        super(SystemCenter, self).__init__(SystemInstruction)
        self.__Input_Device = input_device
        self.__System = System()

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
            if instruction_task is Task.TELL_TIME:
                text_to_say_before = Global.root.find("tell_time").find("before").find(Global.reformat_lang(Global.lang)).text
                HumanMachineInterface.OutputInterface.speech = text_to_say_before
                time = self.__System.get_time()
                text_to_say_after = f"{time[0]} " + \
                                    f"{Global.root.find('tell_time').find('after').find('hours').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{Global.root.find('tell_time').find('between').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{time[1]} " + \
                                    f"{Global.root.find('tell_time').find('after').find('minutes').find(Global.reformat_lang(Global.lang)).text}"
                HumanMachineInterface.OutputInterface.speech = text_to_say_after

            self.set_not_busy()
            self.start_watch()
