import logging

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

import dialogflow_client
from config import DEBUG, VK_GROUP_TOKEN
from logger import setup_logging

logger = logging.getLogger(__name__)


FALLBACK_INTENTS = ["Default Fallback Intent"]


def respond(event, vk) -> None:
    try:
        reply = dialogflow_client.detect_intent_text(
            str(event.user_id),
            event.text,
            skip_intents=FALLBACK_INTENTS,
        )
    except Exception:
        logger.exception("DialogFlow error for user %s", event.user_id)
        return

    if reply is None:
        return

    vk.messages.send(
        user_id=event.user_id,
        message=reply,
        random_id=get_random_id(),
    )


def main() -> None:
    setup_logging(logging.DEBUG if DEBUG else logging.INFO)

    logger.info("Starting VK bot")
    try:
        vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
    except Exception:
        logger.exception("Failed to initialize VK session")
        return

    logger.info("VK bot is running")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.info("Message from user %s", event.user_id)
            try:
                respond(event, vk)
            except Exception:
                logger.exception("Unexpected error handling VK event")


if __name__ == "__main__":
    main()
