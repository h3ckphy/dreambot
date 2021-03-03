import telebot
import config

from telebot import types
from datetime import datetime


is_dream = False
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Проверить")
    markup.add(button)

    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}!\n"
                      "Нажми \"Проверить\", чтобы узнать, реальность это или сон.",
                      reply_markup=markup)


@bot.message_handler(content_types=["text"])
def check_reality(message):
    if message.chat.type == "private":
        if message.text == "Где я?":
            global is_dream

            try:
                now = datetime.now()
            except Exception:
                is_dream = True

            if is_dream:
                bot.send_message(message.chat.id, "Это СОН!\nВремя неизвестно! ОСОЗНАЙСЯ!")
            else:
                now = f"{now.day:02d}.{now.month:02d}.{now.year}  {now.hour:02d}:{now.minute:02d}"
                bot.send_message(message.chat.id, f"Это РЕАЛЬНОСТЬ.\nДата: {now}")
                bot.answer_callback_query()


bot.polling(none_stop=True)
