from google.cloud import dialogflow

from config import GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT_ID


def detect_intent_text(
    session_id: str, text: str, language_code: str = "ru-RU",
) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(GOOGLE_CLOUD_PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code,
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )

    return response.query_result.fulfillment_text
