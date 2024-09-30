from PIL import Image
import numpy as np


def convert_image_to_black_white_mask(image: Image.Image, threshold: int = 128) -> Image.Image:
    """
    Convert an image to a black and white mask (text in white, background in black).

    Args:
        image (Image.Image): The input image.
        threshold (int, optional): Threshold value for binarization (0-255). Defaults to 128.

    Returns:
        Image.Image: The resulting black and white mask image.
    """
    # Convert image to grayscale
    img = image.convert('L')

    # Convert image to numpy array
    img_array = np.array(img)

    # Create a binary mask: 255 for white (text), 0 for black (background)
    binary_mask = np.where(img_array > threshold, 255, 0).astype(np.uint8)

    # Convert back to an image
    binary_img = Image.fromarray(binary_mask)

    return binary_img