import logging

from custom_logger import LogsHandler

import dialogflow_v2 as dialogflow
from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError


logger = logging.getLogger(__name__)
logger.addHandler(LogsHandler())


def detect_intent_texts(project_id, session_id, text, language_code):
    try:
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response
    except (GoogleAuthError, GoogleAPIError):
        logger.exception('Произошла ошибка при работе с сервисом Dialogflow.')
