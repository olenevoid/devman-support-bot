import logging

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import dialogflow_client
from config import BOT_TOKEN, BOT_PROXY, DEBUG, USE_PROXY
from logger import setup_logging

logger = logging.getLogger(__name__)


def _get_application() -> Application:
    builder = Application.builder().token(BOT_TOKEN)
    if USE_PROXY:
        builder = builder.proxy(BOT_PROXY).get_updates_proxy(BOT_PROXY)
        logger.info("Bot will use proxy: %s", BOT_PROXY)
    return builder.build()


async def handle_error(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.exception("Unexpected error in TG handler")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info("User %s started the bot", user.id)
    try:
        await update.message.reply_text(
            "Привет! Я бот технической поддержки. "
            "Задайте ваш вопрос, и я постараюсь помочь."
        )
    except TelegramError:
        logger.exception("Failed to send start message to user %s", user.id)


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text
    logger.info("Message from user %s", user.id)

    reply = dialogflow_client.detect_intent_text(str(user.id), text)
    if reply is None:
        reply = "Something went wrong. Please try again."

    try:
        await update.message.reply_text(reply)
    except TelegramError:
        logger.exception("Failed to reply to user %s", user.id)


def main() -> None:
    setup_logging(logging.DEBUG if DEBUG else logging.INFO)

    logger.info("Starting bot")
    try:
        application = _get_application()
    except (TelegramError, ValueError):
        logger.exception("Failed to initialize TG bot")
        return

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            respond,
        )
    )
    application.add_error_handler(handle_error)

    logger.info("Bot is running")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
