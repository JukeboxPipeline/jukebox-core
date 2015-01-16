# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\atypeadder.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_atypeadder_dialog(object):
    def setupUi(self, atypeadder_dialog):
        atypeadder_dialog.setObjectName("atypeadder_dialog")
        atypeadder_dialog.resize(806, 598)
        self.verticalLayout = QtGui.QVBoxLayout(atypeadder_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.atype_tablev = QtGui.QTableView(atypeadder_dialog)
        self.atype_tablev.setObjectName("atype_tablev")
        self.verticalLayout.addWidget(self.atype_tablev)
        self.add_pb = QtGui.QPushButton(atypeadder_dialog)
        self.add_pb.setObjectName("add_pb")
        self.verticalLayout.addWidget(self.add_pb)

        self.retranslateUi(atypeadder_dialog)
        QtCore.QMetaObject.connectSlotsByName(atypeadder_dialog)

    def retranslateUi(self, atypeadder_dialog):
        atypeadder_dialog.setWindowTitle(QtGui.QApplication.translate("atypeadder_dialog", "Add Assettypes", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("atypeadder_dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

