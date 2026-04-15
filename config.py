from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
USE_PROXY = env.bool("USE_PROXY", False)
HTTP_PROXY = env.str("HTTP_PROXY") if USE_PROXY else None
GOOGLE_CLOUD_PROJECT_ID = env.str("GOOGLE_CLOUD_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = env.str("GOOGLE_APPLICATION_CREDENTIALS")
