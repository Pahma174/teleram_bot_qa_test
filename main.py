import os
import time
import telebot
from telebot import types
from faker import Faker
import random
import string

bot = telebot.TeleBot(token='6869832595:AAEl-iSWnwwa64WdnuVhtVgVNRl8wYnbTrQ', parse_mode='html')

faker = Faker()

formats = ['.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi', '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.css', '.html', '.js', '.json', '.zip', '.rar']
card_types = ['VISA', 'Mastercard', 'Maestro', 'JCB']

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add('Генерация файлов', 'Генерация банковских карт', 'Генерация пароля')

file_format_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
file_format_keyboard.add(*formats, 'Назад')

card_types_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_types_keyboard.add(*card_types, 'Назад')

password_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
password_keyboard.add('Генерация пароля', 'Назад')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! 👋🏻\nЯ бот-генератор тестовых файлов, банковских карт и паролей. Чем могу помочь?", reply_markup=start_keyboard)

@bot.message_handler(func=lambda message: message.text == 'Генерация банковских карт')
def generate_card_type(message):
    bot.send_message(message.chat.id, "Выберите тип банковской карты:", reply_markup=card_types_keyboard)

@bot.message_handler(func=lambda message: message.text == 'Генерация файлов')
def generate_file_format(message):
    bot.send_message(message.chat.id, "Выберите формат файла:", reply_markup=file_format_keyboard)

@bot.message_handler(func=lambda message: message.text in formats)
def handle_file_format(message):
    bot.send_message(message.chat.id, f"Выбран формат файла: {message.text}. Теперь введите размер файла.")

@bot.message_handler(func=lambda message: message.text in card_types)
def handle_card_type(message):
    card_number = faker.credit_card_number(message.text.lower())
    cvv = faker.credit_card_security_code()
    bot.send_message(message.chat.id, f'Тестовая карта {message.text}:\nНомер карты: {card_number}\nCVV: {cvv}')

@bot.message_handler(func=lambda message: message.text == 'Генерация пароля')
def generate_password(message):
    password = generate_random_password()
    bot.send_message(message.chat.id, f"Сгенерированный пароль: {password}")

def generate_random_password():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for _ in range(12))  # Генерация пароля длиной 12 символов
    return password

@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_to_start(message):
    welcome(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки для взаимодействия.")

bot.polling()
