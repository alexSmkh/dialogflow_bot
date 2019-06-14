from custom_logger import get_logger
import dialogflow_v2 as dialogflow
from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError


logger = get_logger(__name__)


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
    except (GoogleAuthError, GoogleAPIError)  as error:
        logger.exception('Произошла ошибка при работе с сервисом Dialogflow.')
