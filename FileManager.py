import cv2 as cv
from numpy import array
from os.path import exists
from Exceptions.IOException import NullReferenceException

# default names
DEFAULT_IMAGE_NAME = "image"
DEFAULT_VIDEO_NAME = "video"
IMAGE_FILE_EXTENSION = ".png"
VIDEO_FILE_EXTENSION = ".avi"

# indexes
imageIndex = 0
videoIndex = 0

# video config
video_codec = cv.VideoWriter_fourcc(*'XVID')
video_name = DEFAULT_VIDEO_NAME + str(videoIndex) + VIDEO_FILE_EXTENSION
FPS = 30.0
FRAME_SIZE = (640, 480)
out = None


def find_file_name(defaultName: str, index: int, extension: str) -> str:
    file_name = defaultName + str(index) + extension
    while exists(file_name):
        file_name = defaultName + str(index + 1) + extension
        index += 1
    return file_name


def save_image(image):
    global imageIndex
    try:
        file_name = find_file_name(DEFAULT_IMAGE_NAME, imageIndex, IMAGE_FILE_EXTENSION)
        cv.imwrite(file_name, image)
        imageIndex += 1
        return file_name

    except Exception as e:
        print(e)


def config_video_saver():
    global videoIndex
    global video_name
    global out

    video_name = find_file_name(DEFAULT_VIDEO_NAME, videoIndex, VIDEO_FILE_EXTENSION)

    out = cv.VideoWriter(video_name, video_codec, FPS, FRAME_SIZE)


def reset_video_saver():
    global out
    out.release()
    out = None


def save_video_frame_by_frame(frame):
    try:
        if out is not None:
            out.write(frame)
        else:
            raise NullReferenceException
    except Exception as e:
        print(e)


def convert_img_to_cv_format(image):
    return cv.cvtColor(array(image), cv.COLOR_RGB2BGR)