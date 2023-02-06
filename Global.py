import xml.etree.ElementTree as ET
from translate import Translator

UI_TITLE = "SU - Interface"

# Runtime variables defined at start in main.py
tree: ET = ET
root: ET.Element = ET.Element("")
lang: str = ""
fr_en_translator = Translator(from_lang="fr", to_lang="en")
en_fr_translator = Translator(from_lang="en", to_lang="fr")


def get_language():
    file = open("Store/Language", 'r')
    language = file.readline()
    file.close()
    return language


def get_username():
    file = open("Store/UserName", 'r')
    user_name = file.readline()
    file.close()
    return user_name


def reformat_lang(language: str) -> str:
    if language == "fr":
        return "fr-FR"
    if language == "en":
        return "en-US"
    if language == "en-US":
        return "en"
    if language == "fr-FR":
        return "fr"
