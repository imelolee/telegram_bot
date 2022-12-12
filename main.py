import logging

from revChatGPT.revChatGPT import AsyncChatbot as ChatGPTBot

from bot import TelegramBot

import local_settings


def main():

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Setup configuration
    chatgpt_config = {
        'email': local_settings.CHATGPT_EMAIL,
        'password': local_settings.CHATGPT_PASSWORD
    }
    telegram_config = {
        'token': local_settings.TELEGRAM_BOT_TOKEN,
        'allowed_user_ids': local_settings.ALLOWED_TELEGRAM_USER_IDS,
        'use_stream': True,
    }

    if local_settings.PROXYS is not None:
        chatgpt_config.update({'proxy': local_settings.PROXYS})
    if local_settings.CF_COOKIE is not None:
        chatgpt_config.update({'cf_clearance': local_settings.CF_COOKIE})

    debug = local_settings.DEBUG_MODE

    # Setup and run ChatGPT and Telegram bot
    gpt_bot = ChatGPTBot(config=chatgpt_config, debug=debug)
    telegram_bot = TelegramBot(config=telegram_config, gpt_bot=gpt_bot)
    telegram_bot.run()


if __name__ == '__main__':
    main()
