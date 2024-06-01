from PIL import Image, ImageOps
import io


def to_heatmap(downloaded_file):
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    heatmap = convert_to_heatmap(image)

    output_stream = io.BytesIO()
    heatmap.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream


def convert_to_heatmap(image):
    # Преобразование изображения в оттенки серого
    gray_image = image.convert('L')
    # Преобразование в тепловую карту
    heatmap_image = ImageOps.colorize(gray_image, black="blue", white="red")
    return heatmap_image
