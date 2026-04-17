import json
import logging
import sys

from google.api_core import exceptions as gcp_exceptions
from google.cloud import dialogflow

from config import GOOGLE_CLOUD_PROJECT_ID
from logger import setup_logging

logger = logging.getLogger(__name__)


def _validate_intent_data(display_name: str, data: dict) -> None:
    if "questions" not in data:
        raise ValueError(
            f"Intent '{display_name}' is missing 'questions' key",
        )
    if not isinstance(data["questions"], list):
        raise ValueError(
            f"Intent '{display_name}': 'questions' must be a list",
        )
    if "answer" not in data:
        raise ValueError(
            f"Intent '{display_name}' is missing 'answer' key",
        )


def create_intents_from_json(json_path: str) -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        intents_data = json.load(f)

    intents_client = dialogflow.IntentsClient()
    parent = f"projects/{GOOGLE_CLOUD_PROJECT_ID}/agent"

    created, failed = 0, 0
    for display_name, data in intents_data.items():
        try:
            _validate_intent_data(display_name, data)
        except ValueError:
            logger.warning("Invalid data for intent '%s'", display_name)
            failed += 1
            continue

        training_phrases = []
        for question in data["questions"]:
            part = dialogflow.Intent.TrainingPhrase.Part(text=question)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        message = dialogflow.Intent.Message(
            text=dialogflow.Intent.Message.Text(text=[data["answer"]]),
        )

        intent = dialogflow.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message],
        )

        try:
            logger.info("Creating intent: %s", display_name)
            intents_client.create_intent(
                request={"parent": parent, "intent": intent},
            )
            logger.info("Intent created: %s", display_name)
            created += 1
        except gcp_exceptions.GoogleAPIError:
            logger.exception("Failed to create intent '%s'", display_name)
            failed += 1

    logger.info(
        "Done: %d created, %d failed out of %d total",
        created,
        failed,
        len(intents_data),
    )


def main() -> None:
    setup_logging()

    if len(sys.argv) != 2:
        logger.error("Usage: python create_intents.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    logger.info("Loading intents from %s", json_path)

    try:
        create_intents_from_json(json_path)
    except (OSError, json.JSONDecodeError):
        logger.exception("Failed to create intents")
        sys.exit(1)


if __name__ == "__main__":
    main()
