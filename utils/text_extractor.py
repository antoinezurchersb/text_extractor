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


def convert_white_to_transparent(image: Image.Image) -> Image.Image:
    """
    Convert all white pixels (#FFFFFF) in an image to transparent.

    Args:
        image (Image.Image): The input black and white image.

    Returns:
        Image.Image: The resulting image with white pixels converted to transparency.
    """
    # Convert the image to RGBA (if it isn't already)
    image = image.convert("RGBA")

    # Get image data
    data = np.array(image)

    # Replace white (255, 255, 255) with transparent (255, 255, 255, 0)
    white = (data[..., 0:3] == [255, 255, 255]).all(axis=-1)
    data[white] = [255, 255, 255, 0]

    # Create a new image from the modified data
    transparent_image = Image.fromarray(data)

    return transparent_image


def place_text_image_on_background_with_aspect_ratio(text_image: Image.Image, background_image: Image.Image,
                                                     position: tuple, scale_factor: float) -> Image.Image:
    """
    Place a transparent text image on a background image at a specific position with the same aspect ratio.

    Args:
        text_image (Image.Image): The image of the text with transparency.
        background_image (Image.Image): The background image where the text will be placed.
        position (tuple): (x, y) coordinates where the top-left of the text image should be placed.
        scale_factor (float): Scaling factor to resize the text image while maintaining aspect ratio.

    Returns:
        Image.Image: The combined image with the text placed on the background.
    """
    # Get original size of the text image
    original_width, original_height = text_image.size

    # Calculate new size while keeping the aspect ratio
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # Resize the text image with the same aspect ratio
    resized_text_image = text_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Paste the resized text image onto the background
    background_image.paste(resized_text_image, position, resized_text_image)

    return background_image