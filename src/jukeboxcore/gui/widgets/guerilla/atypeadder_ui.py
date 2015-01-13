# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\atypeadder.ui'
#
# Created: Tue Jan 13 14:50:07 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_atypeadder_mwin(object):
    def setupUi(self, atypeadder_mwin):
        atypeadder_mwin.setObjectName("atypeadder_mwin")
        atypeadder_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(atypeadder_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.atype_tablev = QtGui.QTableView(self.central_widget)
        self.atype_tablev.setObjectName("atype_tablev")
        self.central_vbox.addWidget(self.atype_tablev)
        self.add_pb = QtGui.QPushButton(self.central_widget)
        self.add_pb.setObjectName("add_pb")
        self.central_vbox.addWidget(self.add_pb)
        atypeadder_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(atypeadder_mwin)
        self.statusbar.setObjectName("statusbar")
        atypeadder_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(atypeadder_mwin)
        QtCore.QMetaObject.connectSlotsByName(atypeadder_mwin)

    def retranslateUi(self, atypeadder_mwin):
        atypeadder_mwin.setWindowTitle(QtGui.QApplication.translate("atypeadder_mwin", "Add Assettypes", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("atypeadder_mwin", "Add", None, QtGui.QApplication.UnicodeUTF8))

