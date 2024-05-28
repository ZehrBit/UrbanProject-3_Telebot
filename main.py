# python 3.12
# link to telegram bot "https://t.me/Urban_Project_3_Telebot"

import telebot
from PIL import Image
import io
from telebot import types
from config import TELEGRAM_TOKEN, ASCII_CHARS

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_states = {}  # тут будем хранить информацию о действиях пользователя


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def image_to_ascii(image_stream, new_width=40, charset=ASCII_CHARS):
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')

    # меняем размер сохраняя отношение сторон
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)  # 0,55 так как буквы выше чем шире
    img_resized = image.resize((new_width, new_height))

    img_str = pixels_to_ascii(img_resized, charset)
    img_width = img_resized.width

    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art


def character_set():
    pass


def pixels_to_ascii(image, charset=ASCII_CHARS):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += charset[pixel * len(charset) // 256]
    return characters


# Огрубляем изображение
def pixelate_image(image, pixel_size):
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Пришли мне изображение, и я предложу тебе варианты!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message,
                 'Я получил твоё фото! Пожалуйста, пришли набор символов для ASCII арта. Если нажать "Символы по умолчанию", '
                 'то набор будет "@%#*+=-:. "',
                 reply_markup=types.InlineKeyboardMarkup().add(
                     types.InlineKeyboardButton("Символы по умолчанию", callback_data="remain")))
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'waiting_for_charset': True}


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.id in user_states and 'waiting_for_charset' in user_states[message.chat.id]:
        if message.text:
            user_states[message.chat.id]['charset'] = message.text
            bot.reply_to(message, "Набор символов сохранён. Теперь выбери действие с изображением.",
                         reply_markup=get_options_keyboard())
            del user_states[message.chat.id]['waiting_for_charset']
    else:
        bot.reply_to(message, "Пожалуйста, пришли изображение или выбери действие с изображением.")


def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Пиксельизация", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton('Преобразовать в "ASCII art"', callback_data="ascii")
    keyboard.add(pixelate_btn, ascii_btn)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Пиксельизация изображения...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Преобразование изображения в формат ASCII...")
        ascii_and_send(call.message)
    elif call.data == "remain":
        bot.answer_callback_query(call.id, 'Набор символов по умолчанию будет: @%#*+=-:. ')
        bot.reply_to(call.message, "Набор символов оставлен по умолчанию. Теперь выбери действие с изображением.",
                     reply_markup=get_options_keyboard())
        user_states[call.message.chat.id]['charset'] = ASCII_CHARS
        del user_states[call.message.chat.id]['waiting_for_charset']


def pixelate_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)


def ascii_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    charset = user_states[message.chat.id].get('charset')
    ascii_art = image_to_ascii(image_stream, charset=charset)
    bot.send_message(message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")


bot.polling(none_stop=True)
