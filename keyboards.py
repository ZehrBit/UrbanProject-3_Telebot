from telebot import types


def get_options_keyboard():
    """Клавиатура для выбора действия с изображением"""
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Пиксельизация", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII art", callback_data="ascii")
    negative_btn = types.InlineKeyboardButton("Инверсия цветов", callback_data="negative")
    mirror_btn = types.InlineKeyboardButton("Отражение", callback_data="mirror")
    heatmap_btn = types.InlineKeyboardButton("Тепловая карта", callback_data="heatmap")
    sticker_btn = types.InlineKeyboardButton("Размер для стикера", callback_data="sticker")
    joke_btn = types.InlineKeyboardButton("Случайная шутка", callback_data="joke")
    compliment_btn = types.InlineKeyboardButton("Случайный комплимент", callback_data="compliment")
    keyboard.add(pixelate_btn, ascii_btn, negative_btn, mirror_btn, heatmap_btn, sticker_btn, joke_btn, compliment_btn)
    return keyboard


def keyboard_for_mirror_options():
    """Клавиатура для выбора как отразить изображение"""
    keyboard = types.InlineKeyboardMarkup()
    flip_top_bottom_btn = types.InlineKeyboardButton("Сверху вниз", callback_data="Сверху вниз")
    flip_left_right_btn = types.InlineKeyboardButton("Слева направо", callback_data="Слева направо")
    keyboard.add(flip_top_bottom_btn, flip_left_right_btn)
    return keyboard


def keyboard_for_random_message():
    """Клавиатура для выбора случайной шутки и случайного комплимента"""
    keyboard = types.InlineKeyboardMarkup()
    joke_btn = types.InlineKeyboardButton("Случайная шутка", callback_data="joke")
    compliment_btn = types.InlineKeyboardButton("Случайный комплимент", callback_data="compliment")
    keyboard.add(joke_btn, compliment_btn)
    return keyboard


def keyboard_for_flip_a_coin():
    """Клавиатура для подбрасывания монетки"""
    keyboard = types.InlineKeyboardMarkup()
    flip_a_coin_btn = types.InlineKeyboardButton("Подбросить монетку", callback_data="flip_a_coin")
    keyboard.add(flip_a_coin_btn)
    return keyboard
