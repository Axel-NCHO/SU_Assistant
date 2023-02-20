from PyQt5 import QtWidgets
from browser import MainWindow
import sys


def start_browser():
    webapp = QtWidgets.QApplication(sys.argv)
    webapp.setApplicationName("Browser@alice")
    if len(sys.argv) <= 1:
        _ = MainWindow()
    else:
        _ = MainWindow(sys.argv[1])
    webapp.exec()
    sys.exit(0)


if __name__ == "__main__":
    start_browser()
