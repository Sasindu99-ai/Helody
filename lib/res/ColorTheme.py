from PyQt5.QtGui import QColor

__all__ = ["ColorTheme"]


class Theme:
    background: QColor
    foreground: QColor
    backgroundReverse: QColor
    foregroundReverse: QColor
    accent: QColor
    theme: QColor
    primary: QColor
    secondary: QColor
    seperator: QColor

    def __init__(self,
                 background: str = "",
                 foreground: str = "",
                 background_reverse: str = "",
                 foreground_reverse: str = "",
                 accent: str = "",
                 theme: str = "",
                 primary: str = "",
                 secondary: str = "",
                 seperator: str = ""):
        self.background = QColor(background)
        self.foreground = QColor(foreground)
        self.backgroundReverse = QColor(background_reverse)
        self.foregroundReverse = QColor(foreground_reverse)
        self.accent = QColor(accent)
        self.theme = QColor(theme)
        self.primary = QColor(primary)
        self.secondary = QColor(secondary)
        self.seperator = QColor(seperator)


class ColorTheme:
    LIGHT = 0
    DARK = 1

    __colorTheme: int
    theme: Theme
    __light: Theme = Theme(background="#EBEBEB",
                           foreground="#000000",
                           seperator="#BBBBBB")
    __dark: Theme = Theme(background="#DFDFDF",
                          foreground="#FFFFFF",
                          seperator="#BBBBBB")
    __themes = [__light, __dark]

    def __init__(self, color_theme: int):
        self.__colorTheme = color_theme
        self.theme = self.__themes[self.__colorTheme]

    def get_theme(self) -> int:
        return self.__colorTheme
