# python 3.12
# link to telegram bot "https://t.me/Urban_Project_3_Telebot"

import telebot
from telebot import types
from config import TELEGRAM_TOKEN, ASCII_CHARS
from image_processing.pixelate import pixelate
from image_processing.to_ascii import to_ascii
from image_processing.negative import negative
from image_processing.convert_to_heatmap import to_heatmap
from image_processing.resize_for_sticker import resize_for_sticker
from image_processing.random_joke import random_joke
from image_processing.mirror import mirror
import keyboards
from loguru import logger

logger.add("logs/info.log", format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | "
                                   "{file}:{line} | {message}", level="INFO", delay=True)
logger.add("logs/error.log", format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | "
                                    "{file}:{line} | {message}", level="ERROR", delay=True)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_status = {
    'waiting for image': True,
    'waiting for charset': False,
    'waiting for image action': False,
    'waiting for flip': False, }

user_status_for_user_id = {}  # хранит информацию о действиях пользователя, user_id, id_photo


@logger.catch
def change_user_status(user_id, status_from_bot):
    """Изменяет статус пользователя"""
    for status, bl in user_status_for_user_id[user_id]["user_status"].items():
        if status_from_bot == status:
            user_status_for_user_id[user_id]["user_status"][status] = True
        else:
            user_status_for_user_id[user_id]["user_status"][status] = False


@logger.catch
def get_downloaded_file(message):
    try:
        photo_id = user_status_for_user_id[message.chat.id]['photo']
        file_info = bot.get_file(photo_id)
        downloaded_file = bot.download_file(file_info.file_path)
        return downloaded_file
    except:
        bot.reply_to(message, "Пожалуйста, пришли изображение.")


@logger.catch
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Я умею преображать картинки и фото!\nПришли мне изображение, и я предложу тебе варианты!")
    change_user_status(message.chat.id, 'waiting for image')


@logger.catch
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.reply_to(message,
                 'Я получил твоё фото!\nПожалуйста, пришли набор символов для ASCII арта.\n'
                 'Если нажать "Символы по умолчанию", то набор по умолчанию будет "@%#*+=-:. "',
                 reply_markup=types.InlineKeyboardMarkup().add(
                     types.InlineKeyboardButton("Символы по умолчанию", callback_data="remain")))
    user_status_for_user_id[message.chat.id] = {'photo': message.photo[-1].file_id, 'user_status': user_status}
    change_user_status(message.chat.id, 'waiting for charset')
    logger.info(
        f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} отправил боту фото')


@logger.catch
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.id in user_status_for_user_id:
        """Выполняет действия в зависимости от статуса пользователя"""
        if user_status_for_user_id[message.chat.id]["user_status"]['waiting for image']:
            bot.reply_to(message, "Пожалуйста, пришли изображение.")
            logger.info(
                f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} бот ждёт изображение, но пользователь прислал текст')
        elif user_status_for_user_id[message.chat.id]["user_status"]["waiting for charset"]:
            if message.text:
                user_status_for_user_id[message.chat.id]['charset'] = message.text
                bot.reply_to(message, "Набор символов сохранён. Теперь выбери действие с изображением.",
                             reply_markup=keyboards.get_options_keyboard())
                change_user_status(message.chat.id, 'waiting for image action')
                logger.info(
                    f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} сохранил свой набор символов: {message.text}')
        elif user_status_for_user_id[message.chat.id]["user_status"]['waiting for image action']:
            bot.reply_to(message, "Сначала выбери действие с изображением или пришли новое",
                         reply_markup=keyboards.get_options_keyboard())
            logger.info(
                f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} бот ждёт действие с изображением, но пользователь прислал текст')
        elif user_status_for_user_id[message.chat.id]["user_status"]['waiting for flip']:
            bot.reply_to(message, "Сначала выбери как отразить изображение или пришли новое",
                         reply_markup=keyboards.keyboard_for_mirror_options())
            logger.info(
                f'User id: {message.chat.id}, first_name: {message.from_user.first_name}, username: {message.from_user.username} бот ждёт выбор как отразить,  но пользователь прислал текст')
    else:
        bot.reply_to(message, "Сначала пришли изображение")


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.message.chat.id in user_status_for_user_id:
        if call.data == "pixelate":
            bot.answer_callback_query(call.id, "Пиксельизация изображения...")
            bot.send_photo(call.message.chat.id, pixelate(get_downloaded_file(call.message)),
                           reply_markup=keyboards.get_options_keyboard())
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "ascii":
            bot.answer_callback_query(call.id, "Преобразование изображения в формат ASCII...")
            charset = user_status_for_user_id[call.message.chat.id].get('charset')
            bot.send_message(call.message.chat.id, f"```\n{to_ascii(get_downloaded_file(call.message), charset)}\n```",
                             parse_mode="MarkdownV2", reply_markup=keyboards.get_options_keyboard())
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "negative":
            bot.answer_callback_query(call.id, "Инверсия цветов изображения...")
            bot.send_photo(call.message.chat.id, negative(get_downloaded_file(call.message)),
                           reply_markup=keyboards.get_options_keyboard())
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "heatmap":
            bot.answer_callback_query(call.id, "Преобразование изображения в тепловую карту...")
            bot.send_photo(call.message.chat.id, to_heatmap(get_downloaded_file(call.message)),
                           reply_markup=keyboards.get_options_keyboard())
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "sticker":
            bot.answer_callback_query(call.id, "Изменение размера изображения для стикера...")
            bot.send_photo(call.message.chat.id, resize_for_sticker(get_downloaded_file(call.message)),
                           reply_markup=keyboards.get_options_keyboard())
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "joke":
            bot.answer_callback_query(call.id, "Отправка случайной шутки...")
            bot.send_message(call.message.chat.id, random_joke())
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "mirror":
            bot.send_message(call.message.chat.id, "Выбери вариант как перевернуть изображение...",
                             reply_markup=keyboards.keyboard_for_mirror_options())
            change_user_status(call.message.chat.id, 'waiting for flip')
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "Сверху вниз":
            bot.answer_callback_query(call.id, "Переворачиваю...")
            bot.send_photo(call.message.chat.id, mirror(get_downloaded_file(call.message), "Сверху вниз"),
                           reply_markup=keyboards.get_options_keyboard())
            change_user_status(call.message.chat.id, 'waiting for image action')
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "Слева направо":
            bot.answer_callback_query(call.id, "Переворачиваю...")
            bot.send_photo(call.message.chat.id, mirror(get_downloaded_file(call.message), "Слева направо"),
                           reply_markup=keyboards.get_options_keyboard())
            change_user_status(call.message.chat.id, 'waiting for image action')
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} использовал {call.data}')
        elif call.data == "remain":
            bot.answer_callback_query(call.id, 'Набор символов по умолчанию будет: @%#*+=-:. ')
            bot.reply_to(call.message, "Набор символов оставлен по умолчанию. Теперь выбери действие с изображением.",
                         reply_markup=keyboards.get_options_keyboard())
            user_status_for_user_id[call.message.chat.id]['charset'] = ASCII_CHARS
            change_user_status(call.message.chat.id, 'waiting for image action')
            logger.info(
                f'User id: {call.message.chat.id}, first_name: {call.from_user.first_name}, username: {call.from_user.username} оставил набор символов по умолчанию')
    else:
        bot.reply_to(call.message, "Пришли, пожалуйста, изображение")


bot.polling(none_stop=True)
