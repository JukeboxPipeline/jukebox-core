# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\shotcreator.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_shotcreator_dialog(object):
    def setupUi(self, shotcreator_dialog):
        shotcreator_dialog.setObjectName("shotcreator_dialog")
        shotcreator_dialog.resize(694, 398)
        self.gridLayout = QtGui.QGridLayout(shotcreator_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.name_lb = QtGui.QLabel(shotcreator_dialog)
        self.name_lb.setObjectName("name_lb")
        self.gridLayout.addWidget(self.name_lb, 0, 0, 1, 1)
        self.name_le = QtGui.QLineEdit(shotcreator_dialog)
        self.name_le.setObjectName("name_le")
        self.gridLayout.addWidget(self.name_le, 0, 1, 1, 1)
        self.desc_lb = QtGui.QLabel(shotcreator_dialog)
        self.desc_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.desc_lb.setObjectName("desc_lb")
        self.gridLayout.addWidget(self.desc_lb, 1, 0, 1, 1)
        self.desc_pte = QtGui.QPlainTextEdit(shotcreator_dialog)
        self.desc_pte.setObjectName("desc_pte")
        self.gridLayout.addWidget(self.desc_pte, 1, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(shotcreator_dialog)
        self.create_pb.setObjectName("create_pb")
        self.gridLayout.addWidget(self.create_pb, 2, 1, 1, 1)

        self.retranslateUi(shotcreator_dialog)
        QtCore.QMetaObject.connectSlotsByName(shotcreator_dialog)

    def retranslateUi(self, shotcreator_dialog):
        shotcreator_dialog.setWindowTitle(QtGui.QApplication.translate("shotcreator_dialog", "Create Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lb.setText(QtGui.QApplication.translate("shotcreator_dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.desc_lb.setText(QtGui.QApplication.translate("shotcreator_dialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("shotcreator_dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))

