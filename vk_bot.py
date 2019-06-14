import random
from custom_logger import get_logger
from config import Config
from dialogflow_handlers import detect_intent_texts

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


logger = get_logger('VK-logger')


def send_message_on_vk(event, vk_api, message):
    vk_api.messages.send(
        message=message,
        user_id=event.user_id,
        random_id=random.randint(1, 10000)
    )


def detect_vk_message_by_dialogflow(event):
    language_code = 'en'
    dialogflow_project_id = Config.PROJECT_ID

    response_from_dialogflow = detect_intent_texts(
        dialogflow_project_id,
        event.user_id,
        event.text,
        language_code
    )
    return response_from_dialogflow


def start_vk_bot():
    vk_session = vk_api.VkApi(token=Config.VK_TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    logger.info('VK-бот запущен.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:  
            response_from_dialogflow = detect_vk_message_by_dialogflow(event)
            if response_from_dialogflow is None:
                continue
            if str(response_from_dialogflow.query_result.intent.display_name) == 'Default Fallback Intent':
                continue
            send_message_on_vk(
                event,
                vk, 
                str(response_from_dialogflow.query_result.fulfillment_text)
            )
        
        
if __name__ == '__main__':
    start_vk_bot()
