from PIL import Image, ImageOps
import io


def negative(downloaded_file):
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    inverted = invert_colors(image)

    output_stream = io.BytesIO()
    inverted.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream


def invert_colors(image):
    return ImageOps.invert(image)
