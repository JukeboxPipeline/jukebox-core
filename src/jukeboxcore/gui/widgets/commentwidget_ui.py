# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\dz016.CA\Documents\Jukebox\jukebox\core\gui\widgets\commentwidget.ui'
#
# Created: Mon Jun 23 20:21:36 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CommentWidget(object):
    def setupUi(self, CommentWidget):
        CommentWidget.setObjectName("CommentWidget")
        CommentWidget.resize(400, 300)
        self.comment_grid = QtGui.QGridLayout(CommentWidget)
        self.comment_grid.setObjectName("comment_grid")
        self.updated_dte = QtGui.QDateTimeEdit(CommentWidget)
        self.updated_dte.setReadOnly(True)
        self.updated_dte.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.updated_dte.setObjectName("updated_dte")
        self.comment_grid.addWidget(self.updated_dte, 1, 3, 1, 1)
        self.user_lb = QtGui.QLabel(CommentWidget)
        self.user_lb.setMinimumSize(QtCore.QSize(50, 50))
        self.user_lb.setMaximumSize(QtCore.QSize(50, 150))
        self.user_lb.setFrameShape(QtGui.QFrame.StyledPanel)
        self.user_lb.setFrameShadow(QtGui.QFrame.Plain)
        self.user_lb.setLineWidth(1)
        self.user_lb.setText("")
        self.user_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.user_lb.setObjectName("user_lb")
        self.comment_grid.addWidget(self.user_lb, 0, 1, 2, 1)
        self.content_lb = QtGui.QLabel(CommentWidget)
        self.content_lb.setText("")
        self.content_lb.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.content_lb.setWordWrap(True)
        self.content_lb.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.content_lb.setObjectName("content_lb")
        self.comment_grid.addWidget(self.content_lb, 3, 0, 1, 7)
        self.updated_lb = QtGui.QLabel(CommentWidget)
        self.updated_lb.setObjectName("updated_lb")
        self.comment_grid.addWidget(self.updated_lb, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.comment_grid.addItem(spacerItem, 0, 6, 1, 1)
        self.created_lb = QtGui.QLabel(CommentWidget)
        self.created_lb.setObjectName("created_lb")
        self.comment_grid.addWidget(self.created_lb, 0, 2, 1, 1)
        self.created_dte = QtGui.QDateTimeEdit(CommentWidget)
        self.created_dte.setReadOnly(True)
        self.created_dte.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.created_dte.setObjectName("created_dte")
        self.comment_grid.addWidget(self.created_dte, 0, 3, 1, 1)
        self.by_lb = QtGui.QLabel(CommentWidget)
        self.by_lb.setObjectName("by_lb")
        self.comment_grid.addWidget(self.by_lb, 0, 4, 1, 1)
        self.username_lb = QtGui.QLabel(CommentWidget)
        self.username_lb.setText("")
        self.username_lb.setObjectName("username_lb")
        self.comment_grid.addWidget(self.username_lb, 0, 5, 1, 1)

        self.retranslateUi(CommentWidget)
        QtCore.QMetaObject.connectSlotsByName(CommentWidget)

    def retranslateUi(self, CommentWidget):
        CommentWidget.setWindowTitle(QtGui.QApplication.translate("CommentWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.updated_lb.setText(QtGui.QApplication.translate("CommentWidget", "updated:", None, QtGui.QApplication.UnicodeUTF8))
        self.created_lb.setText(QtGui.QApplication.translate("CommentWidget", "created:", None, QtGui.QApplication.UnicodeUTF8))
        self.by_lb.setText(QtGui.QApplication.translate("CommentWidget", "by:", None, QtGui.QApplication.UnicodeUTF8))

