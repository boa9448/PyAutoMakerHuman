from threading import Thread, Event, Lock
from typing import Callable

import cv2
import numpy as np
from PySide6.QtCore import Slot, Signal

class WorkThread(Thread):
    def __init__(self, cameras : tuple[cv2.VideoCapture, cv2.VideoCapture]
                    , draw_signal_handler : Callable):
        super().__init__()
        self._exit_event = Event()

    def exit(self) -> None:
        self._exit_event.set()

    def join(self, timeout: float or None = ...) -> None:
        self.exit()
        return super().join(timeout)

    def run(self) -> None:
        pass