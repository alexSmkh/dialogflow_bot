import logging
from os import getenv
from telegram.ext import Updater


class LogsHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        send_report(str(log_entry))


def send_report(report):
    updater = Updater(getenv('TELEGRAM_TOKEN'))
    user_id = getenv('DEVELOPER_ID')
    updater.bot.send_message(user_id, report)