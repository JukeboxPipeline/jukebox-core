# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\assetadder.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_assetadder_dialog(object):
    def setupUi(self, assetadder_dialog):
        assetadder_dialog.setObjectName("assetadder_dialog")
        assetadder_dialog.resize(798, 595)
        self.verticalLayout = QtGui.QVBoxLayout(assetadder_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.asset_treev = QtGui.QTreeView(assetadder_dialog)
        self.asset_treev.setObjectName("asset_treev")
        self.verticalLayout.addWidget(self.asset_treev)
        self.add_pb = QtGui.QPushButton(assetadder_dialog)
        self.add_pb.setObjectName("add_pb")
        self.verticalLayout.addWidget(self.add_pb)

        self.retranslateUi(assetadder_dialog)
        QtCore.QMetaObject.connectSlotsByName(assetadder_dialog)

    def retranslateUi(self, assetadder_dialog):
        assetadder_dialog.setWindowTitle(QtGui.QApplication.translate("assetadder_dialog", "Add Assets", None, QtGui.QApplication.UnicodeUTF8))
        self.add_pb.setText(QtGui.QApplication.translate("assetadder_dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

