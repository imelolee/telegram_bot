import asyncio
import logging

import openai
import telegram.constants as constants
from httpx import HTTPError
from telegram import Update, Message
from telegram.error import RetryAfter, BadRequest
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from utils import bilibiliSearch


class TelegramBot:
    """
    Class representing a Chat-GPT3 Telegram Bot.
    """

    def __init__(self, config: dict):
        """
        Initializes the bot with the given configuration and GPT-3 bot object.
        :param config: A dictionary containing the bot configuration
        """
        self.config = config
        self.disallowed_message = "Sorry, you are not allowed to use this bot. "

    async def help(self, update: Update, context) -> None:
        """
        Shows the help menu.
        """
        await update.message.reply_text("/start - Start the bot\n"
                                        "/reset - Reset conversation\n"
                                        "/help - Help menu\n\n"
                                        "Open source at https://github.com/genleel/telegram_bot",
                                        disable_web_page_preview=True)

    async def start(self, update: Update, context):
        """
        Handles the /start command.
        """
        if not self.is_allowed(update):
            logging.info(f'User {update.message.from_user.name} is not allowed to start the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info('Bot started')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ask me everything.😎")

    async def reset(self, update: Update, context):
        """
        Resets the conversation.
        """
        if not self.is_allowed(update):
            logging.info(f'User {update.message.from_user.name} is not allowed to reset the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info('Resetting the conversation...')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Done!👌")

    async def send_typing_periodically(self, update: Update, context, every_seconds: float):
        """
        Sends the typing action periodically to the chat
        """
        while True:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
            await asyncio.sleep(every_seconds)

    async def prompt(self, update: Update, context):
        """
        React to incoming messages and respond accordingly.
        """
        if not self.is_allowed(update):
            logging.info(f'User {update.message.from_user.name} is not allowed to use the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info(f'New message received from user {update.message.from_user.name}')

        # Send "Typing..." action periodically every 2 seconds until the response is received
        typing_task = context.application.create_task(
            self.send_typing_periodically(update, context, every_seconds=2)
        )

        response = await self.get_chatgpt_response(update.message.text)
        typing_task.cancel()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id,
            text=response,
            parse_mode=constants.ParseMode.MARKDOWN
        )

    async def get_chatgpt_response(self, message) -> dict:
        """
        Gets the response from the ChatGPT APIs.
        """
        try:
            # Use the GPT-3 model
            openai.api_key = self.config['openai_api_key']
            completion = openai.Completion.create(
                engine="text-davinci-002",
                prompt=message,
                max_tokens=1024,
                temperature=0.5
            )

            response = completion.choices[0].text
            return response
        except Exception as e:
            logging.info(f'Error while getting the response: {str(e)}')
            return {"message": "I'm having some trouble talking to you, please try again later."}

    async def send_disallowed_message(self, update: Update, context):
        """
        Sends the disallowed message to the user.
        """
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.disallowed_message,
            disable_web_page_preview=True
        )

    async def error_handler(self, update: object, context) -> None:
        """
        Handles errors in the telegram-python-bot library.
        """
        logging.debug(f'Exception while handling an update: {context.error}')

    def is_allowed(self, update: Update) -> bool:
        """
        Checks if the user is allowed to use the bot.
        """
        if self.config['allowed_user_ids'] == '*':
            return True
        return str(update.message.from_user.username) in self.config['allowed_user_ids']

    def run(self):
        """
        Runs the bot indefinitely until the user presses Ctrl+C
        """
        application = ApplicationBuilder().token(self.config['token']).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('reset', self.reset))
        application.add_handler(CommandHandler('help', self.help))

        application.add_handler(MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.prompt))

        application.add_error_handler(self.error_handler)

        application.run_polling()
