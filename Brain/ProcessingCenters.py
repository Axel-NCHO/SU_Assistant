from enum import Enum
import HumanMachineInterface.OutputInterface
from Brain.DataManagementCenter import DataManagementCenter
from Brain.Instructions import *
from Brain.System import *
from Brain.InstructionArgument import Task
from HumanMachineInterface.InputInterface import InputInterface, KeyboardKeys
from HumanMachineInterface.OutputInterface import OutputInterface
import Global
import subprocess


class Component(Enum):
    TERMINAL = "terminal"


class MediaCenter(DataManagementCenter):
    __instance = None

    @staticmethod
    def get_instance(input_device=None, output_device=None):
        if not MediaCenter.__instance:
            if input_device and output_device:
                MediaCenter.__instance = MediaCenter(input_device, output_device)
            else:
                raise RuntimeError("Missing positional arguments: input_device and output_device")
        return MediaCenter.__instance

    def __init__(self, input_device: InputInterface, output_device: OutputInterface):
        super(MediaCenter, self).__init__(MediaInstruction)
        self.__Input_Device = input_device
        self.__Output_Device = output_device

    def process_instructions(self, external_instruction=None):
        if not self.is_busy():
            self.set_busy()

            # getting instruction details which depend on whether the instruction is from an external component.
            if external_instruction is None:
                instruction = self.get_next_instruction()
                instruction_task, entry, out = self.parse_instruction(instruction)
            else:
                instruction_task, entry, out = self.parse_instruction(external_instruction)
                # entry must be parsed to recover it as a list of inputs.
                entry = self.parse_entry(entry)

            # triggering the right execution for task
            # return when the instruction is from an external component.
            if instruction_task is Task.TAKE_IMAGE:
                return self.handle_task_take_image(out)

            elif instruction_task is Task.TAKE_SCREENSHOT:
                return self.handle_task_take_screenshot(out)

            elif instruction_task is Task.RECORD_VIDEO:
                return self.handle_task_record_video(out)

            elif instruction_task is Task.PLAY_VIDEO:
                self.handle_task_play_video(entry)

            # allow this center to receive and process further instructions
            # already done in executions that could return something for an external component.
            self.set_not_busy()
            self.start_watch()

    def handle_task_take_image(self, out):
        text_to_say_before = Global.root.find("take_photo").find("before").find(
            Global.reformat_lang(Global.lang)).text
        HumanMachineInterface.OutputInterface.speech = text_to_say_before
        _ = self.__Input_Device.capture_image()
        if out is not None:
            if out == Component.TERMINAL.value:
                state_for_component = True
                response_for_component = "Done"
                self.set_not_busy()
                return state_for_component, response_for_component

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_take_screenshot(self, out):
        text_to_say_before = Global.root.find("take_screenshot").find("before").find(
            Global.reformat_lang(Global.lang)).text
        HumanMachineInterface.OutputInterface.speech = text_to_say_before
        _ = self.__Input_Device.capture_screenshot()
        if out is not None:
            if out == Component.TERMINAL.value:
                state_for_component = True
                response_for_component = "Done"
                self.set_not_busy()
                return state_for_component, response_for_component

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_record_video(self, out):
        text_to_say_before = Global.root.find("record_video").find("before").find(
            Global.reformat_lang(Global.lang)).text
        HumanMachineInterface.OutputInterface.speech = text_to_say_before
        _ = self.__Input_Device.capture_video()
        if out is not None:
            if out == Component.TERMINAL.value:
                state_for_component = True
                response_for_component = "Done"
                self.set_not_busy()
                return state_for_component, response_for_component

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_play_video(self, entry):
        if entry is not None:
            self.__Output_Device.play_video(entry)
        # allowing further instructions will be done in the calling function 'process_instructions'

    def get_external_instruction(self, instruction: Instruction):
        state, response = self.process_instructions(external_instruction=instruction)
        return state, response


class SystemCenter(DataManagementCenter):
    __instance = None

    @staticmethod
    def get_instance(input_device=None):
        if not SystemCenter.__instance:
            if input_device:
                SystemCenter.__instance = SystemCenter(input_device)
            else:
                raise RuntimeError("Missing positional arguments: input_device")
        return SystemCenter.__instance

    def __init__(self, input_device: InputInterface):
        super(SystemCenter, self).__init__(SystemInstruction)
        self.__Input_Device = input_device
        self.__System = System()

    def process_instructions(self, external_instruction=None):
        if not self.is_busy():
            self.set_busy()

            # getting instruction details which depend on whether the instruction is from an external component.
            if external_instruction is None:
                instruction = self.get_next_instruction()
                instruction_task, entry, out = self.parse_instruction(instruction)
            else:
                instruction_task, entry, out = self.parse_instruction(external_instruction)
                entry = self.parse_entry(entry)
                print(entry)

            # triggering the right execution for task
            # return when the instruction is from an external component.
            if instruction_task is Task.OPEN:
                self.handle_task_open(entry)

            elif instruction_task is Task.TELL_TIME:
                return self.handle_task_tell_time(out)

            elif instruction_task is Task.TELL_TIME_SPECIFIC:
                return self.handle_task_tell_time_specific(entry, out)

            elif instruction_task is Task.TELL_DATE:
                return self.handle_task_tell_date(out)

            elif instruction_task is Task.SWITCH_WINDOW:
                self.handle_task_switch_window()

            elif instruction_task is Task.SWITCH_TAB:
                self.handle_task_switch_tab()

            elif instruction_task is Task.PRINT:
                self.handle_task_print()

            elif instruction_task is Task.SAVE_AS:
                self.handle_task_save_as()

            elif instruction_task is Task.PLAY_PAUSE:
                self.handle_task_play_pause()

            # allow this center to receive and process further instructions
            # already done in executions that could return something for an external component.
            self.set_not_busy()
            self.start_watch()

    def handle_task_open(self, entry):
        if entry is not None:
            entry = entry.upper()
            if "OPERA" in entry:
                self.__Input_Device.open_app("opera")
        # allowing further instructions will be done in the calling function 'process_instructions'

    def handle_task_tell_time(self, out):
        time = self.__System.get_time()
        if out is not None:
            if out == Component.TERMINAL.value:
                state_for_component = True
                response_for_component = f"{time[0]}h{time[1]}"
                self.set_not_busy()
                return state_for_component, response_for_component
        text_to_say_after = \
        f"{Global.root.find('tell_time').find('before').find(Global.reformat_lang(Global.lang)).text}" + \
        f"{time[0]} " + \
        f"{Global.root.find('tell_time').find('after').find('hours').find(Global.reformat_lang(Global.lang)).text} "+\
        f"{Global.root.find('tell_time').find('between').find(Global.reformat_lang(Global.lang)).text} " + \
        f"{time[1]} " + \
        f"{Global.root.find('tell_time').find('after').find('minutes').find(Global.reformat_lang(Global.lang)).text}"
        HumanMachineInterface.OutputInterface.speech = text_to_say_after

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_tell_time_specific(self, entry, out):
        if out is not None:
            if out == Component.TERMINAL.value:
                time = self.__System.get_time_specific_region(entry[0].capitalize())  # entry[2] is the region
                state_for_component = True
                response_for_component = f"Region: {entry[0].capitalize()}\nTime: {time[0]}h{time[1]}"
                self.set_not_busy()
                return state_for_component, response_for_component
        time = self.__System.get_time_specific_region(entry[2].capitalize())  # entry[2] is the region
        # translated to english because get_time_specific() needs it.
        text_to_say_after = \
        f"{Global.root.find('tell_time').find('before').find(Global.reformat_lang(Global.lang)).text}" + \
        f"{time[0]} " + \
        f"{Global.root.find('tell_time').find('after').find('hours').find(Global.reformat_lang(Global.lang)).text}" + \
        f"{Global.root.find('tell_time').find('between').find(Global.reformat_lang(Global.lang)).text}" + \
        f"{time[1]} " + \
        f"{Global.root.find('tell_time').find('after').find('minutes').find(Global.reformat_lang(Global.lang)).text}"+\
        f"{entry[0]} {entry[1]}"  # entry[0] is the preposition used and entry[1] is
        # the name of the region in the original language
        HumanMachineInterface.OutputInterface.speech = text_to_say_after

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_tell_date(self, out):
        date = self.__System.get_date()
        text_to_say_after = f"{Global.root.find('tell_date').find(Global.reformat_lang(Global.lang)).text} " + \
                            f"{Global.en_fr_translator.translate(date[0])} " + \
                            f"{date[1]} " + \
                            f"{Global.en_fr_translator.translate(date[2])} " + \
                            f"{date[3]}"
        if out is not None:
            if out == Component.TERMINAL.value:
                state_for_component = True
                response_for_component = text_to_say_after
                self.set_not_busy()
                return state_for_component, response_for_component
        HumanMachineInterface.OutputInterface.speech = text_to_say_after

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_switch_window(self):
        HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
            Global.reformat_lang(Global.lang)).text
        self.__Input_Device.touch(KeyboardKeys.SWITCH_WINDOW)
        # allowing further instructions will be done in the calling function 'process_instructions'

    def handle_task_switch_tab(self):
        HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
            Global.reformat_lang(Global.lang)).text
        self.__Input_Device.touch(KeyboardKeys.SWITCH_TAB)
        # allowing further instructions will be done in the calling function 'process_instructions'

    def handle_task_print(self):
        HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
            Global.reformat_lang(Global.lang)).text
        self.__Input_Device.touch(KeyboardKeys.PRINT)
        # allowing further instructions will be done in the calling function 'process_instructions'

    def handle_task_save_as(self):
        HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
            Global.reformat_lang(Global.lang)).text
        self.__Input_Device.touch(KeyboardKeys.SAVE_AS)
        # allowing further instructions will be done in the calling function 'process_instructions'

    def handle_task_play_pause(self):
        HumanMachineInterface.OutputInterface.speech = Global.root.find('understood').find(
            Global.reformat_lang(Global.lang)).text
        self.__Input_Device.touch(KeyboardKeys.SPACE)
        # allowing further instructions will be done in the calling function 'process_instructions'

    def get_external_instruction(self, instruction: Instruction):
        state, response = self.process_instructions(external_instruction=instruction)
        return state, response


class NetCenter(DataManagementCenter):
    __instance = None

    @staticmethod
    def get_instance():
        if not NetCenter.__instance:
            NetCenter.__instance = NetCenter()
        return NetCenter.__instance

    def __init__(self):
        super(NetCenter, self).__init__(NetInstruction)

    def process_instructions(self, external_instruction=None):
        if not self.is_busy():
            self.set_busy()

            # getting instruction details which depend on whether the instruction is from an external component.
            if external_instruction is None:
                instruction = self.get_next_instruction()
                instruction_task, entry, out = self.parse_instruction(instruction)
            else:
                instruction_task, entry, out = self.parse_instruction(external_instruction)
                entry = self.parse_entry(entry)
                print(entry)

            # triggering the right execution for task
            # return when the instruction is from an external component.
            if instruction_task is Task.LOOK_UP:
                return self.handle_task_lookup(entry, out)
            if instruction_task is Task.OPEN:
                return self.handle_task_open_browser(out)

            # allow this center to receive and process further instructions
            # already done in executions that could return something for an external component.
            self.set_not_busy()
            self.start_watch()

    def handle_task_lookup(self, entry, out):
        if out is not None:
            if out == Component.TERMINAL.value:
                search = " ".join(entry)
                _ = subprocess.Popen(args=f"python InternalComponents/Browser/main.py \"{search}\"")
                state_for_component = True
                response_for_component = "See results in the browser"
                self.set_not_busy()
                return state_for_component, response_for_component
        _ = subprocess.Popen(args=f"python InternalComponents/Browser/main.py \"{entry}\"")
        HumanMachineInterface.OutputInterface.speech = Global.root.find("look_up").find(
            Global.reformat_lang(Global.lang)).text

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def handle_task_open_browser(self, out):
        if out is not None:
            if out == Component.TERMINAL.value:
                _ = subprocess.Popen(args=f"python InternalComponents/Browser/main.py")
                state_for_component = True
                response_for_component = "Browser opened successfully"
                self.set_not_busy()
                return state_for_component, response_for_component
        _ = subprocess.Popen(args=f"python InternalComponents/Browser/main.py")
        text_to_say = Global.root.find("understood").find(
            Global.reformat_lang(Global.lang)).text + ". " + \
            Global.root.find("open").find("before").find(
            Global.reformat_lang(Global.lang)).text + " " + \
            Global.root.find("open").find("after").find("browser").find(
            Global.reformat_lang(Global.lang)).text
        HumanMachineInterface.OutputInterface.speech = text_to_say

        # allow this center to receive and process further instructions
        self.set_not_busy()
        self.start_watch()

    def get_external_instruction(self, instruction: Instruction):
        state, response = self.process_instructions(external_instruction=instruction)
        return state, response
