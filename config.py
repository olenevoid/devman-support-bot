from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
VK_GROUP_TOKEN = env.str("VK_GROUP_TOKEN")
DEBUG = env.bool("DEBUG", False)
USE_PROXY = env.bool("USE_PROXY", False)
BOT_PROXY = env.str("BOT_PROXY") if USE_PROXY else None
GOOGLE_CLOUD_PROJECT_ID = env.str("GOOGLE_CLOUD_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = env.str("GOOGLE_APPLICATION_CREDENTIALS")
TELEGRAM_LOG_BOT_TOKEN = env.str("TELEGRAM_LOG_BOT_TOKEN", None)
TELEGRAM_LOG_CHAT_ID = env.str("TELEGRAM_LOG_CHAT_ID", None)
LOG_FILE = env.str("LOG_FILE", "bot.log")
