# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\taskcreator.ui'
#
# Created: Tue Jan 13 14:50:07 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_taskcreator_mwin(object):
    def setupUi(self, taskcreator_mwin):
        taskcreator_mwin.setObjectName("taskcreator_mwin")
        taskcreator_mwin.resize(800, 113)
        self.central_widget = QtGui.QWidget(taskcreator_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_grid = QtGui.QGridLayout(self.central_widget)
        self.central_grid.setObjectName("central_grid")
        self.dep_cb = QtGui.QComboBox(self.central_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dep_cb.sizePolicy().hasHeightForWidth())
        self.dep_cb.setSizePolicy(sizePolicy)
        self.dep_cb.setObjectName("dep_cb")
        self.central_grid.addWidget(self.dep_cb, 0, 1, 1, 1)
        self.dep_lb = QtGui.QLabel(self.central_widget)
        self.dep_lb.setObjectName("dep_lb")
        self.central_grid.addWidget(self.dep_lb, 0, 0, 1, 1)
        self.create_pb = QtGui.QPushButton(self.central_widget)
        self.create_pb.setObjectName("create_pb")
        self.central_grid.addWidget(self.create_pb, 2, 1, 1, 1)
        self.dep_lb_2 = QtGui.QLabel(self.central_widget)
        self.dep_lb_2.setObjectName("dep_lb_2")
        self.central_grid.addWidget(self.dep_lb_2, 1, 0, 1, 1)
        self.deadline_de = QtGui.QDateEdit(self.central_widget)
        self.deadline_de.setDate(QtCore.QDate(2015, 1, 1))
        self.deadline_de.setObjectName("deadline_de")
        self.central_grid.addWidget(self.deadline_de, 1, 1, 1, 1)
        taskcreator_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(taskcreator_mwin)
        self.statusbar.setObjectName("statusbar")
        taskcreator_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(taskcreator_mwin)
        QtCore.QMetaObject.connectSlotsByName(taskcreator_mwin)

    def retranslateUi(self, taskcreator_mwin):
        taskcreator_mwin.setWindowTitle(QtGui.QApplication.translate("taskcreator_mwin", "Create Task", None, QtGui.QApplication.UnicodeUTF8))
        self.dep_lb.setText(QtGui.QApplication.translate("taskcreator_mwin", "Department", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("taskcreator_mwin", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.dep_lb_2.setText(QtGui.QApplication.translate("taskcreator_mwin", "Deadline", None, QtGui.QApplication.UnicodeUTF8))

