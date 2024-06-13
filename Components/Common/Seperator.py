from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QFrame, QSizePolicy

__all__ = "Separator"


class Seperator(QFrame):

    def __init__(self,
                 orientation: Qt.Orientation = Qt.Horizontal,
                 height: int = 3,
                 background: QColor = None):
        super(Seperator, self).__init__()
        if orientation == Qt.Vertical:
            self.setFrameShape(QFrame.VLine)
            self.setMinimumWidth(1)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        else:
            self.setFrameShape(QFrame.HLine)
            self.setMinimumHeight(1)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setContentsMargins(5, 6, 5, 6)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setMidLineWidth(height)
        pal = self.palette()
        pal.setColor(QPalette.WindowText, background)
        self.setPalette(pal)
