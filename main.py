import telebot
import time
import sys
import live_face
import requests
from flask import Flask, request

server = Flask(__name__)
API_TOKEN = "1818910210:AAFHAb9ffRA8k7akf48dOBUpwwpS6lK5cgY"
bot = telebot.TeleBot(API_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    file_id =message.json["photo"][-1]["file_id"]
    file_info = bot.get_file(file_id)

    url = 'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
    response = requests.get(url, stream=True)

    with open("file_from_tg.jpg", "wb") as handle:
        for data in response.iter_content():
            handle.write(data)
    result = live_face.process_image("file_from_tg.jpg")
    time.sleep(1)
    photo = open('released_faces.jpg', 'rb')
    bot.reply_to(message, result)
    bot.send_photo(message.chat.id, photo)

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + TOKEN)
    return "!", 200

bot.polling()

