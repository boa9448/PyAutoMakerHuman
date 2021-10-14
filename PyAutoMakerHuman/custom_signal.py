import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import QImage

class LogSignal(QObject):
    sig = Signal(str, tuple)

    def __init__(self):
        super().__init__()

class TrainDataSetAddEndSignal(QObject):
    sig = Signal()

    def __init__(self):
        super().__init__()

class TestDataSetAddEndSignal(QObject):
    sig = Signal()

    def __init__(self):
        super().__init__()

class TrainExitSignal(QObject):
    sig = Signal()

    def __init__(self):
        super().__init__()

class TestCamSignal(QObject):
    ORIGINAL = 1
    RESULT = 2
    sig = Signal(int, np.ndarray)

    def __init__(self):
        super().__init__()