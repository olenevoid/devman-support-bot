import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import dialogflow_client
from config import BOT_TOKEN, DEBUG, HTTP_PROXY, USE_PROXY
from logger import setup_logging

logger = logging.getLogger(__name__)


def _get_application() -> Application:
    builder = Application.builder().token(BOT_TOKEN)
    if USE_PROXY and HTTP_PROXY:
        builder = builder.proxy(HTTP_PROXY).get_updates_proxy(HTTP_PROXY)
        logger.info("Bot will use proxy: %s", HTTP_PROXY)
    return builder.build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user
        logger.info("User %s started the bot", user.id)
        await update.message.reply_text(
            "Hi! Send me a message and I'll echo it back."
        )
    except Exception:
        logger.exception("Unexpected error in start handler")


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user
        text = update.message.text
        logger.info("Message from user %s: %s", user.id, text)
        try:
            reply = dialogflow_client.detect_intent_text(str(user.id), text)
        except Exception:
            logger.exception("DialogFlow error for user %s", user.id)
            reply = "Something went wrong. Please try again."
        await update.message.reply_text(reply)
    except Exception:
        logger.exception("Unexpected error in respond handler")


def main() -> None:
    setup_logging(logging.DEBUG if DEBUG else logging.INFO)

    logger.info("Starting bot")
    try:
        application = _get_application()
    except Exception:
        logger.exception("Failed to initialize TG bot")
        return

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            respond,
        )
    )

    logger.info("Bot is running")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
