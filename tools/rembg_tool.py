import os
from rembg import remove
from PIL import Image
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(input_image_path, output_image_path):
    """
    Removes the background from an image using rembg and saves it to the output path.

    :param input_image_path: Path to the input image (with background).
    :param output_image_path: Path to save the processed image (without background).
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"The input image at {input_image_path} does not exist.")
        
        # Check file extension
        if not allowed_file(input_image_path):
            raise ValueError(f"Unsupported file type: {input_image_path}")

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
        output_image.save(output_image_path, quality=95)  # You can adjust the quality if needed
        logger.info(f"Background removed and saved to {output_image_path}")
        return output_image

    except FileNotFoundError as fnf_error:
        logger.error(fnf_error)
        return None
    except ValueError as ve_error:
        logger.error(ve_error)
        return None
    except Exception as e:
        logger.error(f"Error removing background: {e}")
        return None
