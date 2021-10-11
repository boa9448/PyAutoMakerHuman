import sys

from PySide6.QtWidgets import *
from .launcher import TrainTestUtilForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainTestUtilForm()
    app.exec()