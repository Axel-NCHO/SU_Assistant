# To add a new language, just add a new (key, value) item to the dictionary “patterns”
# where :
#       → key is an abbreviation of the language name
#       → value is a dictionary containing the pattern to be matched for each service provided
#          by SU.

# patterns names
PHOTO_PATTERN = "PHOTO_PATTERN"
VIDEO_PATTERN = "VIDEO_PATTERN"
SCREENSHOT_PATTERN = "SCREENSHOT_PATTERN"
TIME_PATTERN = "TELL_TIME_PATTERN"
TIME_SPECIFIC_PATTERN = "TIME_SPECIFIC_REGION_PATTERN"
DATE_PATTERN = "TELL_DATE_PATTERN"
SWITCH_WINDOW_PATTERN = "SWITCH_WINDOW__PATTERN"
SWITCH_TAB_PATTERN = "SWITCH_TAB_PATTERN"
PRINT_PATTERN = "PRINT_PATTERN"
SAVE_AS_PATTERN = "SAVE_AS_PATTERN"
OPEN_BROWSER_PATTERN = "open_browser_pattern"
PLAY_PAUSE_PATTERN = "PLAY_PAUSE_PATTERN"

patterns = {"fr":
                {PHOTO_PATTERN: [{"LEMMA": "prendre", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "photo"}],
                 VIDEO_PATTERN: [{"LEMMA": "faire", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "vidéo"}],
                 SCREENSHOT_PATTERN: [{"LEMMA": "faire", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                      {"LOWER": "capture"}, {"LOWER": "d'écran", "OP": "*"}],
                 TIME_PATTERN: [{"LEMMA": "quel"}, {"LOWER": "heure"}, {"POS": "AUX"},
                                {"POS": "PRON"}, {"POS": "PUNCT", "OP": "*"}],
                 TIME_SPECIFIC_PATTERN: [{"LEMMA": "quel"}, {"LOWER": "heure"},
                                         {"POS": "AUX"}, {"POS": "PRON"}, {"POS": "ADP"}, {"POS": "PROPN"},
                                         {"POS": "PUNCT", "OP": "*"}],
                 DATE_PATTERN: [{"LEMMA": "quel", "OP": "*"}, {"LOWER": "jour"}, {"POS": "AUX", "OP": "*"},
                                {"POS": "PRON"}],
                 SWITCH_WINDOW_PATTERN: [{"LOWER": "fenêtre", "POS": "NOUN"}, {"LEMMA": "précédent", "POS": "ADJ"}],
                 SWITCH_TAB_PATTERN: [{"LOWER": "anglais", "POS": "NOUN"}, {"LEMMA": "précédent", "POS": "ADJ"}],
                 PRINT_PATTERN: [{"LEMMA": "exporter", "POS": "VERB", "OP": "*"},
                                 {"LEMMA": "télécharger", "POS": "VERB", "OP": "*"},
                                 {"POS": "DET", "OP": "*"}, {"LOWER": "en"}, {"LOWER": "pdf"}],
                 SAVE_AS_PATTERN: [{"LEMMA": "télécharger", "POS": "VERB"}, {"POS": "DET", "OP": "*"},
                                   {"LOWER": "fichier", "POS": "NOUN"}],
                 OPEN_BROWSER_PATTERN: [{"LEMMA": "ouvrir"}, {"POS": "DET"}, {"LOWER": "navigateur"}],
                 PLAY_PAUSE_PATTERN: [{"LOWER": "pose"}]
                 },

            "en":
                {PHOTO_PATTERN: [{"LEMMA": "take", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "photo"}],
                 VIDEO_PATTERN: [{"LEMMA": "record", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "video"}],
                 SCREENSHOT_PATTERN: [{"LEMMA": "take", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                      {"LOWER": "screenshot"}],
                 TIME_PATTERN: [{"LEMMA": "what"}, {"LOWER": "time"}, {"POS": "AUX"}, {"POS": "PRON"},
                                {"POS": "PUNCT", "OP": "*"}],
                 TIME_SPECIFIC_PATTERN: [{"LEMMA": "what"}, {"LOWER": "time"}, {"POS": "AUX"}, {"POS": "PRON"},
                                         {"POS": "ADP"}, {"POS": "PROPN"}, {"POS": "PUNCT", "OP": "*"}],
                 DATE_PATTERN: [{"LEMMA": "what", "OP": "*"}, {"POS": "AUX", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                {"LEMMA": "date", "POS": "NOUN"}, {"POS": "PUNCT", "OP": "*"}],
                 SWITCH_WINDOW_PATTERN: [{"LOWER": "previous", "POS": "ADJ"}, {"LOWER": "window", "POS": "NOUN"}],
                 SWITCH_TAB_PATTERN: [{"LOWER": "previous", "POS": "ADJ"}, {"LOWER": "tab", "POS": "NOUN"}],
                 PRINT_PATTERN: [{"LEMMA": "export", "POS": "VERB", "OP": "*"},
                                 {"LEMMA": "download", "POS": "VERB", "OP": "*"},
                                 {"POS": "DET", "OP": "*"}, {"LOWER": "in"}, {"LOWER": "pdf"}],
                 SAVE_AS_PATTERN: [{"LEMMA": "download", "POS": "VERB"}, {"POS": "DET", "OP": "*"},
                                   {"LOWER": "file", "POS": "NOUN"}],
                 OPEN_BROWSER_PATTERN: [{"LEMMA": "open"}, {"POS": "DET"}, {"LOWER": "browser"}],
                 PLAY_PAUSE_PATTERN: [{"LOWER": "pause"}]
                 }
            }
"""
patterns :
Dictionary that contains the pattern to be matched for each service provided
by SU in every available language.
"""
