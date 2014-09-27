from PySide import QtCore
from PySide import QtGui


class JB_PlainTextEdit(QtGui.QPlainTextEdit):
    """A plain text edit that supports placeholder text
    """

    def __init__(self, text="", parent=None):
        """Consturct a new text edit with the given text and parent

        :param text: the inital text to display
        :type text: str
        :param parent: the parent widget
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(JB_PlainTextEdit, self).__init__(text, parent)
        self._placeholder = ""

    def placeholder(self):
        """Return the placeholder text

        :returns: placeholder
        :rtype: str
        :raises: None
        """
        return self._placeholder

    def set_placeholder(self, text):
        """Set the placeholder text that will be displayed
        when the text is empty and the widget is out of focus

        :param text: The text for the placeholder
        :type text: str
        :raises: None
        """
        if self._placeholder != text:
            self._placeholder = text
            if not self.hasFocus():
                self.update()

    def paintEvent(self, event):
        """Paint the widget

        :param event:
        :type event:
        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.toPlainText() and not self.hasFocus() and self._placeholder:
            p = QtGui.QPainter(self.viewport())
            p.setClipping(False)
            col = self.palette().text().color()
            col.setAlpha(128)
            oldpen = p.pen()
            p.setPen(col)
            p.drawText(self.viewport().geometry(), QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, self._placeholder)
            p.setPen(oldpen)
        else:
            return super(JB_PlainTextEdit, self).paintEvent(event)

    def focusInEvent(self, e):
        """Repaint the entire viewport

        :param e: the focus event
        :type e: QFocusEvent
        :returns: None
        :rtype: None
        :raises: None
        """
        return super(JB_PlainTextEdit, self).focusOutEvent(e)

    def focusOutEvent(self, e):
        """Repaint the entire viewport

        :param e: the focus event
        :type e: QFocusEvent
        :returns: None
        :rtype: None
        :raises: None
        """

        return super(JB_PlainTextEdit, self).focusOutEvent(e)
