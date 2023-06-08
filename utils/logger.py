import logging
from utils.handle_config import conf
from common.dir_config import LOGFILEPATH


# Создание форматтера с зеленым цветом
class GreenFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return f"\033[32m{message}\033[0m"  # Зеленый цвет


FORMATTER = conf.get_value("logger", "formatter")
LEVEL = conf.get_value("logger", "level")
OUT_LEVEL = conf.get_value("logger", "outLevel")


class HandleLogging(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(LEVEL)

        out_console = logging.StreamHandler()
        out_console.setLevel(LEVEL)

        # Использование GreenFormatter для форматирования
        out_console.setFormatter(GreenFormatter(FORMATTER))
        self.logger.addHandler(out_console)

    def get_log(self):
        return self.logger


log = HandleLogging(file_name=LOGFILEPATH).get_log()
