import logging
from os import environ

from telegram_bot import send_message_on_telegram

from telegram.ext import Updater
from telegram.error import NetworkError, BadRequest


class LogsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        telegram_token = environ['TELEGRAM_TOKEN']
        self.updater = Updater(token=telegram_token)

    def emit(self, record):
        log_entry = self.format(record)
        user_id = environ['DEVELOPER_ID']
        send_message_on_telegram(self.updater, user_id, str(log_entry))


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler())
    return logger