import os
import time
import telebot
from telebot import types
from faker import Faker
import random

bot = telebot.TeleBot(token='6869832595:AAEl-iSWnwwa64WdnuVhtVgVNRl8wYnbTrQ', parse_mode='html')

faker = Faker()

formats = ['.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi', '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.css', '.html', '.js', '.json', '.zip', '.rar']
card_types = ['VISA', 'Mastercard', 'Maestro', 'JCB']

card_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_type_keyboard.add('Генерация файлов', 'Генерация банковских карт')

file_format_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
file_format_keyboard.add(*formats)

card_types_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_types_keyboard.add(*card_types)

# Словарь для отслеживания состояний пользователей
user_state = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! 👋🏻\nЯ бот-генератор тестовых файлов и банковских карт. Чем могу помочь?", reply_markup=card_type_keyboard)

@bot.message_handler(func=lambda message: message.text == 'Генерация банковских карт')
def generate_card_type(message):
    bot.send_message(message.chat.id, "Выберите тип банковской карты:", reply_markup=card_types_keyboard)

@bot.message_handler(func=lambda message: message.text == 'Генерация файлов')
def generate_file_format(message):
    # Устанавливаем состояние пользователя в "waiting_for_file_format"
    user_state[message.chat.id] = "waiting_for_file_format"
    bot.send_message(message.chat.id, "Выберите формат файла:", reply_markup=file_format_keyboard)

@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "waiting_for_file_format")
def handle_file_format(message):
    bot.send_message(message.chat.id, f"Выбран формат файла: {message.text}. Теперь введите размер файла.")

    # Устанавливаем состояние пользователя в "waiting_for_file_size"
    user_state[message.chat.id] = "waiting_for_file_size"
    user_state[f"{message.chat.id}_format"] = message.text

@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "waiting_for_file_size")
def handle_file_size(message):
    # Проверяем, является ли введенный размер числом
    try:
        file_size = int(message.text)
        if file_size <= 0:
            raise ValueError("Размер файла должен быть положительным числом.")
        
        # Теперь у нас есть размер файла, который можно использовать для генерации
        bot.send_message(message.chat.id, f"Выбран размер файла: {file_size}.")
        
        # Обрабатываем генерацию файла с выбранным форматом и размером
        format_selected = user_state[f"{message.chat.id}_format"]
        generate_file(message.chat.id, format_selected, file_size)
        
        # Сбрасываем состояние пользователя
        user_state[message.chat.id] = None
        user_state[f"{message.chat.id}_format"] = None
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите положительное число для размера файла.")

# Функция для генерации файла
def generate_file(chat_id, file_format, file_size):
    # Генерируем уникальное имя файла
    timestamp = int(time.time())
    filename = f'{timestamp}-{file_size}-bytes{file_format}'

    # Генерируем и сохраняем файл с заданным названием, записываем туда случайные байты
    with open(filename, "wb") as f:
        random_bytes = os.urandom(file_size)
        f.write(random_bytes)
    
    # Отправляем сгенерированный файл
    with open(filename, "rb") as f:
        bot.send_document(chat_id, f)
    
    # Удаляем сгенерированный файл
    os.unlink(filename)

@bot.message_handler(func=lambda message: message.text in card_types)
def handle_card_type(message):
    card_number = faker.credit_card_number(message.text.lower())
    cvv = faker.credit_card_security_code()
    bot.send_message(message.chat.id, f'Тестовая карта {message.text}:\nНомер карты: {card_number}\nCVV: {cvv}')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки для взаимодействия.")

bot.polling()
