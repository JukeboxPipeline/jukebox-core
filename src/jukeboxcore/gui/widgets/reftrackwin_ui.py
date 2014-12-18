# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\projects\jukebox-core\src\jukeboxcore\gui\widgets\reftrackwin.ui'
#
# Created: Thu Dec 18 12:07:05 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ReftrackTool(object):
    def setupUi(self, ReftrackTool):
        ReftrackTool.setObjectName("ReftrackTool")
        ReftrackTool.resize(742, 898)
        self.central_widget = QtGui.QWidget(ReftrackTool)
        self.central_widget.setObjectName("central_widget")
        self.central_widget_vbox = QtGui.QVBoxLayout(self.central_widget)
        self.central_widget_vbox.setObjectName("central_widget_vbox")
        self.addnew_hbox = QtGui.QHBoxLayout()
        self.addnew_hbox.setObjectName("addnew_hbox")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.addnew_hbox.addItem(spacerItem)
        self.addnew_tb = QtGui.QToolButton(self.central_widget)
        self.addnew_tb.setObjectName("addnew_tb")
        self.addnew_hbox.addWidget(self.addnew_tb)
        self.central_widget_vbox.addLayout(self.addnew_hbox)
        self.reftrack_treev = QtGui.QTreeView(self.central_widget)
        self.reftrack_treev.setObjectName("reftrack_treev")
        self.central_widget_vbox.addWidget(self.reftrack_treev)
        self.filtersep_hbox = QtGui.QHBoxLayout()
        self.filtersep_hbox.setObjectName("filtersep_hbox")
        self.showfilter_tb = QtGui.QToolButton(self.central_widget)
        self.showfilter_tb.setIconSize(QtCore.QSize(10, 10))
        self.showfilter_tb.setArrowType(QtCore.Qt.DownArrow)
        self.showfilter_tb.setObjectName("showfilter_tb")
        self.filtersep_hbox.addWidget(self.showfilter_tb)
        self.filtersep_line = QtGui.QFrame(self.central_widget)
        self.filtersep_line.setFrameShape(QtGui.QFrame.HLine)
        self.filtersep_line.setFrameShadow(QtGui.QFrame.Sunken)
        self.filtersep_line.setObjectName("filtersep_line")
        self.filtersep_hbox.addWidget(self.filtersep_line)
        self.central_widget_vbox.addLayout(self.filtersep_hbox)
        self.filter_gb = QtGui.QGroupBox(self.central_widget)
        self.filter_gb.setObjectName("filter_gb")
        self.filter_gb_grid = QtGui.QGridLayout(self.filter_gb)
        self.filter_gb_grid.setObjectName("filter_gb_grid")
        self.loaded_checkb = QtGui.QCheckBox(self.filter_gb)
        self.loaded_checkb.setChecked(True)
        self.loaded_checkb.setObjectName("loaded_checkb")
        self.filter_gb_grid.addWidget(self.loaded_checkb, 1, 0, 1, 1)
        self.search_lb = QtGui.QLabel(self.filter_gb)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_lb.sizePolicy().hasHeightForWidth())
        self.search_lb.setSizePolicy(sizePolicy)
        self.search_lb.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_lb.setObjectName("search_lb")
        self.filter_gb_grid.addWidget(self.search_lb, 3, 0, 1, 1)
        self.imported_checkb = QtGui.QCheckBox(self.filter_gb)
        self.imported_checkb.setChecked(True)
        self.imported_checkb.setObjectName("imported_checkb")
        self.filter_gb_grid.addWidget(self.imported_checkb, 1, 2, 1, 1)
        self.unloaded_checkb = QtGui.QCheckBox(self.filter_gb)
        self.unloaded_checkb.setChecked(True)
        self.unloaded_checkb.setObjectName("unloaded_checkb")
        self.filter_gb_grid.addWidget(self.unloaded_checkb, 1, 1, 1, 1)
        self.newest_checkb = QtGui.QCheckBox(self.filter_gb)
        self.newest_checkb.setChecked(True)
        self.newest_checkb.setObjectName("newest_checkb")
        self.filter_gb_grid.addWidget(self.newest_checkb, 2, 0, 1, 1)
        self.empty_checkb = QtGui.QCheckBox(self.filter_gb)
        self.empty_checkb.setChecked(True)
        self.empty_checkb.setObjectName("empty_checkb")
        self.filter_gb_grid.addWidget(self.empty_checkb, 1, 3, 1, 1)
        self.old_checkb = QtGui.QCheckBox(self.filter_gb)
        self.old_checkb.setChecked(True)
        self.old_checkb.setObjectName("old_checkb")
        self.filter_gb_grid.addWidget(self.old_checkb, 2, 1, 1, 1)
        self.alien_checkb = QtGui.QCheckBox(self.filter_gb)
        self.alien_checkb.setChecked(True)
        self.alien_checkb.setObjectName("alien_checkb")
        self.filter_gb_grid.addWidget(self.alien_checkb, 2, 2, 1, 1)
        self.global_checkb = QtGui.QCheckBox(self.filter_gb)
        self.global_checkb.setChecked(True)
        self.global_checkb.setObjectName("global_checkb")
        self.filter_gb_grid.addWidget(self.global_checkb, 2, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.filter_gb_grid.addItem(spacerItem1, 1, 4, 1, 1)
        self.filter_sep_line = QtGui.QFrame(self.filter_gb)
        self.filter_sep_line.setFrameShape(QtGui.QFrame.HLine)
        self.filter_sep_line.setFrameShadow(QtGui.QFrame.Sunken)
        self.filter_sep_line.setObjectName("filter_sep_line")
        self.filter_gb_grid.addWidget(self.filter_sep_line, 0, 0, 1, 5)
        self.search_le = QtGui.QLineEdit(self.filter_gb)
        self.search_le.setObjectName("search_le")
        self.filter_gb_grid.addWidget(self.search_le, 3, 1, 1, 4)
        self.central_widget_vbox.addWidget(self.filter_gb)
        ReftrackTool.setCentralWidget(self.central_widget)
        self.statusbar = QtGui.QStatusBar(ReftrackTool)
        self.statusbar.setObjectName("statusbar")
        ReftrackTool.setStatusBar(self.statusbar)

        self.retranslateUi(ReftrackTool)
        QtCore.QMetaObject.connectSlotsByName(ReftrackTool)

    def retranslateUi(self, ReftrackTool):
        ReftrackTool.setWindowTitle(QtGui.QApplication.translate("ReftrackTool", "Reftrack Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.addnew_tb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Add a new empty Reftrack to the view below.", None, QtGui.QApplication.UnicodeUTF8))
        self.addnew_tb.setText(QtGui.QApplication.translate("ReftrackTool", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.showfilter_tb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show/Hide Filters", None, QtGui.QApplication.UnicodeUTF8))
        self.showfilter_tb.setText(QtGui.QApplication.translate("ReftrackTool", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_gb.setTitle(QtGui.QApplication.translate("ReftrackTool", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.loaded_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show Loaded (a Reference that is loaded)", None, QtGui.QApplication.UnicodeUTF8))
        self.loaded_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Loaded", None, QtGui.QApplication.UnicodeUTF8))
        self.search_lb.setText(QtGui.QApplication.translate("ReftrackTool", "Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.imported_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show imported", None, QtGui.QApplication.UnicodeUTF8))
        self.imported_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Imported", None, QtGui.QApplication.UnicodeUTF8))
        self.unloaded_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show References that are unloaded.", None, QtGui.QApplication.UnicodeUTF8))
        self.unloaded_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Unloaded", None, QtGui.QApplication.UnicodeUTF8))
        self.newest_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show newest", None, QtGui.QApplication.UnicodeUTF8))
        self.newest_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Newest", None, QtGui.QApplication.UnicodeUTF8))
        self.empty_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show empyt (not in the scene)", None, QtGui.QApplication.UnicodeUTF8))
        self.empty_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Empty", None, QtGui.QApplication.UnicodeUTF8))
        self.old_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show outdated", None, QtGui.QApplication.UnicodeUTF8))
        self.old_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Old", None, QtGui.QApplication.UnicodeUTF8))
        self.alien_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show aliens (do not acutally belong to the current scene/parent)", None, QtGui.QApplication.UnicodeUTF8))
        self.alien_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Alien", None, QtGui.QApplication.UnicodeUTF8))
        self.global_checkb.setToolTip(QtGui.QApplication.translate("ReftrackTool", "Show also global reftracks from the global shot/sequence.", None, QtGui.QApplication.UnicodeUTF8))
        self.global_checkb.setText(QtGui.QApplication.translate("ReftrackTool", "Global", None, QtGui.QApplication.UnicodeUTF8))
        self.search_le.setToolTip(QtGui.QApplication.translate("ReftrackTool", "You can search all for all kind of attributes. Seperate words with spaces to filter for multiple categories.", None, QtGui.QApplication.UnicodeUTF8))

