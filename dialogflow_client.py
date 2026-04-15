import logging

from google.cloud import dialogflow

from config import GOOGLE_CLOUD_PROJECT_ID

logger = logging.getLogger(__name__)


def detect_intent_text(
    session_id: str,
    text: str,
    language_code: str = "ru-RU",
) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(GOOGLE_CLOUD_PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(
        text=text,
        language_code=language_code,
    )
    query_input = dialogflow.QueryInput(text=text_input)

    logger.debug(
        "Detecting intent for session %s, text: %s",
        session_id,
        text,
    )

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )

    result = response.query_result
    logger.debug(
        "DialogFlow response for session %s: %s",
        session_id,
        result.fulfillment_text,
    )

    return result.fulfillment_text
