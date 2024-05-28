from PIL import Image
import io
from config import ASCII_CHARS


def to_ascii(downloaded_file, charset):
    image_stream = io.BytesIO(downloaded_file)
    ascii_art = image_to_ascii(image_stream, charset=charset)
    return ascii_art


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


def pixels_to_ascii(image, charset=ASCII_CHARS):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += charset[pixel * len(charset) // 256]
    return characters
