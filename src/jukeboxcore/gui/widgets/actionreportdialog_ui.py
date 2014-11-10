# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\actionreportdialog.ui'
#
# Created: Fri Nov 07 16:12:58 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ActionReportDialog(object):
    def setupUi(self, ActionReportDialog):
        ActionReportDialog.setObjectName("ActionReportDialog")
        ActionReportDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ActionReportDialog.resize(564, 654)
        self.verticalLayout = QtGui.QVBoxLayout(ActionReportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.status_title_lb = QtGui.QLabel(ActionReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_title_lb.sizePolicy().hasHeightForWidth())
        self.status_title_lb.setSizePolicy(sizePolicy)
        self.status_title_lb.setWordWrap(True)
        self.status_title_lb.setObjectName("status_title_lb")
        self.gridLayout.addWidget(self.status_title_lb, 0, 0, 1, 1)
        self.status_lb = QtGui.QLabel(ActionReportDialog)
        self.status_lb.setText("")
        self.status_lb.setObjectName("status_lb")
        self.gridLayout.addWidget(self.status_lb, 0, 1, 1, 2)
        self.traceback_pte = QtGui.QPlainTextEdit(ActionReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.traceback_pte.sizePolicy().hasHeightForWidth())
        self.traceback_pte.setSizePolicy(sizePolicy)
        self.traceback_pte.setDocumentTitle("")
        self.traceback_pte.setPlainText("")
        self.traceback_pte.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.traceback_pte.setObjectName("traceback_pte")
        self.gridLayout.addWidget(self.traceback_pte, 3, 0, 1, 3)
        self.showtb_checkb = QtGui.QCheckBox(ActionReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showtb_checkb.sizePolicy().hasHeightForWidth())
        self.showtb_checkb.setSizePolicy(sizePolicy)
        self.showtb_checkb.setChecked(False)
        self.showtb_checkb.setObjectName("showtb_checkb")
        self.gridLayout.addWidget(self.showtb_checkb, 2, 2, 1, 1)
        self.message_lb = QtGui.QLabel(ActionReportDialog)
        self.message_lb.setText("")
        self.message_lb.setWordWrap(True)
        self.message_lb.setObjectName("message_lb")
        self.gridLayout.addWidget(self.message_lb, 1, 0, 1, 3)
        self.label = QtGui.QLabel(ActionReportDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ActionReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Abort|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ActionReportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ActionReportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ActionReportDialog.reject)
        QtCore.QObject.connect(self.showtb_checkb, QtCore.SIGNAL("toggled(bool)"), self.traceback_pte.setVisible)
        QtCore.QMetaObject.connectSlotsByName(ActionReportDialog)

    def retranslateUi(self, ActionReportDialog):
        ActionReportDialog.setWindowTitle(QtGui.QApplication.translate("ActionReportDialog", "Report", None, QtGui.QApplication.UnicodeUTF8))
        self.status_title_lb.setText(QtGui.QApplication.translate("ActionReportDialog", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.showtb_checkb.setText(QtGui.QApplication.translate("ActionReportDialog", "Show Traceback", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ActionReportDialog", "Do you wish to continue?", None, QtGui.QApplication.UnicodeUTF8))

