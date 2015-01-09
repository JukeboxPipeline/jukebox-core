# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\reftrackadder.ui'
#
# Created: Fri Jan 09 14:02:42 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_reftrackadder_mwin(object):
    def setupUi(self, reftrackadder_mwin):
        reftrackadder_mwin.setObjectName("reftrackadder_mwin")
        reftrackadder_mwin.resize(1204, 581)
        self.central_widget = QtGui.QWidget(reftrackadder_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_vbox.setObjectName("central_vbox")
        self.browser_tabw = QtGui.QTabWidget(self.central_widget)
        self.browser_tabw.setObjectName("browser_tabw")
        self.shot_widget = QtGui.QWidget()
        self.shot_widget.setObjectName("shot_widget")
        self.shot_vbox = QtGui.QVBoxLayout(self.shot_widget)
        self.shot_vbox.setObjectName("shot_vbox")
        self.browser_tabw.addTab(self.shot_widget, "")
        self.asset_widget = QtGui.QWidget()
        self.asset_widget.setObjectName("asset_widget")
        self.asset_vbox = QtGui.QVBoxLayout(self.asset_widget)
        self.asset_vbox.setObjectName("asset_vbox")
        self.browser_tabw.addTab(self.asset_widget, "")
        self.central_vbox.addWidget(self.browser_tabw)
        self.button_vbox = QtGui.QHBoxLayout()
        self.button_vbox.setObjectName("button_vbox")
        self.add_tb = QtGui.QToolButton(self.central_widget)
        self.add_tb.setMinimumSize(QtCore.QSize(50, 40))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.add_tb.setFont(font)
        self.add_tb.setIconSize(QtCore.QSize(20, 20))
        self.add_tb.setAutoRaise(False)
        self.add_tb.setObjectName("add_tb")
        self.button_vbox.addWidget(self.add_tb)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.button_vbox.addItem(spacerItem)
        self.central_vbox.addLayout(self.button_vbox)
        reftrackadder_mwin.setCentralWidget(self.central_widget)

        self.retranslateUi(reftrackadder_mwin)
        self.browser_tabw.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(reftrackadder_mwin)

    def retranslateUi(self, reftrackadder_mwin):
        reftrackadder_mwin.setWindowTitle(QtGui.QApplication.translate("reftrackadder_mwin", "Add Reftracks", None, QtGui.QApplication.UnicodeUTF8))
        self.browser_tabw.setTabText(self.browser_tabw.indexOf(self.shot_widget), QtGui.QApplication.translate("reftrackadder_mwin", "Shots", None, QtGui.QApplication.UnicodeUTF8))
        self.browser_tabw.setTabText(self.browser_tabw.indexOf(self.asset_widget), QtGui.QApplication.translate("reftrackadder_mwin", "Assets", None, QtGui.QApplication.UnicodeUTF8))
        self.add_tb.setToolTip(QtGui.QApplication.translate("reftrackadder_mwin", "Add a new reftrack of the selected element and type to your tool.", None, QtGui.QApplication.UnicodeUTF8))
        self.add_tb.setText(QtGui.QApplication.translate("reftrackadder_mwin", "Add", None, QtGui.QApplication.UnicodeUTF8))

