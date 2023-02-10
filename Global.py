import xml.etree.ElementTree as ET
from translate import Translator

UI_TITLE = "SU - Interface"

# Runtime variables defined at start in main.py
user: str = "axel"
tree: ET = ET
root: ET.Element = ET.Element("")
lang: str = ""
fr_en_translator = Translator(from_lang="fr", to_lang="en")
en_fr_translator = Translator(from_lang="en", to_lang="fr")

terminal_prompt = ">  "
terminal_prompt_color = (252,158,88)
terminal_io_color = (170, 170, 170)
terminal_error_color = (168, 74, 50)
terminal_warning_color = (168, 158, 50)
terminal_error_indicator = "\\error"
terminal_warning_indicator = "\\warn"
terminal_separator = " "
terminal_system_key_word = "sys"
terminal_media_keyword = "media"
terminal_net__keyword = "net"
terminal_memory_keyword = "mem"

media_center = None
system_center = None
net_center = None
memory_center = None

def get_language():
    file = open("Store/Language", 'r')
    language = file.readline()
    file.close()
    return language


def get_username():
    global user
    file = open("Store/UserName", 'r')
    user_name = file.readline()
    file.close()
    user = user_name
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
