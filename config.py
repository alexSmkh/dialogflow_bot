from os import getenv
import logging
from dotenv import load_dotenv


class Config:
    load_dotenv()
    logger = logging.getLogger(__name__)
    try:
        TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
        VK_TOKEN = getenv('VK_TOKEN')
        DEVELOPER_ID = getenv('DEVELOPER_ID')
        PROJECT_ID = getenv('PROJECT_ID')
        TRAINING_FILE_NAME = getenv('TRAINING_FILE_NAME')
    except KeyError as error:
        logger.error('Не найдена переменная окружения.', exc_info=True)