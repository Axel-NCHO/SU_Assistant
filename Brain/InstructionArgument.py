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
    TELL_TIME = "Tell time"                     # TODO: Tell time
    TELL_Date = "Tell date"                     # TODO: Tell date
    WRITE = "Write"                             # TODO: Write text in a text box
    RENAME = "Rename"                           # TODO: Rename a file or a directory
    MAKE_REVIEW = "Make review"                 # TODO: Review of system infos

    # Converse
    GREET = "Greet"                             # TODO: Greet user
