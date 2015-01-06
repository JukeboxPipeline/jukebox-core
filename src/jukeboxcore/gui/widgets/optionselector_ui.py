# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\optionselector.ui'
#
# Created: Tue Jan 06 10:01:02 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_OptionSelector(object):
    def setupUi(self, OptionSelector):
        OptionSelector.setObjectName("OptionSelector")
        OptionSelector.resize(400, 300)
        self.main_vbox = QtGui.QVBoxLayout(OptionSelector)
        self.main_vbox.setObjectName("main_vbox")
        self.browser_vbox = QtGui.QVBoxLayout()
        self.browser_vbox.setObjectName("browser_vbox")
        self.main_vbox.addLayout(self.browser_vbox)
        self.buttons_hbox = QtGui.QHBoxLayout()
        self.buttons_hbox.setObjectName("buttons_hbox")
        self.select_pb = QtGui.QPushButton(OptionSelector)
        self.select_pb.setObjectName("select_pb")
        self.buttons_hbox.addWidget(self.select_pb)
        self.cancel_pb = QtGui.QPushButton(OptionSelector)
        self.cancel_pb.setObjectName("cancel_pb")
        self.buttons_hbox.addWidget(self.cancel_pb)
        self.main_vbox.addLayout(self.buttons_hbox)

        self.retranslateUi(OptionSelector)
        QtCore.QObject.connect(self.cancel_pb, QtCore.SIGNAL("clicked()"), OptionSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionSelector)

    def retranslateUi(self, OptionSelector):
        OptionSelector.setWindowTitle(QtGui.QApplication.translate("OptionSelector", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.select_pb.setText(QtGui.QApplication.translate("OptionSelector", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_pb.setText(QtGui.QApplication.translate("OptionSelector", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

