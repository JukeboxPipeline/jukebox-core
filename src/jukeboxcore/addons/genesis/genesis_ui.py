# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\addons\genesis\genesis.ui'
#
# Created: Mon Nov 03 16:39:53 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_genesis_mwin(object):
    def setupUi(self, genesis_mwin):
        genesis_mwin.setObjectName("genesis_mwin")
        genesis_mwin.resize(1009, 765)
        self.central_widget = QtGui.QWidget(genesis_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.shot_open_pb = QtGui.QPushButton(self.central_widget)
        self.shot_open_pb.setMinimumSize(QtCore.QSize(200, 32))
        self.shot_open_pb.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.shot_open_pb.setFont(font)
        self.shot_open_pb.setObjectName("shot_open_pb")
        self.central_vbox.addWidget(self.shot_open_pb)
        self.asset_open_pb = QtGui.QPushButton(self.central_widget)
        self.asset_open_pb.setMinimumSize(QtCore.QSize(200, 32))
        self.asset_open_pb.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.asset_open_pb.setFont(font)
        self.asset_open_pb.setObjectName("asset_open_pb")
        self.central_vbox.addWidget(self.asset_open_pb)
        self.shot_save_pb = QtGui.QPushButton(self.central_widget)
        self.shot_save_pb.setMinimumSize(QtCore.QSize(200, 32))
        self.shot_save_pb.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.shot_save_pb.setFont(font)
        self.shot_save_pb.setObjectName("shot_save_pb")
        self.central_vbox.addWidget(self.shot_save_pb)
        self.asset_save_pb = QtGui.QPushButton(self.central_widget)
        self.asset_save_pb.setMinimumSize(QtCore.QSize(200, 32))
        self.asset_save_pb.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.asset_save_pb.setFont(font)
        self.asset_save_pb.setObjectName("asset_save_pb")
        self.central_vbox.addWidget(self.asset_save_pb)
        self.asset_descriptor_le = QtGui.QLineEdit(self.central_widget)
        self.asset_descriptor_le.setObjectName("asset_descriptor_le")
        self.central_vbox.addWidget(self.asset_descriptor_le)
        self.asset_descriptor_lb = QtGui.QLabel(self.central_widget)
        self.asset_descriptor_lb.setObjectName("asset_descriptor_lb")
        self.central_vbox.addWidget(self.asset_descriptor_lb)
        self.shot_descriptor_le = QtGui.QLineEdit(self.central_widget)
        self.shot_descriptor_le.setObjectName("shot_descriptor_le")
        self.central_vbox.addWidget(self.shot_descriptor_le)
        self.shot_descriptor_lb = QtGui.QLabel(self.central_widget)
        self.shot_descriptor_lb.setObjectName("shot_descriptor_lb")
        self.central_vbox.addWidget(self.shot_descriptor_lb)
        genesis_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(genesis_mwin)
        self.statusbar.setObjectName("statusbar")
        genesis_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(genesis_mwin)
        QtCore.QMetaObject.connectSlotsByName(genesis_mwin)

    def retranslateUi(self, genesis_mwin):
        genesis_mwin.setWindowTitle(QtGui.QApplication.translate("genesis_mwin", "Genesis", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_open_pb.setText(QtGui.QApplication.translate("genesis_mwin", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_open_pb.setText(QtGui.QApplication.translate("genesis_mwin", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_save_pb.setText(QtGui.QApplication.translate("genesis_mwin", "Save/New", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_save_pb.setText(QtGui.QApplication.translate("genesis_mwin", "Save/New", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_descriptor_lb.setText(QtGui.QApplication.translate("genesis_mwin", "Descriptor:", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_descriptor_lb.setText(QtGui.QApplication.translate("genesis_mwin", "Descriptor:", None, QtGui.QApplication.UnicodeUTF8))

