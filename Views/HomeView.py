from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QSizePolicy, QWidget, QHBoxLayout

from Components.Common.ImageLabel import ImageLabel
from Components.Common.Text import Text
from Core import Window, View
from lib import Color, Images
from lib.res import Localized


class HomeView(View):
    def __init__(self, parent: Window):
        super(HomeView, self).__init__(parent, "Home")

        self.parent = parent

        # [Body]
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.plt: QPalette = self.palette()
        self.plt.setColor(self.backgroundRole(), Color.theme.background)
        self.plt.setColor(self.foregroundRole(), Color.theme.foreground)
        self.setPalette(self.plt)

        # Song Title
        self.title = Text(Localized("song-title"), self.sp(12), self.plt)
        self.title.setWordWrap(True)
        self.title.setElideMode(Qt.ElideMiddle)
        self.title.setAlignment(Qt.AlignCenter)

        # Song Artist
        self.artist = Text(Localized("song-artist"), self.sp(8), self.plt)
        self.artist.setAlignment(Qt.AlignCenter)

        # Body - Cover Art, Lyrics, etc.
        self.body = QStackedWidget()
        self.body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.cover = ImageLabel(Images.song)

        self.body.addWidget(self.cover)

        # [Add to Layout]
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.artist)
        self.layout.addWidget(self.body)
