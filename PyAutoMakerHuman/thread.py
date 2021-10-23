from threading import Thread, Event
from PySide6.QtCore import *

class WorkPyThread(Thread):
    def __init__(self, target, param : tuple, parent = None):
        super().__init__()
        self.target = target
        self.param = param
        self.exit_event = Event()

    def __del__(self):
        pass

    def run(self):
        self.target(*self.param, self.exit_event)

class WorkQThread(QThread):
    def __init__(self, target, param : tuple, parent):
        super().__init__(parent)
        self.target = target
        self.param = param
        self.exit_event = Event()

    def run(self) -> None:
        self.target(*self.param, self.exit_event)

    def join(self, time_out : int = None):
        self.wait(deadline=QDeadlineTimer(QDeadlineTimer.Forever) if time_out is None else time_out)

class WorkThread:
    def __init__(self, thread_type : WorkPyThread or WorkQThread, target, args : tuple, parent = None):
        self.thread_worker = thread_type(target, args, parent)

    def __del__(self):
        pass

    def start(self):
        self.thread_worker.start()

    def join(self):
        self.thread_worker.join()