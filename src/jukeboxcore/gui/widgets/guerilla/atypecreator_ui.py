# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\atypecreator.ui'
#
# Created: Tue Jan 13 18:00:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_atypecreator_mwin(object):
    def setupUi(self, atypecreator_mwin):
        atypecreator_mwin.setObjectName("atypecreator_mwin")
        atypecreator_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(atypecreator_mwin)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout = QtGui.QGridLayout(self.central_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.name_lb = QtGui.QLabel(self.central_widget)
        self.name_lb.setObjectName("name_lb")
        self.gridLayout.addWidget(self.name_lb, 0, 0, 1, 1)
        self.desc_lb = QtGui.QLabel(self.central_widget)
        self.desc_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.desc_lb.setObjectName("desc_lb")
        self.gridLayout.addWidget(self.desc_lb, 1, 0, 1, 1)
        self.desc_pte = QtGui.QPlainTextEdit(self.central_widget)
        self.desc_pte.setObjectName("desc_pte")
        self.gridLayout.addWidget(self.desc_pte, 1, 1, 1, 1)
        self.name_le = QtGui.QLineEdit(self.central_widget)
        self.name_le.setObjectName("name_le")
        self.gridLayout.addWidget(self.name_le, 0, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(self.central_widget)
        self.create_pb.setObjectName("create_pb")
        self.gridLayout.addWidget(self.create_pb, 2, 1, 1, 1)
        atypecreator_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(atypecreator_mwin)
        self.statusbar.setObjectName("statusbar")
        atypecreator_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(atypecreator_mwin)
        QtCore.QObject.connect(self.create_pb, QtCore.SIGNAL("clicked()"), atypecreator_mwin.close)
        QtCore.QMetaObject.connectSlotsByName(atypecreator_mwin)

    def retranslateUi(self, atypecreator_mwin):
        atypecreator_mwin.setWindowTitle(QtGui.QApplication.translate("atypecreator_mwin", "Create Assettype", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lb.setText(QtGui.QApplication.translate("atypecreator_mwin", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.desc_lb.setText(QtGui.QApplication.translate("atypecreator_mwin", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("atypecreator_mwin", "Create", None, QtGui.QApplication.UnicodeUTF8))

