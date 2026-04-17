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
    reply = dialogflow_client.detect_intent_text(
        str(event.user_id),
        event.text,
        skip_intents=FALLBACK_INTENTS,
    )

    if reply is None:
        return

    try:
        vk.messages.send(
            user_id=event.user_id,
            message=reply,
            random_id=get_random_id(),
        )
    except vk_api.exceptions.ApiError:
        logger.exception("Failed to send message to user %s", event.user_id)


def main() -> None:
    setup_logging(logging.DEBUG if DEBUG else logging.INFO)

    logger.info("Starting VK bot")
    try:
        vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
    except vk_api.exceptions.ApiError:
        logger.exception("Failed to initialize VK session")
        return

    logger.info("VK bot is running")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.info("Message from user %s", event.user_id)
            respond(event, vk)


if __name__ == "__main__":
    main()
