from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
USE_PROXY = env.bool("USE_PROXY", False)
HTTP_PROXY = env.str("HTTP_PROXY") if USE_PROXY else None
