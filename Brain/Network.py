import spacy
from spacy.matcher import Matcher

import Global
import HumanMachineInterface.OutputInterface
from Brain.ProcessingCenters import *
from Brain.Instructions import MediaInstruction
from Brain.Patterns import *


class Network:

    def __init__(self, language: str, media_center: MediaCenter, system_center: SystemCenter):
        self.__language = language
        self.__nlp = self.get_vocab()
        self.__matcher = self.config_matcher()
        '''
        self.__system_matcher = self.config_system_matcher()
        self.__converse_matcher = self.config_converse_matcher()
        self.__net_matcher = self.config_net_matcher()
        '''
        self.__media_center = media_center
        self.__system_center = system_center
        self.__attempts_count: int = 0
        self.__MAX_ATTEMPTS_COUNT: int = 5
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
            if TIME_PATTERN in patterns_matched_ids:
                self.__system_center.get_instruction(SystemInstruction(Task.TELL_TIME, None, None))

        else:
            print("no")
            self.__attempts_count += 1
            if self.__attempts_count == self.__MAX_ATTEMPTS_COUNT:
                self.__stand_by = True
                print("stand by ...")

    def __trim_name(self, text: str):
        return text[len(self.__NAME)+1:]

    def config_matcher(self):
        matcher = Matcher(self.__nlp.vocab)
        for pattern in patterns[self.__language].items():
            matcher.add(pattern[0], [pattern[1]])

        # photo_pattern = patterns[self.__language][PHOTO_PATTERN]
        '''
        [[{"LEMMA": "lancer", "POS": "VERB"}], [{"LEMMA": "prendre"}],
                          [{"LEMMA": "capturer", "POS": "VERB"}],
                          [{"LEMMA": "capturer", "POS": "NOUN"}], [{"LEMMA": "enregistrer"}], [{"LEMMA": "lire"}]]
                          '''
        # matcher.add("PHOTO_PATTERN", [photo_pattern])
        return matcher

    '''
    def config_system_matcher(self):
        matcher = Matcher(self.__nlp.vocab)
        patterns_system = [[{"LEMMA": "ouvrir", "POS": "VERB"}], [{"LEMMA": "exécuter", "POS": "VERB"}],
                          [{"LOWER": "bilan", "POS": "NOUN"}], [{"LOWER": "check-up"}]]
        matcher.add("SYSTEM_PATTERN", patterns_system)
        return matcher

    def config_converse_matcher(self):
        matcher = Matcher(self.__nlp.vocab)
        patterns_converse = [[{"LEMMA": "lancer", "POS": "VERB"}], [{"LEMMA": "prendre"}],
                          [{"LEMMA": "capturer", "POS": "VERB"}],
                          [{"LEMMA": "capturer", "POS": "NOUN"}], [{"LEMMA": "enregistrer"}], [{"LEMMA": "lire"}]]
        matcher.add("MEDIA_PATTERN", patterns_converse)
        return matcher

    def config_net_matcher(self):
        matcher = Matcher(self.__nlp.vocab)
        patterns_media = [[{"LEMMA": "lancer", "POS": "VERB"}], [{"LEMMA": "prendre"}],
                          [{"LEMMA": "capturer", "POS": "VERB"}],
                          [{"LEMMA": "capturer", "POS": "NOUN"}], [{"LEMMA": "enregistrer"}], [{"LEMMA": "lire"}]]
        matcher.add("MEDIA_PATTERN", patterns_media)
        return matcher
    '''
