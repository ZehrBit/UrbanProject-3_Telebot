# python 3.12
# link to telegram bot "https://t.me/Urban_Project_3_Telebot"

import telebot
from telebot import types
from config import TELEGRAM_TOKEN, ASCII_CHARS
from image_processing.pixelate import pixelate
from image_processing.to_ascii import to_ascii

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_states = {}  # тут будем хранить информацию о действиях пользователя


def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Пиксельизация", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton('Преобразовать в "ASCII art"', callback_data="ascii")
    keyboard.add(pixelate_btn, ascii_btn)
    return keyboard


def get_downloaded_file(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    return downloaded_file


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Пришли мне изображение, и я предложу тебе варианты!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message,
                 'Я получил твоё фото! Пожалуйста, пришли набор символов для ASCII арта. Если нажать "Оставить", '
                 'то набор по умолчанию будет "@%#*+=-:. "',
                 reply_markup=types.InlineKeyboardMarkup().add(
                     types.InlineKeyboardButton("Оставить", callback_data="remain")))
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'waiting_for_charset': True}


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Выполняет действия в зависимости от статуса пользователя"""
    if message.chat.id in user_states and 'waiting_for_charset' in user_states[message.chat.id]:
        if message.text:
            user_states[message.chat.id]['charset'] = message.text
            bot.reply_to(message, "Набор символов сохранён. Теперь выбери действие с изображением.",
                         reply_markup=get_options_keyboard())
            del user_states[message.chat.id]['waiting_for_charset']
    else:
        bot.reply_to(message, "Пожалуйста, пришли изображение или выбери действие с изображением.")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Пиксельизация изображения...")
        output_stream = pixelate(get_downloaded_file(call.message))
        bot.send_photo(call.message.chat.id, output_stream)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Преобразование изображения в формат ASCII...")
        charset = user_states[call.message.chat.id].get('charset')
        ascii_art = to_ascii(get_downloaded_file(call.message), charset)
        bot.send_message(call.message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")
    elif call.data == "remain":
        bot.answer_callback_query(call.id, 'Набор символов по умолчанию будет: @%#*+=-:. ')
        bot.reply_to(call.message, "Набор символов оставлен по умолчанию. Теперь выбери действие с изображением.",
                     reply_markup=get_options_keyboard())
        user_states[call.message.chat.id]['charset'] = ASCII_CHARS


bot.polling(none_stop=True)
