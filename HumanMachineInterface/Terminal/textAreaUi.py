# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\textArea.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import Global


class UiTextAreaWidget(object):
    def setup_ui(self, textAreaUi):
        textAreaUi.setObjectName("textAreaUi")
        textAreaUi.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(textAreaUi)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(textAreaUi)
        self.widget.setMinimumSize(QtCore.QSize(600, 400))
        # self.widget.setMaximumSize(QtCore.QSize(600, 400))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_area = CustomQTextEdit(self.widget)  # QWidget.QTextEdit
        self.text_area.setMinimumSize(QtCore.QSize(600, 400))
        # self.text_area.setMaximumSize(QtCore.QSize(600, 400))
        self.text_area.setStyleSheet("QTextEdit{\n"
                                     "    background-color:rgb(35, 34, 39);\n"
                                     "    color:rgb(170, 170, 170);\n"
                                     "    border-bottom-left-radius:5px;\n"
                                     "    border-bottom-right-radius:5px;\n"
                                     "    padding:2px;\n"
                                     "}")
        self.text_area.setObjectName("text_area")
        self.text_area.setFont(QtGui.QFont("Calibri", 13))
        self.verticalLayout_2.addWidget(self.text_area)
        self.verticalLayout.addWidget(self.widget)
        self.text_area.setFocus()

        self.retranslate_ui(textAreaUi)
        QtCore.QMetaObject.connectSlotsByName(textAreaUi)

    def retranslate_ui(self, textAreaUi):
        _translate = QtCore.QCoreApplication.translate
        textAreaUi.setWindowTitle(_translate("textAreaUi", "Form"))


class CustomQTextEdit(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super(CustomQTextEdit, self).__init__(parent=parent)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key_Backspace:
            if not self.toPlainText().endswith(Global.terminal_prompt):
                super().keyPressEvent(e)
            else:
                self.setTextColor(QtGui.QColor(Global.terminal_io_color[0],
                                               Global.terminal_io_color[1],
                                               Global.terminal_io_color[2]))

        elif e.key() == QtCore.Qt.Key_Return:
            content = self.toPlainText()
            command = content[content.rfind(Global.terminal_prompt) + len(Global.terminal_prompt):]
            self.__execute_command(command)

        elif e.key() == QtCore.Qt.Key_Alt:
            self.clear()
            self.set_default_text()
        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.__move_cursor_to_end()

    def setText(self, text: str) -> None:
        super().append(text)
        self.__move_cursor_to_end()

    def set_default_text(self):
        self.setTextColor(QtGui.QColor(Global.terminal_prompt_color[0],
                                       Global.terminal_prompt_color[1],
                                       Global.terminal_prompt_color[2]))
        self.append(f"terminal@alice/{Global.user} {Global.terminal_prompt}")
        self.__set_default_io_color()

    def __set_default_io_color(self):
        self.setTextColor(QtGui.QColor(Global.terminal_io_color[0],
                                       Global.terminal_io_color[1],
                                       Global.terminal_io_color[2]))

    def __move_cursor_to_end(self):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.setTextCursor(cursor)
        self.__set_default_io_color()

    def __execute_command(self, command: str):
        self.setText(f"command: {command}\nstatus: [OK]")
        # self.setText("\n")
        self.set_default_text()