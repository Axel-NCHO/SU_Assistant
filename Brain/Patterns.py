# To add a new language, just add a new (key, value) item to the dictionary "patterns"
# where :
#       -> key is an abbreviation of the language name
#       -> value is a dictionary containing the pattern to be matched for each service provided
#          by SU

# patterns names
PHOTO_PATTERN = "PHOTO_PATTERN"
VIDEO_PATTERN = "VIDEO_PATTERN"

patterns = {"fr":
                {PHOTO_PATTERN: [{"LEMMA": "prendre", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "photo"}],
                 VIDEO_PATTERN: [{"LEMMA": "faire", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "vidéo"}]
                 },

            "en":
                {PHOTO_PATTERN: [{"LEMMA": "take", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "photo"}],
                 VIDEO_PATTERN: [{"LEMMA": "record", "POS": "VERB", "OP": "*"}, {"POS": "DET", "OP": "*"},
                                 {"LOWER": "video"}]
                 }
            }
"""
patterns :
Dictionary that contains the pattern to be matched for each service provided
by SU in every available language.
"""
