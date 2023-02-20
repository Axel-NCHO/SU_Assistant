import spacy
from spacy.matcher import Matcher
from playsound import playsound

import Global
import HumanMachineInterface.OutputInterface
from Brain.ProcessingCenters import *
from Brain.Instructions import MediaInstruction
from Brain.Patterns import *


class Network:

    def __init__(self, language: str, media_center: MediaCenter, system_center: SystemCenter,
                 net_center: NetCenter):
        self.__language = language
        self.__nlp = self.get_vocab()
        self.__matcher = self.config_matcher()

        self.__media_center = media_center
        self.__system_center = system_center
        self.__net_center = net_center

        self.__attempts_count: int = 0
        self.__MAX_ATTEMPTS_COUNT: int = 3
        self.__NAME: str = "alice"
        self.__stand_by = False

    def get_vocab(self):
        if self.__language == "fr":
            return spacy.load("fr_core_news_sm", disable=["parser"])
        if self.__language == "en":
            return spacy.load("en_core_web_sm", disable=["parser"])
        return spacy.blank("fr")

    def parse_instruction(self, instruction: str):

        text = instruction
        if text == self.__NAME:
            HumanMachineInterface.OutputInterface.speech = Global.root.find("pay_attention").find(self.__language).text
            if self.__stand_by:
                self.__attempts_count = 0
                self.__stand_by = False
                print("out of stand-by")
            return
        elif not text.startswith(self.__NAME):
            if self.__stand_by:
                print("no")
                return
        else:
            text = self.__trim_name(text)
            if self.__stand_by:
                self.__attempts_count = 0
                self.__stand_by = False
                print("out of stand-by")

        lookup_keyword = Global.root.find("look_up").find("keyword").find(Global.reformat_lang(Global.lang)).text
        if text.startswith(lookup_keyword):
            self.__net_center.get_instruction(NetInstruction(Task.LOOK_UP, text[len(lookup_keyword)+1:], None))
            return

        doc = self.__nlp(text)

        # Find instruction group
        matches = self.__matcher(doc)

        if len(matches) != 0:
            patterns_matched_ids = [doc.vocab.strings[match[0]] for match in matches]
            # media
            if PHOTO_PATTERN in patterns_matched_ids:
                self.__media_center.get_instruction(MediaInstruction(Task.TAKE_IMAGE, None, None))
            if VIDEO_PATTERN in patterns_matched_ids:
                self.__media_center.get_instruction(MediaInstruction(Task.RECORD_VIDEO, None, None))
            if SCREENSHOT_PATTERN in patterns_matched_ids:
                self.__media_center.get_instruction(MediaInstruction(Task.TAKE_SCREENSHOT, None, None))
            if TIME_SPECIFIC_PATTERN in patterns_matched_ids:
                # region: str = doc.ents[0].text
                region = "France"
                preposition = "en"
                for token in doc:
                    if token.pos_ == "PROPN":
                        region = token.text
                    if token.pos_ == "ADP":
                        preposition = token.text
                self.__system_center.get_instruction(
                    SystemInstruction(Task.TELL_TIME_SPECIFIC, (preposition, region, Global.fr_en_translator.translate(
                        region)), None))
            elif TIME_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.TELL_TIME, None, None))
            if DATE_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.TELL_DATE, None, None))
            if SWITCH_WINDOW_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.SWITCH_WINDOW, None, None))
            if SWITCH_TAB_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.SWITCH_TAB, None, None))
            if PRINT_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.PRINT, None, None))
            if SAVE_AS_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.SAVE_AS, None, None))
            if OPEN_BROWSER_PATTERN in patterns_matched_ids:
                self.__net_center.get_instruction(NetInstruction(Task.OPEN, None, None))

        else:
            print("no")
            self.__attempts_count += 1
            if self.__attempts_count == self.__MAX_ATTEMPTS_COUNT:
                self.__stand_by = True
                playsound("Store/Media/water_drop.mp3")
                print("stand by ...")

    def __trim_name(self, text: str):
        return text[len(self.__NAME)+1:]

    def config_matcher(self):
        matcher = Matcher(self.__nlp.vocab)
        for pattern in patterns[self.__language].items():
            matcher.add(pattern[0], [pattern[1]])
        return matcher
