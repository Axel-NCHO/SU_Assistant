from Brain.Threading import Threading
from time import sleep
from sys import argv
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie
from PIL import Image

from HumanMachineInterface.IOInterface import IOInterface
from HumanMachineInterface.IOMode import IOMode


def smooth_gif_resize(gif, frameWidth, frameHeight):
    gif = Image.open(gif)
    gifWidth0, gifHeight0 = gif.size

    widthRatio = frameWidth / gifWidth0
    heightRatio = frameHeight / gifHeight0

    if widthRatio >= heightRatio:
        gifWidth1 = gifWidth0 * heightRatio
        gifHeight1 = frameHeight
        return gifWidth1, gifHeight1

    gifWidth1 = frameWidth
    gifHeight1 = gifHeight0 * widthRatio
    return gifWidth1, gifHeight1


class OutputInterface(IOInterface):
    """
    Output Interface: \n
    Performs all machine-to-human operations: output actions
    """

    __instance = None

    @staticmethod
    def get_instance(lang=None):
        if not OutputInterface.__instance:
            if lang:
                OutputInterface.__instance = OutputInterface(lang)
            else:
                raise RuntimeError("Missing positional arguments: language")
        return OutputInterface.__instance

    def __init__(self, language: str = "fr-FR"):
        super(OutputInterface, self).__init__(IOMode.OUTPUT, language)
        self.__speech = ""
        self.__is_shown = False
        self.__app = QtWidgets.QApplication(argv)

        # create invisible widget
        self.__window = QtWidgets.QWidget()
        self.__window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.__window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.__window.setFixedSize(300, 300)

        self.__invisible_bg = QtWidgets.QWidget(self.__window)
        self.__invisible_bg.setStyleSheet('QWidget{background-color: white}')
        self.__invisible_bg.setObjectName('vc')
        self.__invisible_bg.setFixedSize(250, 250)
        self.__invisible_bg.setStyleSheet('QWidget#vc{background-color: transparent}')
        self.__layout = QtWidgets.QGridLayout()

        # add a close button
        '''
        self.__close_button = QtWidgets.QPushButton()
        self.__close_button.setText('close window')
        self.__close_button.clicked.connect(lambda: self.__app.exit(0))
        self.__layout.addWidget(self.__close_button)
        '''

        # add a close button as label
        self.__close_label = QtWidgets.QLabel()
        self.__close_label.setText("x")
        self.__close_label.setStyleSheet("background-color: transparent; color: white;")
        self.__close_label.setAlignment(QtCore.Qt.AlignRight)
        self.__close_label.mousePressEvent = self.__close
        self.__layout.addWidget(self.__close_label)

        # set qmovie as label
        self.__label = QtWidgets.QLabel()
        self.__movie = QMovie("Store/Media/ui.gif")
        self.__movie_size = QtCore.QSize(*smooth_gif_resize("Store/Media/ui.gif", 200, 200))
        self.__movie.setScaledSize(self.__movie_size)
        self.__label.setMovie(self.__movie)
        self.__label.setAlignment(QtCore.Qt.AlignCenter)
        self.__movie.start()
        self.__layout.addWidget(self.__label)
        self.__invisible_bg.setLayout(self.__layout)

        # Set position of the ui to the bottom right corner
        self.__ag = QtWidgets.QDesktopWidget().availableGeometry()
        self.__sg = QtWidgets.QDesktopWidget().screenGeometry()
        self.__widget = self.__window.geometry()
        self.__x = self.__ag.width() - self.__widget.width()
        self.__y = 2 * self.__ag.height() - self.__sg.height() - self.__widget.height()
        self.__window.move(self.__x, self.__y)

    def set_speech(self, speech: str):
        self.__speech = speech

    def is_shown(self):
        return self.__is_shown

    def speak(self, text: str):
        """
        Speak with installed voices \n
        :param text: Information to be spoken
        """
        super(OutputInterface, self).speak(text)

    def play_video(self, videoPath: str):
        """
        Play a video file \n
        :param videoPath: Path to the video file.
        """
        super(OutputInterface, self).play_video(videoPath)

    def show(self):
        # Watchman to take into account speech inquiries from other modules
        Threading.start_thread(target=self.wait_for_speech, daemon=True)
        self.__is_shown = True

        self.__window.show()
        self.__app.exec()

    def wait_for_speech(self):
        while True:
            if self.__speech != "":
                Threading.start_thread(target=self.speak, daemon=True, args=[self.__speech])
            if self.__speech != "":
                self.__speech = ""
            sleep(.5)

    def __close(self):
        self.__is_shown = False
        self.__app.exit(0)
