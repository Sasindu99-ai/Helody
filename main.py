import sys

from PyQt5.QtWidgets import QApplication

from Helody import Helody

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Helody()
    sys.exit(app.exec_())
