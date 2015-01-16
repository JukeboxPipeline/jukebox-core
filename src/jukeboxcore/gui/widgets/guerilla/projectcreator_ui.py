# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\projectcreator.ui'
#
# Created: Tue Jan 13 18:54:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_projectcreator_dialog(object):
    def setupUi(self, projectcreator_dialog):
        projectcreator_dialog.setObjectName("projectcreator_dialog")
        projectcreator_dialog.resize(803, 145)
        self.gridLayout = QtGui.QGridLayout(projectcreator_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.name_lb = QtGui.QLabel(projectcreator_dialog)
        self.name_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_lb.setObjectName("name_lb")
        self.gridLayout.addWidget(self.name_lb, 0, 0, 1, 1)
        self.name_le = QtGui.QLineEdit(projectcreator_dialog)
        self.name_le.setObjectName("name_le")
        self.gridLayout.addWidget(self.name_le, 0, 1, 1, 1)
        self.short_lb = QtGui.QLabel(projectcreator_dialog)
        self.short_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.short_lb.setObjectName("short_lb")
        self.gridLayout.addWidget(self.short_lb, 1, 0, 1, 1)
        self.short_le = QtGui.QLineEdit(projectcreator_dialog)
        self.short_le.setObjectName("short_le")
        self.gridLayout.addWidget(self.short_le, 1, 1, 1, 1)
        self.path_lb = QtGui.QLabel(projectcreator_dialog)
        self.path_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.path_lb.setObjectName("path_lb")
        self.gridLayout.addWidget(self.path_lb, 2, 0, 1, 1)
        self.path_le = QtGui.QLineEdit(projectcreator_dialog)
        self.path_le.setObjectName("path_le")
        self.gridLayout.addWidget(self.path_le, 2, 1, 1, 1)
        self.semester_lb = QtGui.QLabel(projectcreator_dialog)
        self.semester_lb.setObjectName("semester_lb")
        self.gridLayout.addWidget(self.semester_lb, 3, 0, 1, 1)
        self.semester_le = QtGui.QLineEdit(projectcreator_dialog)
        self.semester_le.setObjectName("semester_le")
        self.gridLayout.addWidget(self.semester_le, 3, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(projectcreator_dialog)
        self.create_pb.setObjectName("create_pb")
        self.gridLayout.addWidget(self.create_pb, 4, 1, 1, 1)

        self.retranslateUi(projectcreator_dialog)
        QtCore.QMetaObject.connectSlotsByName(projectcreator_dialog)

    def retranslateUi(self, projectcreator_dialog):
        projectcreator_dialog.setWindowTitle(QtGui.QApplication.translate("projectcreator_dialog", "Create Project", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lb.setText(QtGui.QApplication.translate("projectcreator_dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.short_lb.setText(QtGui.QApplication.translate("projectcreator_dialog", "Short", None, QtGui.QApplication.UnicodeUTF8))
        self.path_lb.setText(QtGui.QApplication.translate("projectcreator_dialog", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.semester_lb.setText(QtGui.QApplication.translate("projectcreator_dialog", "Semester", None, QtGui.QApplication.UnicodeUTF8))
        self.semester_le.setPlaceholderText(QtGui.QApplication.translate("projectcreator_dialog", "e.g. SS15 or WS15/16", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("projectcreator_dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))

