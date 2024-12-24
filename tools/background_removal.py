from rembg import remove
from PIL import Image
import io

def remove_background(input_path, output_path):
    with open(input_path, 'rb') as inp_file:
        input_data = inp_file.read()
        output_data = remove(input_data)

    output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
    output_image.save(output_path, format="PNG")
