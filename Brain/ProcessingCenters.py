import os

import FileManager
import HumanMachineInterface.OutputInterface
from Brain.DataManagementCenter import DataManagementCenter
from Brain.Instructions import *
from Brain.System import *
from Brain.InstructionArgument import Task
from HumanMachineInterface.InputInterface import InputInterface, KeyboardKeys
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
            elif instruction_task is Task.TELL_TIME:
                time = self.__System.get_time()
                text_to_say_after = f"{Global.root.find('tell_time').find('before').find(Global.reformat_lang(Global.lang)).text}" + \
                                    f"{time[0]} " + \
                                    f"{Global.root.find('tell_time').find('after').find('hours').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{Global.root.find('tell_time').find('between').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{time[1]} " + \
                                    f"{Global.root.find('tell_time').find('after').find('minutes').find(Global.reformat_lang(Global.lang)).text}"
                HumanMachineInterface.OutputInterface.speech = text_to_say_after
            elif instruction_task is Task.TELL_TIME_SPECIFIC:
                time = self.__System.get_time_specific_region(entry[2].capitalize())    # entry[2] is the region
                # translated to english because get_time_specific() needs it
                text_to_say_after = f"{Global.root.find('tell_time').find('before').find(Global.reformat_lang(Global.lang)).text}" + \
                                    f"{time[0]} " + \
                                    f"{Global.root.find('tell_time').find('after').find('hours').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{Global.root.find('tell_time').find('between').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{time[1]} " + \
                                    f"{Global.root.find('tell_time').find('after').find('minutes').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{entry[0]} {entry[1]}"  # entry[0] is the preposition used and entry[1] is
                # the name of the region in the original language
                HumanMachineInterface.OutputInterface.speech = text_to_say_after
            elif instruction_task is Task.TELL_DATE:
                date = self.__System.get_date()
                text_to_say_after = f"{Global.root.find('tell_date').find(Global.reformat_lang(Global.lang)).text} " + \
                                    f"{Global.en_fr_translator.translate(date[0])} " + \
                                    f"{date[1]} " + \
                                    f"{Global.en_fr_translator.translate(date[2])} " + \
                                    f"{date[3]}"
                HumanMachineInterface.OutputInterface.speech = text_to_say_after
            elif instruction_task is Task.SWITCH_WINDOW:
                HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(Global.reformat_lang(Global.lang)).text
                self.__Input_Device.touch(KeyboardKeys.SWITCH_WINDOW)
            elif instruction_task is Task.SWITCH_TAB:
                HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(Global.reformat_lang(Global.lang)).text
                self.__Input_Device.touch(KeyboardKeys.SWITCH_TAB)
            elif instruction_task is Task.PRINT:
                HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
                    Global.reformat_lang(Global.lang)).text
                self.__Input_Device.touch(KeyboardKeys.PRINT)
            elif instruction_task is Task.SAVE_AS:
                HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
                    Global.reformat_lang(Global.lang)).text
                self.__Input_Device.touch(KeyboardKeys.SAVE_AS)

            self.set_not_busy()
            self.start_watch()
