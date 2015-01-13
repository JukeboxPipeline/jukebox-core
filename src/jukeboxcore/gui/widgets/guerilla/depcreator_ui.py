# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\depcreator.ui'
#
# Created: Tue Jan 13 18:00:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_depcreator_mwin(object):
    def setupUi(self, depcreator_mwin):
        depcreator_mwin.setObjectName("depcreator_mwin")
        depcreator_mwin.resize(800, 600)
        self.central_widget = QtGui.QWidget(depcreator_mwin)
        self.central_widget.setObjectName("central_widget")
        self.central_grid = QtGui.QGridLayout(self.central_widget)
        self.central_grid.setObjectName("central_grid")
        self.des_pte = QtGui.QPlainTextEdit(self.central_widget)
        self.des_pte.setObjectName("des_pte")
        self.central_grid.addWidget(self.des_pte, 3, 1, 1, 1)
        self.short_le = QtGui.QLineEdit(self.central_widget)
        self.short_le.setObjectName("short_le")
        self.central_grid.addWidget(self.short_le, 1, 1, 1, 1)
        self.ordervalue_sb = QtGui.QSpinBox(self.central_widget)
        self.ordervalue_sb.setObjectName("ordervalue_sb")
        self.central_grid.addWidget(self.ordervalue_sb, 4, 1, 1, 1)
        self.odervalue_lb = QtGui.QLabel(self.central_widget)
        self.odervalue_lb.setObjectName("odervalue_lb")
        self.central_grid.addWidget(self.odervalue_lb, 4, 0, 1, 1)
        self.description_lb = QtGui.QLabel(self.central_widget)
        self.description_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.description_lb.setObjectName("description_lb")
        self.central_grid.addWidget(self.description_lb, 3, 0, 1, 1)
        self.name_le = QtGui.QLineEdit(self.central_widget)
        self.name_le.setObjectName("name_le")
        self.central_grid.addWidget(self.name_le, 0, 1, 1, 1)
        self.short_lb = QtGui.QLabel(self.central_widget)
        self.short_lb.setObjectName("short_lb")
        self.central_grid.addWidget(self.short_lb, 1, 0, 1, 1)
        self.name_lb = QtGui.QLabel(self.central_widget)
        self.name_lb.setObjectName("name_lb")
        self.central_grid.addWidget(self.name_lb, 0, 0, 1, 1)
        self.assetflag_hbox = QtGui.QHBoxLayout()
        self.assetflag_hbox.setObjectName("assetflag_hbox")
        self.shot_rb = QtGui.QRadioButton(self.central_widget)
        self.shot_rb.setChecked(True)
        self.shot_rb.setObjectName("shot_rb")
        self.assetflag_hbox.addWidget(self.shot_rb)
        self.asset_rb = QtGui.QRadioButton(self.central_widget)
        self.asset_rb.setObjectName("asset_rb")
        self.assetflag_hbox.addWidget(self.asset_rb)
        self.central_grid.addLayout(self.assetflag_hbox, 2, 1, 1, 1)
        self.create_pb = QtGui.QPushButton(self.central_widget)
        self.create_pb.setObjectName("create_pb")
        self.central_grid.addWidget(self.create_pb, 5, 1, 1, 1)
        depcreator_mwin.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(depcreator_mwin)
        self.statusbar.setObjectName("statusbar")
        depcreator_mwin.setStatusBar(self.statusbar)

        self.retranslateUi(depcreator_mwin)
        QtCore.QObject.connect(self.create_pb, QtCore.SIGNAL("clicked()"), depcreator_mwin.close)
        QtCore.QMetaObject.connectSlotsByName(depcreator_mwin)

    def retranslateUi(self, depcreator_mwin):
        depcreator_mwin.setWindowTitle(QtGui.QApplication.translate("depcreator_mwin", "Create Department", None, QtGui.QApplication.UnicodeUTF8))
        self.odervalue_lb.setText(QtGui.QApplication.translate("depcreator_mwin", "Ordervalue", None, QtGui.QApplication.UnicodeUTF8))
        self.description_lb.setText(QtGui.QApplication.translate("depcreator_mwin", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.short_lb.setText(QtGui.QApplication.translate("depcreator_mwin", "Short", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lb.setText(QtGui.QApplication.translate("depcreator_mwin", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_rb.setText(QtGui.QApplication.translate("depcreator_mwin", "Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_rb.setText(QtGui.QApplication.translate("depcreator_mwin", "Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("depcreator_mwin", "Create", None, QtGui.QApplication.UnicodeUTF8))

