import telebot
import webbrowser #Для открытия страниц в браузере

bot = telebot.TeleBot("6315495463:AAFxyxwggpOM8BKsOnmbCcKP7RgF-mNCTtI")

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

@bot.message_handler()
def handler_other_messages(message):
    bot.send_message(message.chat.id,f"Вы написали: '{message.text}'")

bot.infinity_polling()
#bot.polling(none_stop=True)
