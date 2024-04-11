import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from Core import Database, Window
from Util import UI
from Views import HomeView
from lib.res import ColorTheme, Images as ImageSet

db: Database = Database("DB/helody.sqlite")
Color: ColorTheme = ColorTheme(ColorTheme.LIGHT)
Images: ImageSet = ImageSet(theme=Color.get_theme())

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOTPATH)


class Helody(Window):

    def __init__(self):
        super(Helody, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Helody")
        self.setWindowIcon(QIcon(UI.pixmap(Images.icon, 32, 32, Qt.KeepAspectRatioByExpanding,
                                           Qt.SmoothTransformation)))
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.navigate(HomeView)

        self.show()
