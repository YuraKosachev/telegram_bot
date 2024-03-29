import telebot
import webbrowser #Для открытия страниц в браузере
from telebot import types
import helpers.json_helpers as helpers
import constants.app_constants as constants
import time
from random import randrange
import requests


settings = helpers.get_json(constants.SETTINGS)
bot = telebot.TeleBot(settings["bot_key"])
#lesson 5 
#weather bot
@bot.message_handler(commands=["weather"])
def get_weather(message):
    city = ''.join(str(x) for x in message.text.split()[1:]) #split the command
    key = settings["weather_api_key"]
    url = settings["weather_api_endpoint"].format(city,key)
    response = requests.get(url )
    if not response.ok:
        bot.send_message(message.chat.id, f"Что то пошло не так с этим городом{response.content} ")
        return
    bot.reply_to(message, f"мм. погодка та у нас ничего в {response.content} ")

#end lesson 5
#отправка кнопок управления ReplyKeyboardMarkup lesson 3
@bot.message_handler(commands=["sleep"])
def set_sleep(message):
    sleep_sec = randrange(1, 20)
    time.sleep(sleep_sec)
    bot.send_message(message.chat.id, "Хорошо поспал!. мм ")

@bot.message_handler(commands=["start_btn"])
def get_files(message):
    markup = types.ReplyKeyboardMarkup()
    btnSite = types.KeyboardButton("Перейти на сайт")
    btnDel = types.KeyboardButton("Удалить фото") #далее созадются колбеки
    btnUpd = types.KeyboardButton("Изменить текст")
    markup.row(btnSite)
    markup.row(btnDel,btnUpd) #две кнопки в ряду

    #markup.add(types.InlineKeyboardButton("Перейти на сайт", url='https://yandex.ru'))
    #markup.add(types.InlineKeyboardButton("Удалить фото", callback_data='delete'))
    #markup.add(types.InlineKeyboardButton("Изменить текст", callback_data='edit')
    #bot.send_photo(message.chat.id, "https://i.imgur.com/ofwPfHE.png")
    with open('./documents/photos/11111.png', 'rb') as file:
        bot.send_photo(message.chat.id,file,reply_markup=markup)
        #bot.send_audio(message.chat.id,file,reply_markup = markup)
    #bot.send_message(message.chat.id, f"Привет {message.from_user.full_name}", reply_markup=markup)
    bot.register_next_step_handler(message, on_click) #Регистрация функции нажатия кнопки

def on_click(message):
    if message.text == "Перейти на сайт":
        bot.send_message(message.chat.id, "Web is open")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Delete")



#отправка файлов InlineKeyboardMarkup
@bot.message_handler(content_types=['photo', 'audio'])
def get_files(message):
    markup = types.InlineKeyboardMarkup()
    btnSite = types.InlineKeyboardButton("Перейти на сайт", url='https://yandex.ru')
    btnDel = types.InlineKeyboardButton("Удалить фото", callback_data='delete') #далее созадются колбеки
    btnUpd = types.InlineKeyboardButton("Изменить текст", callback_data='edit')
    markup.row(btnSite)
    markup.row(btnDel,btnUpd) #две кнопки в ряду

    #markup.add(types.InlineKeyboardButton("Перейти на сайт", url='https://yandex.ru'))
    #markup.add(types.InlineKeyboardButton("Удалить фото", callback_data='delete'))
    #markup.add(types.InlineKeyboardButton("Изменить текст", callback_data='edit'))
    bot.reply_to(message, "Супер фото", reply_markup=markup)

#Callbacks
@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text",callback.message.chat.id, callback.message.message_id)
#/отправка файлов lesson 3

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id,"Hello")

@bot.message_handler(commands=["help","commands","description"])
def help(message):
    bot.send_message(message.chat.id,f"Вам необходима помощь {message.from_user.full_name}?")

@bot.message_handler(commands=["html"])
def html(message):
    bot.send_message(message.chat.id, f"<strong>Привет {message.from_user.full_name}</strong>", parse_mode="html")

@bot.message_handler(commands=["markdown"])
def markdown(message):
    bot.send_message(message.chat.id, f"** Привет {message.from_user.full_name} **", parse_mode="MarkdownV2")

@bot.message_handler(commands=["site","website"])
def go_to_website(message):
    webbrowser.open("https://yandex.ru")

#отслежтваем все входящие сообщения
@bot.message_handler()
def handler_other_messages(message):
    bot.send_message(message.chat.id,f"Вы написали: '{message.text}'")

bot.infinity_polling()
#bot.polling(none_stop=True)
