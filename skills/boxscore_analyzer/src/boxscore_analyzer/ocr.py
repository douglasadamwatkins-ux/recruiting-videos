from typing import Dict
from PIL import Image
import pytesseract


def ocr_image(path: str) -> str:
    """Run OCR on an image and return raw extracted text."""
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text
