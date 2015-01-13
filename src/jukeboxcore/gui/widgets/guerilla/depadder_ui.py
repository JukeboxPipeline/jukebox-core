# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\depadder.ui'
#
# Created: Tue Jan 13 18:00:45 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_depadder_mwin(object):
    def setupUi(self, depadder_mwin):
        depadder_mwin.setObjectName("depadder_mwin")
        depadder_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(depadder_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.dep_tablev = QtGui.QTableView(self.central_widget)
        self.dep_tablev.setObjectName("dep_tablev")
        self.central_vbox.addWidget(self.dep_tablev)
        self.add_pb = QtGui.QPushButton(self.central_widget)
        self.add_pb.setObjectName("add_pb")
        self.central_vbox.addWidget(self.add_pb)
        depadder_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(depadder_mwin)
        self.statusbar.setObjectName("statusbar")
        depadder_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(depadder_mwin)
        QtCore.QMetaObject.connectSlotsByName(depadder_mwin)

    def retranslateUi(self, depadder_mwin):
        depadder_mwin.setWindowTitle(QtGui.QApplication.translate("depadder_mwin", "Add Department", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("depadder_mwin", "Add", None, QtGui.QApplication.UnicodeUTF8))

