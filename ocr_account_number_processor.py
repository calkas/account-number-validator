import re
import pytesseract


def get_number_account_from_image(img_file, account_number_pattern):
    ocr = pytesseract.image_to_string(img_file)
    print("-------------------- OCR --------------------")
    print(ocr)
    print("---------------------------------------------")
    match = re.search(account_number_pattern, ocr)
    if not match:
        return ''
    return match.group()
