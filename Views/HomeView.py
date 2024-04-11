from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QToolButton

from Core import Window, View
from Views.PlayListsView import PlayListsView


class HomeView(View):
    def __init__(self, parent: Window):
        super(HomeView, self).__init__(parent, "Home")

        # [Body]
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.button = QToolButton()
        self.button.setText("Hello, World!")

        self.layout.addWidget(self.button)

        self.button.clicked.connect(lambda: self.parent.navigate(PlayListsView))
