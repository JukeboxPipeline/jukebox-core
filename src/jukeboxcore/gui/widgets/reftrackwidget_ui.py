# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\reftrackwidget.ui'
#
# Created: Tue Jan 06 10:42:43 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ReftrackWidget(object):
    def setupUi(self, ReftrackWidget):
        ReftrackWidget.setObjectName("ReftrackWidget")
        ReftrackWidget.resize(685, 48)
        ReftrackWidget.setMaximumSize(QtCore.QSize(16777215, 48))
        ReftrackWidget.setAutoFillBackground(True)
        self.verticalLayout = QtGui.QVBoxLayout(ReftrackWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.reftrack_fr = QtGui.QFrame(ReftrackWidget)
        self.reftrack_fr.setMaximumSize(QtCore.QSize(16777215, 48))
        self.reftrack_fr.setAutoFillBackground(False)
        self.reftrack_fr.setFrameShape(QtGui.QFrame.Box)
        self.reftrack_fr.setFrameShadow(QtGui.QFrame.Plain)
        self.reftrack_fr.setLineWidth(2)
        self.reftrack_fr.setObjectName("reftrack_fr")
        self.reftrack_fr_hbox = QtGui.QHBoxLayout(self.reftrack_fr)
        self.reftrack_fr_hbox.setSpacing(0)
        self.reftrack_fr_hbox.setContentsMargins(0, 0, 0, 0)
        self.reftrack_fr_hbox.setObjectName("reftrack_fr_hbox")
        self.type_icon_fr = QtGui.QFrame(self.reftrack_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_icon_fr.sizePolicy().hasHeightForWidth())
        self.type_icon_fr.setSizePolicy(sizePolicy)
        self.type_icon_fr.setMinimumSize(QtCore.QSize(48, 48))
        self.type_icon_fr.setMaximumSize(QtCore.QSize(48, 48))
        self.type_icon_fr.setBaseSize(QtCore.QSize(0, 0))
        self.type_icon_fr.setAutoFillBackground(False)
        self.type_icon_fr.setStyleSheet("")
        self.type_icon_fr.setFrameShape(QtGui.QFrame.NoFrame)
        self.type_icon_fr.setFrameShadow(QtGui.QFrame.Plain)
        self.type_icon_fr.setLineWidth(1)
        self.type_icon_fr.setObjectName("type_icon_fr")
        self.type_icon_hbox = QtGui.QVBoxLayout(self.type_icon_fr)
        self.type_icon_hbox.setSpacing(0)
        self.type_icon_hbox.setContentsMargins(0, 0, 0, 0)
        self.type_icon_hbox.setObjectName("type_icon_hbox")
        self.type_icon_lb = QtGui.QLabel(self.type_icon_fr)
        self.type_icon_lb.setMinimumSize(QtCore.QSize(0, 0))
        self.type_icon_lb.setText("")
        self.type_icon_lb.setObjectName("type_icon_lb")
        self.type_icon_hbox.addWidget(self.type_icon_lb)
        self.reftrack_fr_hbox.addWidget(self.type_icon_fr)
        self.main_fr = QtGui.QWidget(self.reftrack_fr)
        self.main_fr.setObjectName("main_fr")
        self.main_vbox = QtGui.QVBoxLayout(self.main_fr)
        self.main_vbox.setSpacing(0)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_vbox.setObjectName("main_vbox")
        self.upper_fr = QtGui.QWidget(self.main_fr)
        self.upper_fr.setStyleSheet("")
        self.upper_fr.setObjectName("upper_fr")
        self.horizontalLayout = QtGui.QHBoxLayout(self.upper_fr)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.maintext_lb = QtGui.QLabel(self.upper_fr)
        self.maintext_lb.setText("")
        self.maintext_lb.setObjectName("maintext_lb")
        self.horizontalLayout.addWidget(self.maintext_lb)
        self.main_vbox.addWidget(self.upper_fr)
        self.btn_fr = QtGui.QWidget(self.main_fr)
        self.btn_fr.setStyleSheet("")
        self.btn_fr.setObjectName("btn_fr")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.btn_fr)
        self.horizontalLayout_2.setContentsMargins(-1, 2, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.duplicate_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.duplicate_tb.sizePolicy().hasHeightForWidth())
        self.duplicate_tb.setSizePolicy(sizePolicy)
        self.duplicate_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.duplicate_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.duplicate_tb.setIconSize(QtCore.QSize(24, 24))
        self.duplicate_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.duplicate_tb.setAutoRaise(True)
        self.duplicate_tb.setArrowType(QtCore.Qt.NoArrow)
        self.duplicate_tb.setObjectName("duplicate_tb")
        self.horizontalLayout_2.addWidget(self.duplicate_tb)
        self.delete_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_tb.sizePolicy().hasHeightForWidth())
        self.delete_tb.setSizePolicy(sizePolicy)
        self.delete_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.delete_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.delete_tb.setIconSize(QtCore.QSize(24, 24))
        self.delete_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.delete_tb.setAutoRaise(True)
        self.delete_tb.setArrowType(QtCore.Qt.NoArrow)
        self.delete_tb.setObjectName("delete_tb")
        self.horizontalLayout_2.addWidget(self.delete_tb)
        self.load_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_tb.sizePolicy().hasHeightForWidth())
        self.load_tb.setSizePolicy(sizePolicy)
        self.load_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.load_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.load_tb.setIconSize(QtCore.QSize(24, 24))
        self.load_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.load_tb.setAutoRaise(True)
        self.load_tb.setArrowType(QtCore.Qt.NoArrow)
        self.load_tb.setObjectName("load_tb")
        self.horizontalLayout_2.addWidget(self.load_tb)
        self.unload_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unload_tb.sizePolicy().hasHeightForWidth())
        self.unload_tb.setSizePolicy(sizePolicy)
        self.unload_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.unload_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.unload_tb.setIconSize(QtCore.QSize(24, 24))
        self.unload_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.unload_tb.setAutoRaise(True)
        self.unload_tb.setArrowType(QtCore.Qt.NoArrow)
        self.unload_tb.setObjectName("unload_tb")
        self.horizontalLayout_2.addWidget(self.unload_tb)
        self.reference_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reference_tb.sizePolicy().hasHeightForWidth())
        self.reference_tb.setSizePolicy(sizePolicy)
        self.reference_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.reference_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.reference_tb.setIconSize(QtCore.QSize(24, 24))
        self.reference_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.reference_tb.setAutoRaise(True)
        self.reference_tb.setArrowType(QtCore.Qt.NoArrow)
        self.reference_tb.setObjectName("reference_tb")
        self.horizontalLayout_2.addWidget(self.reference_tb)
        self.importtf_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importtf_tb.sizePolicy().hasHeightForWidth())
        self.importtf_tb.setSizePolicy(sizePolicy)
        self.importtf_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.importtf_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.importtf_tb.setIconSize(QtCore.QSize(24, 24))
        self.importtf_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.importtf_tb.setAutoRaise(True)
        self.importtf_tb.setArrowType(QtCore.Qt.NoArrow)
        self.importtf_tb.setObjectName("importtf_tb")
        self.horizontalLayout_2.addWidget(self.importtf_tb)
        self.importref_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importref_tb.sizePolicy().hasHeightForWidth())
        self.importref_tb.setSizePolicy(sizePolicy)
        self.importref_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.importref_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.importref_tb.setIconSize(QtCore.QSize(24, 24))
        self.importref_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.importref_tb.setAutoRaise(True)
        self.importref_tb.setArrowType(QtCore.Qt.NoArrow)
        self.importref_tb.setObjectName("importref_tb")
        self.horizontalLayout_2.addWidget(self.importref_tb)
        self.replace_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replace_tb.sizePolicy().hasHeightForWidth())
        self.replace_tb.setSizePolicy(sizePolicy)
        self.replace_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.replace_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.replace_tb.setIconSize(QtCore.QSize(24, 24))
        self.replace_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.replace_tb.setAutoRaise(True)
        self.replace_tb.setArrowType(QtCore.Qt.NoArrow)
        self.replace_tb.setObjectName("replace_tb")
        self.horizontalLayout_2.addWidget(self.replace_tb)
        self.menu_tb = QtGui.QToolButton(self.btn_fr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_tb.sizePolicy().hasHeightForWidth())
        self.menu_tb.setSizePolicy(sizePolicy)
        self.menu_tb.setMinimumSize(QtCore.QSize(24, 24))
        self.menu_tb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.menu_tb.setIconSize(QtCore.QSize(24, 24))
        self.menu_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.menu_tb.setAutoRaise(True)
        self.menu_tb.setArrowType(QtCore.Qt.NoArrow)
        self.menu_tb.setObjectName("menu_tb")
        self.horizontalLayout_2.addWidget(self.menu_tb)
        self.main_vbox.addWidget(self.btn_fr)
        self.reftrack_fr_hbox.addWidget(self.main_fr)
        self.verticalLayout.addWidget(self.reftrack_fr)

        self.retranslateUi(ReftrackWidget)
        QtCore.QMetaObject.connectSlotsByName(ReftrackWidget)

    def retranslateUi(self, ReftrackWidget):
        ReftrackWidget.setWindowTitle(QtGui.QApplication.translate("ReftrackWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.duplicate_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Duplicate", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.load_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.unload_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Unload", None, QtGui.QApplication.UnicodeUTF8))
        self.reference_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Reference", None, QtGui.QApplication.UnicodeUTF8))
        self.importtf_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.importref_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.replace_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_tb.setText(QtGui.QApplication.translate("ReftrackWidget", "Menu", None, QtGui.QApplication.UnicodeUTF8))

