# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\prjadder.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_prjadder_dialog(object):
    def setupUi(self, prjadder_dialog):
        prjadder_dialog.setObjectName("prjadder_dialog")
        prjadder_dialog.resize(987, 631)
        self.verticalLayout = QtGui.QVBoxLayout(prjadder_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.prj_tablev = QtGui.QTableView(prjadder_dialog)
        self.prj_tablev.setObjectName("prj_tablev")
        self.verticalLayout.addWidget(self.prj_tablev)
        self.add_pb = QtGui.QPushButton(prjadder_dialog)
        self.add_pb.setObjectName("add_pb")
        self.verticalLayout.addWidget(self.add_pb)

        self.retranslateUi(prjadder_dialog)
        QtCore.QMetaObject.connectSlotsByName(prjadder_dialog)

    def retranslateUi(self, prjadder_dialog):
        prjadder_dialog.setWindowTitle(QtGui.QApplication.translate("prjadder_dialog", "Add Projects", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("prjadder_dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

