# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\taskcreator.ui'
#
# Created: Tue Jan 13 18:54:58 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_taskcreator_dialog(object):
    def setupUi(self, taskcreator_dialog):
        taskcreator_dialog.setObjectName("taskcreator_dialog")
        taskcreator_dialog.resize(855, 93)
        self.gridLayout = QtGui.QGridLayout(taskcreator_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.dep_lb = QtGui.QLabel(taskcreator_dialog)
        self.dep_lb.setObjectName("dep_lb")
        self.gridLayout.addWidget(self.dep_lb, 0, 0, 1, 1)
        self.dep_cb = QtGui.QComboBox(taskcreator_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dep_cb.sizePolicy().hasHeightForWidth())
        self.dep_cb.setSizePolicy(sizePolicy)
        self.dep_cb.setObjectName("dep_cb")
        self.gridLayout.addWidget(self.dep_cb, 0, 1, 1, 1)
        self.deadline_lb = QtGui.QLabel(taskcreator_dialog)
        self.deadline_lb.setObjectName("deadline_lb")
        self.gridLayout.addWidget(self.deadline_lb, 1, 0, 1, 1)
        self.deadline_de = QtGui.QDateEdit(taskcreator_dialog)
        self.deadline_de.setDate(QtCore.QDate(2015, 1, 1))
        self.deadline_de.setObjectName("deadline_de")
        self.gridLayout.addWidget(self.deadline_de, 1, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(taskcreator_dialog)
        self.create_pb.setObjectName("create_pb")
        self.gridLayout.addWidget(self.create_pb, 2, 1, 1, 1)

        self.retranslateUi(taskcreator_dialog)
        QtCore.QMetaObject.connectSlotsByName(taskcreator_dialog)

    def retranslateUi(self, taskcreator_dialog):
        taskcreator_dialog.setWindowTitle(QtGui.QApplication.translate("taskcreator_dialog", "Create Task", None, QtGui.QApplication.UnicodeUTF8))
        self.dep_lb.setText(QtGui.QApplication.translate("taskcreator_dialog", "Department", None, QtGui.QApplication.UnicodeUTF8))
        self.deadline_lb.setText(QtGui.QApplication.translate("taskcreator_dialog", "Deadline", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("taskcreator_dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))

