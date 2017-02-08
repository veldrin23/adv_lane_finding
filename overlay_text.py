from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np


def overlay_text(image, text, pos=(0, 0), color=(255, 255, 255)):
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 42)
    draw.text(pos, text, color, font=font)
    image = np.asarray(image)

    return image
