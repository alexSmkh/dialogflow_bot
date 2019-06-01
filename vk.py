import random
from os import environ
from dialogflow_handlers import detect_intent_texts
from custom_logger import get_logger

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


logger = get_logger('VK logger')


def send_message_on_vk(event, vk_api, message):
    vk_api.messages.send(
        message=message,
        user_id=event.user_id,
        random_id=random.randint(1, 10000)
    )


def detect_vk_message_by_dialogflow(event, vk_api):
    dialogflow_project_id = environ['DF_PROJECT_ID']
    language_code = 'ru'

    response_from_dialogflow = detect_intent_texts(
        dialogflow_project_id,
        event.user_id,
        event.text,
        language_code
    )
    return response_from_dialogflow


def start_vk_bot(): 
    logger.info('VK-бот запущен')
    token = environ['VK_TOKEN']
    vk_session = vk_api.VkApi(token=token)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error:
        logger.info(f'Бот упал с ошибкой {error}.')
        logger.warning(error, exc_info=True)


    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:  
            response_from_dialogflow = detect_vk_message_by_dialogflow(event, vk)
            if str(response_from_dialogflow.query_result.action) == 'input.unknown':
                continue
            send_message_on_vk(
                event,
                vk, 
                str(response_from_dialogflow.query_result.fulfillment_text)
            )
        
        
if __name__ == '__main__':
    start_vk_bot()
