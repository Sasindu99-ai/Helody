from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from Core import View, Window


class PlayListsView(View):

    def __init__(self, parent: Window):
        super(PlayListsView, self).__init__(parent, "PlayLists")

        # [Body]
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("PlayListsView"))
