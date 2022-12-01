from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from request_open_weather import get_ow_forecast

import os
import random
import redis
import datetime
import pytz

r = redis.from_url("redis://red-cdu0mopa6gdv3sp5q8bg:6379") # connection to the database
db_keys = r.keys(pattern='*')   # allows us to fetch data

telegram_bot_token = "5658759506:AAEMEiLNPRLXKKX3Z0IZ9ZK1s1xuBGeqfqg"

updater = Updater("5658759506:AAEMEiLNPRLXKKX3Z0IZ9ZK1s1xuBGeqfqg", use_context=True)

list_of_greets = ["GENIO", "FACHA", "MÁQUINA", "BEAR", "ANIMAL", "ÍDOLO", "OSO", "CRACK", "CAPO", "TITÁN"]


# def start(update: Update, context: CallbackContext):
    
#     user_id = update.message.from_user.id # Get user ID
#     user_name = update.message.from_user.name # Get USERNAME
#     r.set(user_name, user_id)
    
#     message = f"Hola {random.choice(list_of_greets)}, bienvenido al good_morning_bot!. Si te interesa, todos los días te puedo contar cómo va a estar el tiempo. Saludis"
#     update.message.reply_text(message)
    
# def daily_message(context: CallbackContext):

#     message = f"Buen día {random.choice(list_of_greets)}." + "\n" + get_ow_forecast()
#     # send message to all users
#     for keys in db_keys:
#         id = r.get(keys).decode("UTF-8")
#         context.bot.send_message(chat_id=id, text=message)

	
# def weather(update: Update, context: CallbackContext):
def weather(context: CallbackContext):

    message = get_ow_forecast()
    
    for keys in db_keys:
        id = r.get(keys).decode("UTF-8")
        context.bot.send_message(chat_id=id, text=message)

# def once(context: CallbackContext):
    
#     message = "Hello, this message will be sent only once"
    
#     # send message to all users
#     for keys in db_keys:
#         id = r.get(keys).decode("UTF-8")
#         context.bot.send_message(chat_id=id, text=message)

# def good_night(context: CallbackContext):
    
#     message = "Chau bro, que descanses"
#     # send message to all users
#     for keys in db_keys:
#         id = r.get(keys).decode("UTF-8")
#         context.bot.send_message(chat_id=id, text=message)

# j = updater.job_queue # Scheduled messages

# j.run_daily(good_night, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=22, minute=22, second=00, tzinfo=pytz.timezone("America/Argentina/Buenos_Aires")))
# j.run_daily(start, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=23, minute=12, second=00, tzinfo=pytz.timezone("America/Argentina/Buenos_Aires")))
# j.run_daily(weather, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=23, minute=12, second=30, tzinfo=pytz.timezone("America/Argentina/Buenos_Aires")))
# j.run_daily(daily_message, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=8, minute=0, second=00, tzinfo=pytz.timezone("America/Argentina/Buenos_Aires")))

# updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('weather', weather))

# If the application runs locally:
#updater.start_polling()

# Deploy the app:
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://good-morning-bot-01.onrender.com/' + telegram_bot_token)
