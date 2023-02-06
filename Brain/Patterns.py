# To add a new language, just add a new (key, value) item to the dictionary "patterns"
# where :
#       -> key is an abbreviation of the language name
#       -> value is a dictionary containing the pattern to be matched for each service provided
#          by SU

# patterns names
PHOTO_PATTERN = "PHOTO_PATTERN"
VIDEO_PATTERN = "VIDEO_PATTERN"
SCREENSHOT_PATTERN = "SCREENSHOT_PATTERN"
TIME_PATTERN = "Tell time pattern"

patterns = {"fr":
                {PHOTO_PATTERN: [{"LEMMA": "prendre", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "photo"}],
                 VIDEO_PATTERN: [{"LEMMA": "faire", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "vidéo"}],
                 SCREENSHOT_PATTERN: [{"LEMMA": "faire", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                      {"LOWER": "capture"}, {"LOWER": "d'écran", "OP": "*"}],
                 TIME_PATTERN: [{"LEMMA": "quel", "OP": "*"}, {"LOWER": "heure", "OP": "*"}, {"POS": "AUX", "OP": "*"},
                                {"POS": "PRON", "OP": "*"}, {"POS": "PUNCT", "OP": "*"}, {"POS": "AUX", "OP": "*"},
                                {"LEMMA": "quel", "OP": "*"}, {"LOWER": "heure", "OP": "*"}]
                 },

            "en":
                {PHOTO_PATTERN: [{"LEMMA": "take", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "photo"}],
                 VIDEO_PATTERN: [{"LEMMA": "record", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "video"}],
                 SCREENSHOT_PATTERN: [{"LEMMA": "take", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                      {"LOWER": "screenshot"}],
                 TIME_PATTERN: [{"LEMMA": "what", "OP": "*"}, {"POS": "AUX", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                {"LOWER": "time", "OP": "*"}, {"POS": "AUX", "OP": "*"}, {"POS": "PRON", "OP": "*"},
                                {"POS": "PUNCT", "OP": "*"}]
                 }
            }
"""
patterns :
Dictionary that contains the pattern to be matched for each service provided
by SU in every available language.
"""
