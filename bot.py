from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from request_open_weather import get_ow_forecast

import os

telegram_bot_token = "5658759506:AAEMEiLNPRLXKKX3Z0IZ9ZK1s1xuBGeqfqg"

updater = Updater("5658759506:AAEMEiLNPRLXKKX3Z0IZ9ZK1s1xuBGeqfqg", use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text("Hello there! Welcome to memo_bot")

def weather(update: Update, context: CallbackContext):
	update.message.reply_text(get_ow_forecast())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('weather', weather))

# If the application runs locally:
#updater.start_polling()

# Deploy the app:
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://good-morning-bot-01.onrender.com/' + telegram_bot_token)

#updater.bot.setWebhook('https://good-morning-bot-01.herokuapp.com/' + telegram_bot_token)
