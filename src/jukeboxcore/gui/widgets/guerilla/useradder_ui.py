# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\useradder.ui'
#
# Created: Tue Jan 13 18:54:58 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_useradder_dialog(object):
    def setupUi(self, useradder_dialog):
        useradder_dialog.setObjectName("useradder_dialog")
        useradder_dialog.resize(795, 601)
        self.verticalLayout = QtGui.QVBoxLayout(useradder_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.user_tablev = QtGui.QTableView(useradder_dialog)
        self.user_tablev.setObjectName("user_tablev")
        self.verticalLayout.addWidget(self.user_tablev)
        self.add_pb = QtGui.QPushButton(useradder_dialog)
        self.add_pb.setObjectName("add_pb")
        self.verticalLayout.addWidget(self.add_pb)

        self.retranslateUi(useradder_dialog)
        QtCore.QMetaObject.connectSlotsByName(useradder_dialog)

    def retranslateUi(self, useradder_dialog):
        useradder_dialog.setWindowTitle(QtGui.QApplication.translate("useradder_dialog", "Add Users", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("useradder_dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

