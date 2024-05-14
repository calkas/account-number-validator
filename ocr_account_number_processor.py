import re
import pytesseract
from PIL import Image


def get_number_account_from_image(img_file, account_number_pattern):
    image = Image.open(img_file)
    ocr = pytesseract.image_to_string(image)
    print("-------------------- OCR --------------------")
    print(ocr)
    print("---------------------------------------------")
    match = re.search(account_number_pattern, ocr)
    image.close()
    if not match:
        return ''
    return match.group()
