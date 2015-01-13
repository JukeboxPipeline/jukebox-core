# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\assetadder.ui'
#
# Created: Tue Jan 13 14:50:07 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_assetadder_mwin(object):
    def setupUi(self, assetadder_mwin):
        assetadder_mwin.setObjectName("assetadder_mwin")
        assetadder_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(assetadder_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.asset_treev = QtGui.QTreeView(self.central_widget)
        self.asset_treev.setObjectName("asset_treev")
        self.central_vbox.addWidget(self.asset_treev)
        self.add_pb = QtGui.QPushButton(self.central_widget)
        self.add_pb.setObjectName("add_pb")
        self.central_vbox.addWidget(self.add_pb)
        assetadder_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(assetadder_mwin)
        self.statusbar.setObjectName("statusbar")
        assetadder_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(assetadder_mwin)
        QtCore.QMetaObject.connectSlotsByName(assetadder_mwin)

    def retranslateUi(self, assetadder_mwin):
        assetadder_mwin.setWindowTitle(QtGui.QApplication.translate("assetadder_mwin", "Add Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("assetadder_mwin", "Add", None, QtGui.QApplication.UnicodeUTF8))

