# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\guerilla\depcreator.ui'
#
# Created: Tue Jan 13 20:31:48 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_depcreator_dialog(object):
    def setupUi(self, depcreator_dialog):
        depcreator_dialog.setObjectName("depcreator_dialog")
        depcreator_dialog.resize(796, 599)
        self.gridLayout = QtGui.QGridLayout(depcreator_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.desc_pte = QtGui.QPlainTextEdit(depcreator_dialog)
        self.desc_pte.setObjectName("desc_pte")
        self.gridLayout.addWidget(self.desc_pte, 4, 2, 1, 1)
        self.create_pb = QtGui.QPushButton(depcreator_dialog)
        self.create_pb.setObjectName("create_pb")
        self.gridLayout.addWidget(self.create_pb, 6, 2, 1, 1)
        self.ordervalue_sb = QtGui.QSpinBox(depcreator_dialog)
        self.ordervalue_sb.setMaximum(99999)
        self.ordervalue_sb.setObjectName("ordervalue_sb")
        self.gridLayout.addWidget(self.ordervalue_sb, 5, 2, 1, 1)
        self.description_lb = QtGui.QLabel(depcreator_dialog)
        self.description_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.description_lb.setObjectName("description_lb")
        self.gridLayout.addWidget(self.description_lb, 4, 1, 1, 1)
        self.name_lb = QtGui.QLabel(depcreator_dialog)
        self.name_lb.setObjectName("name_lb")
        self.gridLayout.addWidget(self.name_lb, 1, 1, 1, 1)
        self.short_le = QtGui.QLineEdit(depcreator_dialog)
        self.short_le.setObjectName("short_le")
        self.gridLayout.addWidget(self.short_le, 2, 2, 1, 1)
        self.name_le = QtGui.QLineEdit(depcreator_dialog)
        self.name_le.setObjectName("name_le")
        self.gridLayout.addWidget(self.name_le, 1, 2, 1, 1)
        self.odervalue_lb = QtGui.QLabel(depcreator_dialog)
        self.odervalue_lb.setObjectName("odervalue_lb")
        self.gridLayout.addWidget(self.odervalue_lb, 5, 1, 1, 1)
        self.short_lb = QtGui.QLabel(depcreator_dialog)
        self.short_lb.setObjectName("short_lb")
        self.gridLayout.addWidget(self.short_lb, 2, 1, 1, 1)
        self.assetflag_hbox = QtGui.QHBoxLayout()
        self.assetflag_hbox.setObjectName("assetflag_hbox")
        self.shot_rb = QtGui.QRadioButton(depcreator_dialog)
        self.shot_rb.setChecked(True)
        self.shot_rb.setObjectName("shot_rb")
        self.assetflag_hbox.addWidget(self.shot_rb)
        self.asset_rb = QtGui.QRadioButton(depcreator_dialog)
        self.asset_rb.setObjectName("asset_rb")
        self.assetflag_hbox.addWidget(self.asset_rb)
        self.gridLayout.addLayout(self.assetflag_hbox, 3, 2, 1, 1)

        self.retranslateUi(depcreator_dialog)
        QtCore.QMetaObject.connectSlotsByName(depcreator_dialog)

    def retranslateUi(self, depcreator_dialog):
        depcreator_dialog.setWindowTitle(QtGui.QApplication.translate("depcreator_dialog", "Create Department", None, QtGui.QApplication.UnicodeUTF8))
        self.create_pb.setText(QtGui.QApplication.translate("depcreator_dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.description_lb.setText(QtGui.QApplication.translate("depcreator_dialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lb.setText(QtGui.QApplication.translate("depcreator_dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.odervalue_lb.setText(QtGui.QApplication.translate("depcreator_dialog", "Ordervalue", None, QtGui.QApplication.UnicodeUTF8))
        self.short_lb.setText(QtGui.QApplication.translate("depcreator_dialog", "Short", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_rb.setText(QtGui.QApplication.translate("depcreator_dialog", "Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_rb.setText(QtGui.QApplication.translate("depcreator_dialog", "Asset", None, QtGui.QApplication.UnicodeUTF8))

