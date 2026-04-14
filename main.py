import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import logger
from config import BOT_TOKEN, HTTP_PROXY, USE_PROXY

logger = logging.getLogger(__name__)


def _get_application() -> Application:
    builder = Application.builder().token(BOT_TOKEN)
    if USE_PROXY and HTTP_PROXY:
        builder = builder.proxy(HTTP_PROXY).get_updates_proxy(HTTP_PROXY)
        logger.info("Bot will use proxy: %s", HTTP_PROXY)
    return builder.build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info("User %s started the bot", user.id)
    await update.message.reply_text(
        "Hi! Send me a message and I'll echo it back."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info(
        "Echoing message from user %s: %s", user.id, update.message.text
    )
    await update.message.reply_text(update.message.text)


def main() -> None:
    logger.info("Starting bot")
    application = _get_application()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo,
        )
    )

    logger.info("Bot is running")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
