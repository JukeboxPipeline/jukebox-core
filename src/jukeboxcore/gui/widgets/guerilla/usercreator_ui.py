# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\usercreator.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_usercreator_dialog(object):
    def setupUi(self, usercreator_dialog):
        usercreator_dialog.setObjectName("usercreator_dialog")
        usercreator_dialog.resize(661, 145)
        self.gridLayout = QtGui.QGridLayout(usercreator_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.username_lb = QtGui.QLabel(usercreator_dialog)
        self.username_lb.setObjectName("username_lb")
        self.gridLayout.addWidget(self.username_lb, 0, 0, 1, 1)
        self.username_le = QtGui.QLineEdit(usercreator_dialog)
        self.username_le.setObjectName("username_le")
        self.gridLayout.addWidget(self.username_le, 0, 1, 1, 1)
        self.first_lb = QtGui.QLabel(usercreator_dialog)
        self.first_lb.setObjectName("first_lb")
        self.gridLayout.addWidget(self.first_lb, 1, 0, 1, 1)
        self.first_le = QtGui.QLineEdit(usercreator_dialog)
        self.first_le.setObjectName("first_le")
        self.gridLayout.addWidget(self.first_le, 1, 1, 1, 1)
        self.last_lb = QtGui.QLabel(usercreator_dialog)
        self.last_lb.setObjectName("last_lb")
        self.gridLayout.addWidget(self.last_lb, 2, 0, 1, 1)
        self.last_le = QtGui.QLineEdit(usercreator_dialog)
        self.last_le.setObjectName("last_le")
        self.gridLayout.addWidget(self.last_le, 2, 1, 1, 1)
        self.email_lb = QtGui.QLabel(usercreator_dialog)
        self.email_lb.setObjectName("email_lb")
        self.gridLayout.addWidget(self.email_lb, 3, 0, 1, 1)
        self.email_le = QtGui.QLineEdit(usercreator_dialog)
        self.email_le.setObjectName("email_le")
        self.gridLayout.addWidget(self.email_le, 3, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(usercreator_dialog)
        self.create_pb.setObjectName("create_pb")
        self.gridLayout.addWidget(self.create_pb, 4, 1, 1, 1)

        self.retranslateUi(usercreator_dialog)
        QtCore.QMetaObject.connectSlotsByName(usercreator_dialog)

    def retranslateUi(self, usercreator_dialog):
        usercreator_dialog.setWindowTitle(QtGui.QApplication.translate("usercreator_dialog", "Create User", None, QtGui.QApplication.UnicodeUTF8))
        self.username_lb.setText(QtGui.QApplication.translate("usercreator_dialog", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.first_lb.setText(QtGui.QApplication.translate("usercreator_dialog", "First", None, QtGui.QApplication.UnicodeUTF8))
        self.last_lb.setText(QtGui.QApplication.translate("usercreator_dialog", "Last", None, QtGui.QApplication.UnicodeUTF8))
        self.email_lb.setText(QtGui.QApplication.translate("usercreator_dialog", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("usercreator_dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))

