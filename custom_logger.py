import logging
from config import Config
from telegram.ext import Updater


class LogsHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        send_report(str(log_entry))


def send_report(report):
    telegram_token = Config.TELEGRAM_TOKEN
    updater = Updater(token=telegram_token)
    user_id = Config.DEVELOPER_ID
    updater.bot.send_message(user_id, report)


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = LogsHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s ~ %(levelname)s ~ %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger