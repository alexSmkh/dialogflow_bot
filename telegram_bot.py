from custom_logger import Config
from dialogflow_handlers import detect_intent_texts
from custom_logger import get_logger

from telegram.ext import Updater
from telegram.ext import CommandHandler 
from telegram.ext import MessageHandler, Filters
from telegram.error import BadRequest, NetworkError


logger = get_logger(__name__)


def send_message_on_telegram(bot, chat_id, message):
    try:
        bot.send_message(
            chat_id=chat_id,
            text=message
        )
    except (BadRequest, NetworkError) as error:
        logger.info(f'Бот упал с ошибкой {error}')
        logger.error(error, exc_info=True)


def start(bot, update):
    send_message_on_telegram(
        bot,
        chat_id=update.message.chat_id,
        text='Здравствуйте!'
    )


def detect_telegram_message_by_dialogflow(bot, update):
    dialogflow_project_id = Config.PROJECT_ID
    language_code = 'en'
    
    response_from_dialogflow = detect_intent_texts(
        dialogflow_project_id,
        update.message.chat_id,
        update.message.text,
        language_code
    )
    
    send_message_on_telegram(
        bot,
        update.message.chat_id,
        str(response_from_dialogflow.query_result.fulfillment_text)
    )


def start_telegram_bot():
    tlgrm_token = Config.TELEGRAM_TOKEN
    try:
        updater = Updater(token=tlgrm_token)
        dispatcher = updater.dispatcher

        start_hundler = CommandHandler('start', start)
        dialogflow_handler = MessageHandler(Filters.text,   detect_telegram_message_by_dialogflow)

        dispatcher.add_handler(start_hundler)
        dispatcher.add_handler(dialogflow_handler)
        updater.start_polling()
        logger.info('Telegram-bot запущен.')

    except (BadRequest, NetworkError) as error:
        logger.info(f'Бот упал с ошибкой {error}')
        logger.error(error, exc_info=True)


if __name__ == '__main__':
    start_telegram_bot()