from PIL import Image, ImageOps
import io


def resize_for_sticker(downloaded_file):
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    resized_image = resize_512(image)

    output_stream = io.BytesIO()
    resized_image.save(output_stream, format="PNG")
    output_stream.seek(0)
    return output_stream


def resize_512(image, max_size=512):
    width, height = image.size
    if width > height:
        ratio = max_size / float(width)
        new_height = int(height * ratio)
        new_width = max_size
    else:
        ratio = max_size / float(height)
        new_width = int(width * ratio)
        new_height = max_size
    return image.resize((new_width, new_height))
