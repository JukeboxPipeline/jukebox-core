# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\usercreator.ui'
#
# Created: Tue Jan 13 14:50:07 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_usercreator_mwin(object):
    def setupUi(self, usercreator_mwin):
        usercreator_mwin.setObjectName("usercreator_mwin")
        usercreator_mwin.resize(800, 165)
        self.central_widget = QtGui.QWidget(usercreator_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_grid = QtGui.QGridLayout(self.central_widget)
        self.central_grid.setObjectName("central_grid")
        self.email_lb = QtGui.QLabel(self.central_widget)
        self.email_lb.setObjectName("email_lb")
        self.central_grid.addWidget(self.email_lb, 3, 0, 1, 1)
        self.last_lb = QtGui.QLabel(self.central_widget)
        self.last_lb.setObjectName("last_lb")
        self.central_grid.addWidget(self.last_lb, 2, 0, 1, 1)
        self.create_pb = QtGui.QPushButton(self.central_widget)
        self.create_pb.setObjectName("create_pb")
        self.central_grid.addWidget(self.create_pb, 4, 1, 1, 1)
        self.username_le = QtGui.QLineEdit(self.central_widget)
        self.username_le.setObjectName("username_le")
        self.central_grid.addWidget(self.username_le, 0, 1, 1, 1)
        self.username_lb = QtGui.QLabel(self.central_widget)
        self.username_lb.setObjectName("username_lb")
        self.central_grid.addWidget(self.username_lb, 0, 0, 1, 1)
        self.first_lb = QtGui.QLabel(self.central_widget)
        self.first_lb.setObjectName("first_lb")
        self.central_grid.addWidget(self.first_lb, 1, 0, 1, 1)
        self.first_le = QtGui.QLineEdit(self.central_widget)
        self.first_le.setObjectName("first_le")
        self.central_grid.addWidget(self.first_le, 1, 1, 1, 1)
        self.last_le = QtGui.QLineEdit(self.central_widget)
        self.last_le.setObjectName("last_le")
        self.central_grid.addWidget(self.last_le, 2, 1, 1, 1)
        self.email_le = QtGui.QLineEdit(self.central_widget)
        self.email_le.setObjectName("email_le")
        self.central_grid.addWidget(self.email_le, 3, 1, 1, 1)
        usercreator_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(usercreator_mwin)
        self.statusbar.setObjectName("statusbar")
        usercreator_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(usercreator_mwin)
        QtCore.QMetaObject.connectSlotsByName(usercreator_mwin)

    def retranslateUi(self, usercreator_mwin):
        usercreator_mwin.setWindowTitle(QtGui.QApplication.translate("usercreator_mwin", "Create User", None, QtGui.QApplication.UnicodeUTF8))
        self.email_lb.setText(QtGui.QApplication.translate("usercreator_mwin", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.last_lb.setText(QtGui.QApplication.translate("usercreator_mwin", "Last", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("usercreator_mwin", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.username_lb.setText(QtGui.QApplication.translate("usercreator_mwin", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.first_lb.setText(QtGui.QApplication.translate("usercreator_mwin", "First", None, QtGui.QApplication.UnicodeUTF8))

