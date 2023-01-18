import logging

from bot import TelegramBot

import local_settings


def main():

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Setup configuration
    bot_config = {
        'token': local_settings.TELEGRAM_BOT_TOKEN,
        'allowed_user_ids': local_settings.ALLOWED_TELEGRAM_USER_IDS,
        'use_stream': True,
        'openai_api_key': local_settings.OPEAAI_API_KEY
    }

    # Setup and run ChatGPT and Telegram bot
    telegram_bot = TelegramBot(config=bot_config)
    telegram_bot.run()


if __name__ == '__main__':
    main()
