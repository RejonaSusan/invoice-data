import pytesseract
from PIL import Image

def extract_text_from_image(stream, num):
    img = Image.open(stream)
    img = img.rotate(num, expand=True)
    text = pytesseract.image_to_string(img)
    return text