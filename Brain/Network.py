import spacy
from spacy.matcher import Matcher
from Brain.MediaCenter import *
from Brain.Instructions import MediaInstruction
from Brain.Patterns import *


class Network:

    def __init__(self, language: str, media_center: MediaCenter):
        self.__language = language
        self.__nlp = self.get_vocab()
        self.__matcher = self.config_matcher()
        '''
        self.__system_matcher = self.config_system_matcher()
        self.__converse_matcher = self.config_converse_matcher()
        self.__net_matcher = self.config_net_matcher()
        '''
        self.__media_center = media_center

    def get_vocab(self):
        if self.__language == "fr":
            return spacy.load("fr_core_news_sm", disable=["parser"])
        if self.__language == "en":
            return spacy.load("en_core_web_sm", disable=["parser"])
        return spacy.blank("fr")

    def parse_instruction(self, instruction):

        text = instruction
        doc = self.__nlp(text)

        # Find instruction group
        matches = self.__matcher(doc)

        if len(matches) != 0:
            patterns_matched_ids = [doc.vocab.strings[match[0]] for match in matches]
            if PHOTO_PATTERN in patterns_matched_ids:
                self.__media_center.get_instruction(MediaInstruction(Task.TAKE_IMAGE, None, None))
            if VIDEO_PATTERN in patterns_matched_ids:
                self.__media_center.get_instruction(MediaInstruction(Task.RECORD_VIDEO, None, None))

        else:
            print("no")

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
