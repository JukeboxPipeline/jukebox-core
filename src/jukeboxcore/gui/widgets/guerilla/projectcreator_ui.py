# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\projectcreator.ui'
#
# Created: Tue Jan 13 18:00:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_projectcreator_mwin(object):
    def setupUi(self, projectcreator_mwin):
        projectcreator_mwin.setObjectName("projectcreator_mwin")
        projectcreator_mwin.resize(800, 167)
        self.central_widget = QtGui.QWidget(projectcreator_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_grid = QtGui.QGridLayout(self.central_widget)
        self.central_grid.setObjectName("central_grid")
        self.path_lb = QtGui.QLabel(self.central_widget)
        self.path_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.path_lb.setObjectName("path_lb")
        self.central_grid.addWidget(self.path_lb, 2, 0, 1, 1)
        self.path_le = QtGui.QLineEdit(self.central_widget)
        self.path_le.setObjectName("path_le")
        self.central_grid.addWidget(self.path_le, 2, 1, 1, 1)
        self.name_lb = QtGui.QLabel(self.central_widget)
        self.name_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_lb.setObjectName("name_lb")
        self.central_grid.addWidget(self.name_lb, 0, 0, 1, 1)
        self.short_le = QtGui.QLineEdit(self.central_widget)
        self.short_le.setObjectName("short_le")
        self.central_grid.addWidget(self.short_le, 1, 1, 1, 1)
        self.semester_lb = QtGui.QLabel(self.central_widget)
        self.semester_lb.setObjectName("semester_lb")
        self.central_grid.addWidget(self.semester_lb, 3, 0, 1, 1)
        self.short_lb = QtGui.QLabel(self.central_widget)
        self.short_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.short_lb.setObjectName("short_lb")
        self.central_grid.addWidget(self.short_lb, 1, 0, 1, 1)
        self.name_le = QtGui.QLineEdit(self.central_widget)
        self.name_le.setObjectName("name_le")
        self.central_grid.addWidget(self.name_le, 0, 1, 1, 1)
        self.semester_le = QtGui.QLineEdit(self.central_widget)
        self.semester_le.setObjectName("semester_le")
        self.central_grid.addWidget(self.semester_le, 3, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(self.central_widget)
        self.create_pb.setObjectName("create_pb")
        self.central_grid.addWidget(self.create_pb, 4, 1, 1, 1)
        projectcreator_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(projectcreator_mwin)
        self.statusbar.setObjectName("statusbar")
        projectcreator_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(projectcreator_mwin)
        QtCore.QObject.connect(self.create_pb, QtCore.SIGNAL("clicked()"), projectcreator_mwin.close)
        QtCore.QMetaObject.connectSlotsByName(projectcreator_mwin)

    def retranslateUi(self, projectcreator_mwin):
        projectcreator_mwin.setWindowTitle(QtGui.QApplication.translate("projectcreator_mwin", "Create Project", None, QtGui.QApplication.UnicodeUTF8))
        self.path_lb.setText(QtGui.QApplication.translate("projectcreator_mwin", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lb.setText(QtGui.QApplication.translate("projectcreator_mwin", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.semester_lb.setText(QtGui.QApplication.translate("projectcreator_mwin", "Semester", None, QtGui.QApplication.UnicodeUTF8))
        self.short_lb.setText(QtGui.QApplication.translate("projectcreator_mwin", "Short", None, QtGui.QApplication.UnicodeUTF8))
        self.semester_le.setPlaceholderText(QtGui.QApplication.translate("projectcreator_mwin", "e.g. SS15 or WS15/16", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("projectcreator_mwin", "Create", None, QtGui.QApplication.UnicodeUTF8))

