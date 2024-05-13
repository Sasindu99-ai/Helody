from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton

from Util import UI, Styles
from lib.res import Localized


class Button(QToolButton):
    WIDTH = 16
    HEIGHT = 16
    VERTICAL_PADDING = 20
    HORIZONTAL_PADDING = 10
    ICON: str

    def __init__(self, icon: str | QIcon, tooltip: str, size: QSize | None = None, style: str = "",
                 padding: tuple = (10, 20), action: callable = None):
        super(Button, self).__init__()

        if size is not None:
            self.WIDTH = size.width()
            self.HEIGHT = size.height()
        if type(icon) == str:
            self.ICON = icon
            icon: QIcon = UI.icon(self.ICON, width=self.dp(self.WIDTH), height=self.dp(self.HEIGHT))
            self.setIcon(icon)
        self.HORIZONTAL_PADDING = padding[0]
        self.VERTICAL_PADDING = padding[1]
        self.setStyleSheet(style)
        self.setToolTip(Localized(tooltip))
        self.setIconSize(QSize(self.dp(self.WIDTH), self.dp(self.HEIGHT)))
        self.setFixedSize(QSize(self.dp(self.WIDTH) + self.HORIZONTAL_PADDING,
                                self.dp(self.HEIGHT) + self.VERTICAL_PADDING))

        if action is not None:
            self.onClick(action)

    def onClick(self, func: callable): # noqa
        self.clicked.connect(func)  # noqa

    def dp(self, unit: int):
        return UI.dp(unit, self.devicePixelRatio())

    # noinspection PyPep8Naming
    def setPadding(self, w: int, h: int):
        self.HORIZONTAL_PADDING = w
        self.VERTICAL_PADDING = h
        self.setFixedSize(QSize(self.dp(self.WIDTH) + self.HORIZONTAL_PADDING,
                                self.dp(self.HEIGHT) + self.VERTICAL_PADDING))
