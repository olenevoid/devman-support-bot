# Бот технической поддержки Devman

Бот технической поддержки для Telegram и ВКонтакте, использующий [Google Dialogflow](https://cloud.google.com/dialogflow) для распознавания намерений и автоматических ответов на вопросы пользователей.

<img width="589" height="521" alt="Telegram_GqJrttYeHy" src="https://github.com/user-attachments/assets/fff4f584-4d84-48e7-9e06-3be5310cf98a" />

**Демо Telegram бота:** [https://t.me/demo_spprt_bot](https://t.me/demo_spprt_bot)

<img width="579" height="558" alt="chrome_rTmS3oHWcF" src="https://github.com/user-attachments/assets/72dcddfa-1a75-468d-9eb4-a4718c020d82" />

**Демо VK бота:** [https://vk.ru/club237694014](https://vk.ru/club237694014)

Боты запускаются независимо друг от друга и могут работать одновременно.

## Возможности

- Автоматические ответы на частые вопросы через Dialogflow
- Поддержка двух платформ: Telegram и ВКонтакте
- Пропуск fallback-интентов в VK боте (бот молчит, если не понял пользователя)
- Логирование в файл с ротацией и опциональные уведомления об ошибках в Telegram
- Поддержка HTTP-прокси

## Установка Python и зависимостей

Скрипт тестировался на версии Python 3.12 и может некорректно работать на более поздних версиях. Для Windows и Mac нужную версию можно скачать по [ссылке](https://www.python.org/downloads/). Для Linux установка альтернативной версии Python осуществляется средствами [pyenv](https://github.com/pyenv/pyenv).

Для установки зависимостей выполните команду:

```
pip install -r requirements.txt
```

Для установки dev-зависимостей (линтеры, форматтеры, pre-commit):

```
pip install -r requirements-dev.txt
pre-commit install
```

## Подготовка Dialogflow

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите [Dialogflow API](https://console.cloud.google.com/apis/library/dialogflow.googleapis.com)
3. Создайте сервисный аккаунт и скачайте JSON-ключ
4. Подготовьте файл с интентами в формате `questions.json`

Для загрузки интентов в Dialogflow выполните:

```
python create_intents.py questions.json
```

## Переменные окружения

Для корректной работы создайте файл `.env` в корне проекта на основе `.env.example`:

- **BOT_TOKEN** — токен Telegram бота. Создание бота и получение токена делается через [BotFather](https://t.me/BotFather). Подробнее в официальной [инструкции](https://core.telegram.org/bots/tutorial#getting-ready)
- **VK_GROUP_TOKEN** — токен сообщества ВКонтакте. Получить можно в настройках группы: Управление → Работа с API → Токены
- **GOOGLE_CLOUD_PROJECT_ID** — идентификатор проекта Google Cloud
- **GOOGLE_APPLICATION_CREDENTIALS** — путь к JSON-файлу с ключами сервисного аккаунта Google Cloud
- **DEBUG** — включение отладочного режима (`True` / `False`). По умолчанию `False`
- **USE_PROXY** — включение HTTP-прокси (`True` / `False`). По умолчанию `False`
- **BOT_PROXY** — адрес прокси в формате `http://ip:port`. Игнорируется, если `USE_PROXY=False`
- **TELEGRAM_LOG_BOT_TOKEN** — (опционально) токен Telegram бота для отправки логов
- **TELEGRAM_LOG_CHAT_ID** — (опционально) id чата для получения логов. Если указан только один из параметров, Telegram-логирование не будет активировано

Пример содержания файла `.env`:

```
BOT_TOKEN=your_tg_bot_token
VK_GROUP_TOKEN=your_vk_group_token
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
DEBUG=False
USE_PROXY=False
BOT_PROXY=http://some-proxy-address:port
TELEGRAM_LOG_BOT_TOKEN=optional_bot_token_for_logs
TELEGRAM_LOG_CHAT_ID=optional_chat_id_for_logs
```

## Запуск

Запуск Telegram бота:

```
python tg_bot.py
```

Запуск VK бота:

```
python vk_bot.py
```
