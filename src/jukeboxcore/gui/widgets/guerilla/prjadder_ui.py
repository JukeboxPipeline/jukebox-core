# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\prjadder.ui'
#
# Created: Tue Jan 13 14:50:07 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_prjadder_mwin(object):
    def setupUi(self, prjadder_mwin):
        prjadder_mwin.setObjectName("prjadder_mwin")
        prjadder_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(prjadder_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.prj_tablev = QtGui.QTableView(self.central_widget)
        self.prj_tablev.setObjectName("prj_tablev")
        self.central_vbox.addWidget(self.prj_tablev)
        self.add_pb = QtGui.QPushButton(self.central_widget)
        self.add_pb.setObjectName("add_pb")
        self.central_vbox.addWidget(self.add_pb)
        prjadder_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(prjadder_mwin)
        self.statusbar.setObjectName("statusbar")
        prjadder_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(prjadder_mwin)
        QtCore.QMetaObject.connectSlotsByName(prjadder_mwin)

    def retranslateUi(self, prjadder_mwin):
        prjadder_mwin.setWindowTitle(QtGui.QApplication.translate("prjadder_mwin", "Add Project", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("prjadder_mwin", "Add", None, QtGui.QApplication.UnicodeUTF8))

