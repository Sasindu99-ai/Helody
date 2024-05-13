from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QEvent


class Text(QLabel):
    _full_text: str
    _elide_mode: int = Qt.ElideRight

    def __init__(self, text: str = "", size: int = 12, plt: QPalette = None):
        super(Text, self).__init__(text)
        self._full_text = text
        if plt is not None:
            self.setPalette(plt)
        self.setFont(QFont("Helvetica", size))

    def setElideMode(self, mode: Qt.TextElideMode = Qt.ElideRight):  # noqa
        self._elide_mode = mode
        self.updateText()

    def resizeEvent(self, event: QEvent):
        super().resizeEvent(event)
        self.updateText()

    def updateText(self):  # noqa
        font_metrics = self.fontMetrics()
        elided_text = font_metrics.elidedText(self._full_text, self._elide_mode, self.width())
        super().setText(elided_text)

    def setText(self, text: str):
        self._full_text = text
        self.updateText()
