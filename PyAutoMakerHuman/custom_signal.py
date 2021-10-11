import numpy as np
from PySide6.QtCore import *

class LogSignal(QObject):
    sig = Signal(str, tuple)

    def __init__(self):
        super().__init__()

class TrainExitSignal(QObject):
    sig = Signal()

    def __init__(self):
        super().__init__()

class TestCamSignal(QObject):
    sig = Signal(np.ndarray)

    def __init__(self):
        super().__init__()