# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\terminalUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UiTerminal(object):
    def setup_ui(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 440)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainWidget = QtWidgets.QWidget(Form)
        self.mainWidget.setStyleSheet("QWidget#mainWidget{\n"
                                      "    background-color:rgb(45, 45, 45);\n"
                                      "    border:1px solid rgb(0, 0, 0);\n"
                                      "}")
        self.mainWidget.setObjectName("mainWidget")
        self.verticalLayout.addWidget(self.mainWidget)

        self.retranslate_ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslate_ui(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
