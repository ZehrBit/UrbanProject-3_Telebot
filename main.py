# python 3.12
# link to telegram bot "https://t.me/Urban_Project_3_Telebot"

import telebot
from telebot import types
from config import TELEGRAM_TOKEN, ASCII_CHARS
from image_processing.pixelate import pixelate
from image_processing.to_ascii import to_ascii
from image_processing.negative import negative
from image_processing.mirror import mirror
from loguru import logger

logger.add("logs/info.log", format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | "
                                   "{file}:{line} | {message}", level="INFO")
logger.add("logs/error.log", format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | "
                                    "{file}:{line} | {message}", level="ERROR")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_states = {
    'waiting_for_img': True,
    'waiting_for_charset': False,
    'waiting_for_flip': False,
}  # тут будем хранить информацию о действиях пользователя


def change_user_state(user_states: dict, state: str):
    pass


@logger.catch
def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Пиксельизация", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII art", callback_data="ascii")
    negative_btn = types.InlineKeyboardButton("Инверсия цветов", callback_data="negative")
    mirror_btn = types.InlineKeyboardButton("Отражение", callback_data="mirror")
    keyboard.add(pixelate_btn, ascii_btn, negative_btn, mirror_btn)
    return keyboard


@logger.catch
def keyboard_for_mirror_options():
    keyboard = types.InlineKeyboardMarkup()
    flip_top_bottom_btn = types.InlineKeyboardButton("Сверху вниз", callback_data="Сверху вниз")
    flip_left_right_btn = types.InlineKeyboardButton("Слева направо", callback_data="Слева направо")
    keyboard.add(flip_top_bottom_btn, flip_left_right_btn)
    return keyboard


@logger.catch
def get_downloaded_file(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    return downloaded_file


@logger.catch
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Я умею преображать картинки и фото!\nПришли мне изображение, и я предложу тебе варианты!")


@logger.catch
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message,
                 'Я получил твоё фото!\nПожалуйста, пришли набор символов для ASCII арта.\n'
                 'Если нажать "Символы по умолчанию", то набор по умолчанию будет "@%#*+=-:. "',
                 reply_markup=types.InlineKeyboardMarkup().add(
                     types.InlineKeyboardButton("Символы по умолчанию", callback_data="remain")))
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'waiting_for_charset': True}
    logger.info(
        f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} отправил боту фото')


@logger.catch
@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Выполняет действия в зависимости от статуса пользователя"""
    if user_states[message.chat.id]['waiting_for_charset']:
        if message.text:
            user_states[message.chat.id]['charset'] = message.text
            bot.reply_to(message, "Набор символов сохранён. Теперь выбери действие с изображением.",
                         reply_markup=get_options_keyboard())
            user_states[message.chat.id]['waiting_for_charset'] = False
            logger.info(
                f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} сохранил свой набор символов: {message.text}')
    elif user_states[message.chat.id]['waiting_for_flip']:
        bot.reply_to(message, "Для начала выбери как отразить изображение")
    else:
        bot.reply_to(message, "Пожалуйста, пришли изображение.")


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Пиксельизация изображения...")
        bot.send_photo(call.message.chat.id, pixelate(get_downloaded_file(call.message)))
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Преобразование изображения в формат ASCII...")
        charset = user_states[call.message.chat.id].get('charset')
        bot.send_message(call.message.chat.id, f"```\n{to_ascii(get_downloaded_file(call.message), charset)}\n```",
                         parse_mode="MarkdownV2")
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
    elif call.data == "negative":
        bot.answer_callback_query(call.id, "Инверсия цветов изображения...")
        bot.send_photo(call.message.chat.id, negative(get_downloaded_file(call.message)))
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
    elif call.data == "mirror":
        user_states[call.message.chat.id]['waiting_for_flip'] = True
        bot.send_message(call.message.chat.id, "Выбери вариант как перевернуть изображение...",
                         reply_markup=keyboard_for_mirror_options())
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
    elif call.data == "Сверху вниз":
        bot.answer_callback_query(call.id, "Переворачиваю...")
        bot.send_photo(call.message.chat.id, mirror(get_downloaded_file(call.message), "Сверху вниз"))
        user_states[call.message.chat.id]['waiting_for_flip'] = False
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
    elif call.data == "Слева направо":
        bot.answer_callback_query(call.id, "Переворачиваю...")
        bot.send_photo(call.message.chat.id, mirror(get_downloaded_file(call.message), "Слева направо"))
        user_states[call.message.chat.id]['waiting_for_flip'] = False
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
    elif call.data == "remain":
        bot.answer_callback_query(call.id, 'Набор символов по умолчанию будет: @%#*+=-:. ')
        bot.reply_to(call.message, "Набор символов оставлен по умолчанию. Теперь выбери действие с изображением.",
                     reply_markup=get_options_keyboard())
        user_states[call.message.chat.id]['charset'] = ASCII_CHARS
        logger.info(
            f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} оставил набор символов по умолчанию')


bot.polling(none_stop=True)
