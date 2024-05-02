from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton

from Util import UI, Styles
from lib.res import Localized


class MenuButton(QToolButton):
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, icon: str | QIcon, tooltip: str):
        super(MenuButton, self).__init__()

        if type(icon) == str:
            icon: QIcon = UI.icon(icon, width=self.dp(self.WIDTH), height=self.dp(self.HEIGHT))
        self.setIcon(icon)
        self.setStyleSheet(Styles.menuButton)
        self.setToolTip(Localized(tooltip))
        self.setIconSize(QSize(self.dp(self.WIDTH), self.dp(self.HEIGHT)))
        self.setFixedSize(QSize(self.dp(self.WIDTH) + 10, self.dp(self.HEIGHT) + 20))

    def onClick(self, func): # noqa
        self.clicked.connect(func)  # noqa

    def dp(self, unit: int):
        return UI.dp(unit, self.devicePixelRatio())
