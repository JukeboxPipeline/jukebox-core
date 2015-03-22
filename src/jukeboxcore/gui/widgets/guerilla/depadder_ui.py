# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\depadder.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_depadder_dialog(object):
    def setupUi(self, depadder_dialog):
        depadder_dialog.setObjectName("depadder_dialog")
        depadder_dialog.resize(798, 593)
        self.verticalLayout = QtGui.QVBoxLayout(depadder_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dep_tablev = QtGui.QTableView(depadder_dialog)
        self.dep_tablev.setObjectName("dep_tablev")
        self.verticalLayout.addWidget(self.dep_tablev)
        self.add_pb = QtGui.QPushButton(depadder_dialog)
        self.add_pb.setObjectName("add_pb")
        self.verticalLayout.addWidget(self.add_pb)

        self.retranslateUi(depadder_dialog)
        QtCore.QMetaObject.connectSlotsByName(depadder_dialog)

    def retranslateUi(self, depadder_dialog):
        depadder_dialog.setWindowTitle(QtGui.QApplication.translate("depadder_dialog", "Add Departments", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("depadder_dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

