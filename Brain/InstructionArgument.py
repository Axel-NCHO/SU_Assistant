from enum import Enum


class Group(Enum):
    MEDIA = "Media"
    SYSTEM = "System"
    MEMORY = "Memory"
    NET = "Net"
    CONVERSE = "Converse"


class Task(Enum):
    # Media
    TAKE_IMAGE = "Take image"
    TAKE_SCREENSHOT = "Take screenshot"
    RECORD_VIDEO = "Record video"
    PLAY_VIDEO = "Play video"

    # System
    OPEN = "Open"
    TELL_TIME = "Tell time"                     # Tell time                                 [OK]
    TELL_TIME_SPECIFIC = "Tell time specific"   # Tell time in a specific region            [OK]
    TELL_DATE = "Tell date"                     # Tell date                                 [OK]
    WRITE = "Write"                             # Write text in a text box
    RENAME = "Rename"                           # Rename a file or a directory
    MAKE_REVIEW = "Make review"                 # Review of system infos
    SAVE_AS = "save as"                         # Save a file by doing ctrl+s
    PRINT = "print"                             # Print a file to PDF by doing ctrl+p [OK]
    SWITCH_WINDOW = "switch window"             # Go to previous widows by doing alt+tab [OK]
    SWITCH_TAB = "switch tab"                   # Go to the previous tab by doing ctrl+tab [OK]
    PLAY_PAUSE = "play_pause"

    # Net
    LOOK_UP = "look up"

    # Converse
    GREET = "Greet"                             # Greet user
