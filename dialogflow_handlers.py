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


logger = get_logger('Dialogflow logger')


def detect_intent_texts(project_id, session_id, text, language_code):
    project_id = environ['DF_PROJECT_ID']
    
    
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
        logger.info(f'Бот упал с ошибкой {error}.')
        logger.warning(error, exc_info=True)

