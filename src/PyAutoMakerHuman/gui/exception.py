class FrameException(Exception):
    def __init__(self, message : str):
        super().__init__(message)


class ExitException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class StopException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DataModifyExecption(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NextExecption(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)