from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget

from Components.Common.ImageLabel import ImageLabel
from Components.Common.Slider import Slider
from Components.Common.Text import Text
from Components.Home.HomeButton import HomeButton
from Components.Home.MiniButton import MiniButton
from Core import View, Window
from lib import Color, Images, Localized
from Util import Styles


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
        self.body.setMinimumHeight(self.dp(100))

        self.cover = ImageLabel(Images.song)
        self.lyrics = QWidget(self)
        self.download = QWidget(self)

        self.body.addWidget(self.cover)
        self.body.addWidget(self.lyrics)
        self.body.addWidget(self.download)
        self.body.setCurrentWidget(self.cover)

        # Actions
        self.actions = QWidget(self)
        self.actions.setLayout(QHBoxLayout())
        self.actions.layout().setAlignment(Qt.AlignCenter)
        self.actions.layout().setContentsMargins(0, 0, 0, 0)
        self.actions.layout().setSpacing(0)
        self.actions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.sort = MiniButton(Images.sort, "sort-by")
        self.songInfo = MiniButton(Images.songInfo, "song-info")
        self.lyricsButton = MiniButton(Images.lyrics, "lyrics")
        self.shuffle = MiniButton(Images.shuffle, "shuffle")
        self.repeat = MiniButton(Images.overPlay, "repeat")
        self.fullScreen = MiniButton(Images.maximize, "maximize")

        self.actions.layout().addWidget(self.sort)
        self.actions.layout().addWidget(self.songInfo)
        self.actions.layout().addWidget(self.lyricsButton)
        self.actions.layout().addStretch()
        self.actions.layout().addWidget(self.shuffle)
        self.actions.layout().addWidget(self.repeat)
        self.actions.layout().addWidget(self.fullScreen)

        self.slider = Slider(Qt.Horizontal, self)
        self.slider.setStyleSheet(Styles.defaultSlider)
        self.slider.setCursor(Qt.PointingHandCursor)

        # Time Labels
        self.times = QWidget(self)
        self.times.setLayout(QHBoxLayout())
        self.times.layout().setAlignment(Qt.AlignCenter)
        self.times.layout().setContentsMargins(0, 0, 0, 0)
        self.times.layout().setSpacing(0)
        self.times.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.currentTime = Text("00:00:00", self.sp(8), self.plt)
        self.currentTime.setContentsMargins(20, 0, 5, 0)

        self.volumeSlider = Slider(Qt.Horizontal, self)
        self.volumeSlider.setStyleSheet(Styles.defaultSlider)
        self.volumeSlider.setCursor(Qt.PointingHandCursor)
        self.volumeSlider.setMaximumWidth(300)
        self.volumeSlider.setMinimumWidth(200)
        self.volumeSlider.setRange(0, 100)

        self.volumeLabel = Text("100%", self.sp(8), self.plt)
        self.volumeLabel.setContentsMargins(0, 0, 20, 0)

        self.totalTime = Text("00:00:00", self.sp(8), self.plt)
        self.totalTime.setContentsMargins(5, 0, 20, 0)

        self.times.layout().addWidget(self.currentTime)
        self.times.layout().addStretch()
        self.times.layout().addWidget(self.volumeSlider)
        self.times.layout().addWidget(self.volumeLabel)
        self.times.layout().addStretch()
        self.times.layout().addWidget(self.totalTime)

        # Player Controls
        self.controls = QWidget(self)
        self.controls.setLayout(QHBoxLayout())
        self.controls.layout().setAlignment(Qt.AlignCenter)
        self.controls.layout().setContentsMargins(0, 0, 0, 0)
        self.controls.layout().setSpacing(0)
        self.controls.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.volume = HomeButton(Images.lowVolume, "low-volume")
        self.openFiles = HomeButton(
            Images.openFiles,
            "open-files",
            action=lambda: self.parent.openFiles(
                self.parent.player.currentPlaylist, True))
        self.previous = HomeButton(Images.previous, "previous")
        self.play = HomeButton(Images.play,
                               "play",
                               action=self.parent.player.play)
        self.next = HomeButton(Images.next, "next")
        self.stop = HomeButton(Images.stop, "stop")
        self.playingList = HomeButton(Images.playingList, "playing-list")

        self.controls.layout().addWidget(self.volume)
        self.controls.layout().addStretch()
        self.controls.layout().addWidget(self.openFiles)
        self.controls.layout().addWidget(self.previous)
        self.controls.layout().addWidget(self.play)
        self.controls.layout().addWidget(self.next)
        self.controls.layout().addWidget(self.stop)
        self.controls.layout().addStretch()
        self.controls.layout().addWidget(self.playingList)

        # [Add to Layout]
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.artist)
        self.layout.addWidget(self.body)
        self.layout.addWidget(self.actions)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.times)
        self.layout.addWidget(self.controls)

    def onCreate(self):
        pass
