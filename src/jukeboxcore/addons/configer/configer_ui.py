# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\dz016\Documents\Jukebox\jukebox\addons\coreplugins\configer\configer.ui'
#
# Created: Tue May 06 11:12:11 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_configer_mwin(object):
    def setupUi(self, configer_mwin):
        configer_mwin.setObjectName("configer_mwin")
        configer_mwin.resize(854, 729)
        self.central_mwin = QtGui.QWidget(configer_mwin)
        self.central_mwin.setObjectName("central_mwin")
        self.verticalLayout = QtGui.QVBoxLayout(self.central_mwin)
        self.verticalLayout.setObjectName("verticalLayout")
        self.view_splitter = QtGui.QSplitter(self.central_mwin)
        self.view_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.view_splitter.setObjectName("view_splitter")
        self.files_lv = QtGui.QListView(self.view_splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.files_lv.sizePolicy().hasHeightForWidth())
        self.files_lv.setSizePolicy(sizePolicy)
        self.files_lv.setObjectName("files_lv")
        self.configobj_treev = QtGui.QTreeView(self.view_splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configobj_treev.sizePolicy().hasHeightForWidth())
        self.configobj_treev.setSizePolicy(sizePolicy)
        self.configobj_treev.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.configobj_treev.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.configobj_treev.setObjectName("configobj_treev")
        self.verticalLayout.addWidget(self.view_splitter)
        self.btns_hbox = QtGui.QHBoxLayout()
        self.btns_hbox.setObjectName("btns_hbox")
        self.save_pb = QtGui.QPushButton(self.central_mwin)
        self.save_pb.setObjectName("save_pb")
        self.btns_hbox.addWidget(self.save_pb)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.btns_hbox.addItem(spacerItem)
        self.reset_pb = QtGui.QPushButton(self.central_mwin)
        self.reset_pb.setObjectName("reset_pb")
        self.btns_hbox.addWidget(self.reset_pb)
        self.verticalLayout.addLayout(self.btns_hbox)
        configer_mwin.setCentralWidget(self.central_mwin)
        self.statusbar = QtGui.QStatusBar(configer_mwin)
        self.statusbar.setObjectName("statusbar")
        configer_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(configer_mwin)
        QtCore.QMetaObject.connectSlotsByName(configer_mwin)

    def retranslateUi(self, configer_mwin):
        configer_mwin.setWindowTitle(QtGui.QApplication.translate("configer_mwin", "Config Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.save_pb.setText(QtGui.QApplication.translate("configer_mwin", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_pb.setText(QtGui.QApplication.translate("configer_mwin", "Reset Value", None, QtGui.QApplication.UnicodeUTF8))

