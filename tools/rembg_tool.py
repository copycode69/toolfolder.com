from rembg import remove
from PIL import Image
import io

def remove_background(input_image_path, output_image_path):
    """
    Removes the background from an image using rembg and saves it to the output path.

    :param input_image_path: Path to the input image (with background).
    :param output_image_path: Path to save the processed image (without background).
    """
    try:
        # Open the input image
        with open(input_image_path, 'rb') as input_file:
            input_data = input_file.read()
        
        # Process the image
        output_data = remove(input_data)
        
        # Load the output image from the processed data
        output_image = Image.open(io.BytesIO(output_data))

        # Convert RGBA to RGB if saving as JPEG
        if output_image.mode == 'RGBA' and output_image_path.lower().endswith('.jpg'):
            output_image = output_image.convert('RGB')

        # Save the output image
        output_image.save(output_image_path)
        print(f"Background removed and saved to {output_image_path}")
        return output_image

    except Exception as e:
        print(f"Error removing background: {e}")
        return None
