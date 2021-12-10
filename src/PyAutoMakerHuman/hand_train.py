import hand
import train

class HandTrainer:
    def __init__(self):
        self.util = hand.HandUtil()
        self.trainer = train.SvmUtil()
        self.logger = print

    def __del__(self):
        pass

    def set_logger(self, logger) -> None:
        self.logger = logger
        self.util.set_logger(logger)
        self.trainer.set_logger(logger)

    def log(self, log_message: str) -> None:
        self.logger(log_message)