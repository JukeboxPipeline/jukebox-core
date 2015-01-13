# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\useradder.ui'
#
# Created: Tue Jan 13 18:00:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_useradder_mwin(object):
    def setupUi(self, useradder_mwin):
        useradder_mwin.setObjectName("useradder_mwin")
        useradder_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(useradder_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.user_tablev = QtGui.QTableView(self.central_widget)
        self.user_tablev.setObjectName("user_tablev")
        self.central_vbox.addWidget(self.user_tablev)
        self.add_pb = QtGui.QPushButton(self.central_widget)
        self.add_pb.setObjectName("add_pb")
        self.central_vbox.addWidget(self.add_pb)
        useradder_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(useradder_mwin)
        self.statusbar.setObjectName("statusbar")
        useradder_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(useradder_mwin)
        QtCore.QMetaObject.connectSlotsByName(useradder_mwin)

    def retranslateUi(self, useradder_mwin):
        useradder_mwin.setWindowTitle(QtGui.QApplication.translate("useradder_mwin", "Add user", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("useradder_mwin", "Add", None, QtGui.QApplication.UnicodeUTF8))

