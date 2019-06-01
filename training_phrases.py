import json
from json import JSONDecodeError
from os import environ
from os import getcwd
from os.path import join
from custom_logger import get_logger

import dialogflow_v2 as dialogflow
from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError


environ["GOOGLE_APPLICATION_CREDENTIALS"] = join(
        getcwd(),
        environ['CREDENTIALS_FILE_NAME']
)


logger = get_logger('Training phrases logger')


def load_intents_data():
    try:
        with open('questions.json', 'r') as data:
            intents_data = json.load(data)
    except (FileNotFoundError, JSONDecodeError) as error:
        logger.info(f'Бот упал с ошибкой {error}')
        logger.warning(error, exc_info=True)
    return intents_data


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    try:
        intents_client = dialogflow.IntentsClient()
        parent = intents_client.project_agent_path(project_id)
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.types.Intent.TrainingPhrase.Part(
                text=training_phrases_part)
            training_phrase = dialogflow.types.Intent.TrainingPhrase    (parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.types.Intent.Message.Text(text=   [message_texts])
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message])

        response = intents_client.create_intent(parent, intent)
        return response
    except (GoogleAuthError, GoogleAPIError) as error:
        logger.info(f'Бот упал с ошибкой {error}.')
        logger.warning(error, exc_info=True)


def start_training():
    project_id = environ['DF_PROJECT_ID']
    
    intents_data = load_intents_data()

    for intent_name in intents_data:
        create_intent(
            project_id,
            intent_name,
            intents_data[intent_name]['questions'],
            intents_data[intent_name]['answer'] 
        )


if __name__ == '__main__':
    start_training()