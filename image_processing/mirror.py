from PIL import Image
import io


def mirror(downloaded_file, flip):
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    if flip == "⮁":
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif flip == "⮀":
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream