import json
from json import JSONDecodeError
from os import getenv, path, getcwd

from custom_logger import get_logger

from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError


logger = get_logger(__name__)


def load_questions_and_answers():
    if path.exists(path.join(getcwd(), getenv('TRAINING_FILE_NAME'))):
        try:
            with open(getenv('TRAINING_FILE_NAME'), 'r') as data:
                return json.load(data)
        except JSONDecodeError:
            logger.exception('Ошибка при декодировании файла.')


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    try:
        intents_client = dialogflow.IntentsClient()
        parent = intents_client.project_agent_path(project_id)
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.types.Intent.TrainingPhrase.Part(
                text=training_phrases_part)
            training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.types.Intent.Message.Text(text=[message_texts])
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message]
        )
        response = intents_client.create_intent(parent, intent)
        return response
    except (GoogleAuthError, GoogleAPIError):
        logger.exception('Ошибка при создании интента в Dialogflow.')


def start_training():
    project_id = getenv('PROJECT_ID')
    questions_and_answers = load_questions_and_answers()
    if questions_and_answers is None:
        raise('.')

    for intent_name in questions_and_answers:
        questions, answers = questions_and_answers[intent_name]
        create_intent(
            project_id,
            intent_name,
            questions_and_answers[intent_name][questions],
            questions_and_answers[intent_name][answers]
        )


if __name__ == '__main__':
    load_dotenv()
    start_training()
