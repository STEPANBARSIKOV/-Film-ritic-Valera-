# bot.py
import telebot
import logic
import config
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_genre = types.KeyboardButton('По жанру')
    item_year = types.KeyboardButton('По году выпуска')
    markup.add(item_genre, item_year)
    bot.send_message(message.chat.id, "Привет! Я кинокритик Валера, посоветую лучшие фильмы по выбранному вами жанру или году выпуска!\n\nВыберите критерий для подбора фильма:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'По жанру':
        genres = logic.get_random_genres()
        markup = types.ReplyKeyboardMarkup(row_width=1)
        for genre in genres:
            markup.add(types.KeyboardButton(genre))
        bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=markup)
        bot.register_next_step_handler(message, process_genre_step)
    elif message.text == 'По году выпуска':
        bot.send_message(message.chat.id, "Введите год:")
        bot.register_next_step_handler(message, process_year_step)
    else:
        bot.send_message(message.chat.id, "Извините, я не понимаю вашего сообщения. Попробуйте еще раз.")

def process_genre_step(message):
    genre = message.text
    top_movies = logic.get_top_movies_by_genre(genre)
    if top_movies:
        response = f"Вот топ-5 фильмов в жанре '{genre}':\n"
        for i, movie in enumerate(top_movies, start=1):
            response += f"{i}. {movie[0]} - средняя оценка {movie[1]}\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, f"Извините, но в жанре '{genre}' у нас пока нет фильмов.")

def process_year_step(message):
    try:
        year = int(message.text)
        top_movies = logic.get_top_movies_by_year(year)
        if top_movies:
            response = f"Вот топ-5 фильмов за {year} год:\n"
            for i, movie in enumerate(top_movies, start=1):
                response += f"{i}. {movie[0]} - средняя оценка {movie[1]}\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, f"Извините, но за {year} год у нас пока нет фильмов.")
    except ValueError:
        bot.send_message(message.chat.id, "Извините, но вы ввели некорректный год. Попробуйте еще раз.")

if __name__ == '__main__':
    bot.polling(none_stop=True)