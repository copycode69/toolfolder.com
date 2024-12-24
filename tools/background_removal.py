from rembg import remove
from PIL import Image
import io

def remove_background(input_path, output_path):
    # Open the input image
    with open(input_path, 'rb') as input_file:
        input_image = input_file.read()
    
    # Process the image to remove the background
    output_image = remove(input_image)
    
    # Save the output image
    with open(output_path, 'wb') as output_file:
        output_file.write(output_image)

# Example usage
remove_background("input.jpg", "output.png")
