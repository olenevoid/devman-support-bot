import functools
import logging

from google.cloud import dialogflow

from config import GOOGLE_CLOUD_PROJECT_ID

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def _get_session_client():
    return dialogflow.SessionsClient()


def detect_intent_text(
    session_id: str,
    text: str,
    language_code: str = "ru-RU",
    skip_intents: list[str] | None = None,
) -> str | None:
    session_client = _get_session_client()
    session = session_client.session_path(
        GOOGLE_CLOUD_PROJECT_ID,
        session_id,
    )

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

    if skip_intents and result.intent.display_name in skip_intents:
        logger.debug(
            "Skipping intent '%s' for session %s",
            result.intent.display_name,
            session_id,
        )
        return None

    return result.fulfillment_text
