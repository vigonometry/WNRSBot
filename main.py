#Credits to https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/reply_keyboard_markup_example.py for reference code in creation of the bot user interface

#Note: you will need to run pip install requests and pip install pyTelegramBotAPI prior to running this bot
import random
import csv
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_API', "string")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

with open('WNRS_Level1.csv', newline='') as f:
  reader = csv.reader(f)
  levelOne = list(reader)
  map(lambda x: x[0], levelOne)

with open('WNRS_Level2.csv', newline='') as f:
  reader = csv.reader(f)
  levelTwo = list(reader)
  map(lambda x: x[0], levelTwo)

with open('WNRS_Level3.csv', newline='') as f:
  reader = csv.reader(f)
  levelThree = list(reader)
  map(lambda x: x[0], levelThree)

levelOnelen = len(levelOne)
levelTwolen = len(levelTwo)
levelThreelen = len(levelThree)


categories = ["Level One", "Level Two", "Level Three"]
  


def keyboard():
  row = [KeyboardButton(x) for x in categories]
  markup = ReplyKeyboardMarkup(row_width = 12).add(*row)
  return markup

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,"Select a category",reply_markup=keyboard())

@bot.message_handler(func=lambda message:True)
def sub_messages(message):
    if message.text == "Level One": bot.send_message(message.from_user.id,random.choice(levelOne),reply_markup=keyboard())
   
    elif message.text == "Level Two":
        bot.send_message(message.from_user.id, random.choice(levelTwo), reply_markup=keyboard())
    elif message.text == "Level Three":
      bot.send_message(message.from_user.id, random.choice(levelThree), reply_markup=keyboard())

    else:
        bot.send_message(message.chat.id,f"You sent {message.text} which is not a currently recognized command/input, here are a list of recognized commands [/start]")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://shan-wnrsbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 4000)))
bot.infinity_polling()