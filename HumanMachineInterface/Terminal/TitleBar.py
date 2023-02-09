from sys import exit

from PyQt5 import QtCore, QtGui, QtWidgets
from HumanMachineInterface.Terminal.titleBarUi import UiTitleBarWidget
from HumanMachineInterface.Terminal.MovableLabel import MovableLabel
from HumanMachineInterface.Terminal.Tab import Tab


class TitleBar(QtWidgets.QWidget, UiTitleBarWidget):

    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent=parent)
        self.setup_ui(self)
        self.parent = parent
        MovableLabel.main_window = self.parent

        self.titleBarPushButton_3.clicked.connect(self.parent.showMinimized)
        self.titleBarPushButton_2.clicked.connect(self.window_show_maximized)
        self.titleBarPushButton.clicked.connect(exit)

    def window_show_maximized(self):
        if self.titleBarPushButton_2.isChecked():
            self.parent.showMaximized()
            self.titleBarPushButton_2.setText(";")
        else:
            self.parent.showNormal()
            self.titleBarPushButton_2.setText("")

    def insert_tab(self, tab_widget):
        self.horizontalLayout.addWidget(tab_widget)
