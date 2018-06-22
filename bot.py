import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import requests

import xml.etree.ElementTree

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    r = requests.get("https://api.wolframalpha.com/v2/query", {
        'input': update.message.text,
        'appid': 'WOLFRAMALPHA-APPID-HERE'
    })

    e = xml.etree.ElementTree.fromstring(r.text.encode('utf-8').strip())

    result = []
    for plaintext in e.findall('.//plaintext'):
        if isinstance(plaintext.text, basestring):
            result.append(plaintext.text)
    if len(result) == 0:
        result = ["Sorry, I don't know that.."]

    bot.send_message(chat_id=update.message.chat_id, text="\n\n".join(result))

updater = Updater(token='TELEGRAM-BOT-TOKEN-HERE')
dispatcher = updater.dispatcher

# Handle /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Handle regular messages
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

# Start
updater.start_polling()
