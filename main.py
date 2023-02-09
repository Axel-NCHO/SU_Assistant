'''import threading

import Global
from Global import get_username, get_language, reformat_lang, ET

import HumanMachineInterface.OutputInterface
from Brain.Network import Network, MediaCenter, SystemCenter
from HumanMachineInterface.InputInterface import InputInterface
from HumanMachineInterface.OutputInterface import OutputInterface


def wait_for_request():
    while inp.is_listening():
        speech = inp.listen()
        print(speech)
        net.parse_instruction(speech)
    print("Stopped waiting for request.")


def great_user():
    HumanMachineInterface.OutputInterface.speech = root.find("greeting").find(reformat_lang(lang)).find(
        "start").text + " " + user_name + ", " + root.find("greeting").find(reformat_lang(lang)).find("end").text


tree = ET.parse("HumanMachineInterface/StandardSpeech.xml")
root = tree.getroot()
Global.tree = tree
Global.root = root

user_name = get_username()
print("Setting up language")
lang = get_language()  # must be reformatted if not called by In/Out interface
Global.lang = lang
print("Setting up input interface")
inp = InputInterface(lang)
print("Setting up output interface")
out = OutputInterface(lang)
print("Setting up processing centers")
media_center = MediaCenter(inp, out)
system_center = SystemCenter(inp)
print("Setting up central network")
net = Network(reformat_lang(lang), media_center, system_center)

# Great user
great_user()

wait_for_request_thread = threading.Thread(target=wait_for_request)
wait_for_request_thread.start()

out.show()

# Executed when out is closed
# As it's the main process, all the other threads will exit too as they are daemons.
# But the process that listens for new requests is not a daemon. It must be explicitly stopped.
# If all threads are not stopped, the program will continue to run in background even if the main
# process (the Tk window) has exited.
inp.stop_listening()
'''

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from HumanMachineInterface.Terminal.Terminal import Terminal


app = QtWidgets.QApplication(sys.argv)
ui = Terminal()
ui.show()
app.exec()
app.exit(0)
'''

import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TitleBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            Background-image:url('img/titlebar bg.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF00FF;
            font-size:11px;
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        self.minimize = QtWidgets.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('img/min.png'))
        self.maximize = QtWidgets.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('img/max.png'))
        close = QtWidgets.QToolButton(self)
        close.setIcon(QtGui.QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label = QtWidgets.QLabel(self)
        label.setText("Window Title")
        self.setWindowTitle("Window Title")
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1, 500)
        hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if (self.maxNormal):
            box.showNormal()
            self.maxNormal = False
            self.maximize.setIcon(QtGui.QIcon('img/max.png'))
            print('1')
        else:
            box.showMaximized()
            self.maxNormal = True
            print('2')
            self.maximize.setIcon(QtGui.QIcon('img/max2.png'))

    def close(self):
        box.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            box.moving = True
            box.offset = event.pos()

    def mouseMoveEvent(self, event):
        if box.moving: box.move(event.globalPos() - box.offset)


class Frame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.m_mouse_down = False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        css = """
        QFrame{
            Background:  #D700D7;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar = TitleBar(self)
        self.m_content = QtWidgets.QWidget(self)
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.m_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        vbox.addLayout(layout)
        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button() == Qt.LeftButton

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

    def mouseReleaseEvent(self, event):
        m_mouse_down = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    box = Frame()
    box.move(60, 60)
    l = QtWidgets.QVBoxLayout(box.contentWidget())
    l.setContentsMargins(0, 0, 0, 0)
    edit = QtWidgets.QLabel("""I would've did anything for you to show you how much I adored you
But it's over now, it's too late to save our loveJust promise me you'll think of me
Every time you look up in the sky and see a star 'cuz I'm  your star.""")
    l.addWidget(edit)
    box.show()
    app.exec_()
'''
