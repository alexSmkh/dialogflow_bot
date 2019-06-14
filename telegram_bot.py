from os import getenv

from dialogflow_handlers import detect_intent_texts
from custom_logger import get_logger

from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler 
from telegram.ext import MessageHandler, Filters
from telegram.error import BadRequest, NetworkError


logger = get_logger('Telegram logger')


def send_message_on_telegram(bot, chat_id, message):
    try:
        bot.send_message(
            chat_id=chat_id,
            text=message
        )
    except (BadRequest, NetworkError):
        logger.exception(f'Ошибка при отправке сообщения в Telegram.')


def start(bot, update):
    send_message_on_telegram(
        bot,
        chat_id=update.message.chat_id,
        text='Здравствуйте!'
    )


def detect_telegram_message_by_dialogflow(bot, update):
    dialogflow_project_id = getenv('PROJECT_ID')
    language_code = 'en'
    
    response_from_dialogflow = detect_intent_texts(
        dialogflow_project_id,
        update.message.chat_id,
        update.message.text,
        language_code
    )
    if response_from_dialogflow is not None:
        send_message_on_telegram(
            bot,
            update.message.chat_id,
            str(response_from_dialogflow.query_result.fulfillment_text)
        )


def start_telegram_bot():
    tlgrm_token = getenv('TELEGRAM_TOKEN')
    updater = Updater(token=tlgrm_token)
    dispatcher = updater.dispatcher
    start_hundler = CommandHandler('start', start)
    dialogflow_handler = MessageHandler(Filters.text,   detect_telegram_message_by_dialogflow)

    dispatcher.add_handler(start_hundler)
    dispatcher.add_handler(dialogflow_handler)
    updater.start_polling()
    logger.info('Telegram-bot запущен.')


if __name__ == '__main__':
    load_dotenv()
    start_telegram_bot()