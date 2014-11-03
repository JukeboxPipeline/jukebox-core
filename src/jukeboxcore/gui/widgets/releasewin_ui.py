# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\releasewin.ui'
#
# Created: Mon Nov 03 16:40:12 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_release_mwin(object):
    def setupUi(self, release_mwin):
        release_mwin.setObjectName("release_mwin")
        release_mwin.resize(1009, 764)
        self.central_widget = QtGui.QWidget(release_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.release_hbox = QtGui.QHBoxLayout()
        self.release_hbox.setObjectName("release_hbox")
        self.release_pb = QtGui.QPushButton(self.central_widget)
        self.release_pb.setMinimumSize(QtCore.QSize(200, 30))
        self.release_pb.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.release_pb.setFont(font)
        self.release_pb.setObjectName("release_pb")
        self.release_hbox.addWidget(self.release_pb)
        self.central_vbox.addLayout(self.release_hbox)
        release_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(release_mwin)
        self.statusbar.setObjectName("statusbar")
        release_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(release_mwin)
        QtCore.QMetaObject.connectSlotsByName(release_mwin)

    def retranslateUi(self, release_mwin):
        release_mwin.setWindowTitle(QtGui.QApplication.translate("release_mwin", "Release", None, QtGui.QApplication.UnicodeUTF8))
        self.release_pb.setText(QtGui.QApplication.translate("release_mwin", "Release", None, QtGui.QApplication.UnicodeUTF8))

