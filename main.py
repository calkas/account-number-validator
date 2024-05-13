import argparse
import os
import re
import pytesseract
from PIL import Image

ACCOUNT_NUMBER_PATTER = '\d{2}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}'


def input_args_validation(arg_input):
    image_file = arg_input['image']
    assert os.path.isfile(image_file), "Problem with image file"

    # Account number validation
    account_number = arg_input['account_number']
    if account_number[0] == ' ' or account_number[len(account_number) - 1] == ' ':
        assert False, "Please remove trailing space before/after the account number"

    match = re.search(ACCOUNT_NUMBER_PATTER, account_number)
    if not match:
        assert False, ("The input account number is not valid. It should be in the following format:XX XXXX XXXX XXXX "
                       "XXXX XXXX XXXX")


def get_account_number_from_raw_ocr(ocr_txt):
    match = re.search(ACCOUNT_NUMBER_PATTER, parsed_ocr)
    if match:
        return match.group()
    return ''


def account_number_validation(current_account_number, parsed_account_number):
    assert len(current_account_number) == len(parsed_account_number), "Number of digits or format does not match"
    number_of_validated_digits = 0
    error_digit_pos_index = []

    for index in range(0, len(current_account_number)):
        if (current_account_number[index].isdigit() and parsed_account_number[index].isdigit()
                and current_account_number[index] == parsed_account_number[index]):
            number_of_validated_digits = number_of_validated_digits + 1
        else:
            error_digit_pos_index.append(index)

    print("Account number to check:")
    print(account_to_check)
    percent_matcher = (number_of_validated_digits * 100 / 26)
    if percent_matcher != 100.0:
        print("Parsed account number:")
        for i in range(0, len(parsed_account_number)):
            if i in error_digit_pos_index:
                print("\x1b[31m", parsed_account_number[i], "\x1b[0m", end='')
            else:
                print(parsed_account_number[i], end='')

        print("\nMatched in \x1b[33m", percent_matcher, "%\x1b[0m")
        print("Account Number Validation: \x1b[31mFAIL\x1b[0m")
        assert False, "Account number validation failed"

    print("Parsed account number:")
    print(parsed_account_number)
    print("Matched in \x1b[32m", percent_matcher, "%\x1b[0m")
    print("Account Number Validation \x1b[32mPASS\x1b[0m")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image",
                    required=True,
                    help="Path to the image")
    ap.add_argument("-an", "--account_number",
                    required=True,
                    help="the account number for validation")
    args = vars(ap.parse_args())

    input_args_validation(args)

    account_to_check = args['account_number']
    filename = args['image'].format(os.getpid())
    img = Image.open(filename)

    print(
        "\x1b[94m=================================\n..::Account Number "
        "Validation::..\n=================================\x1b[0m")

    parsed_ocr = pytesseract.image_to_string(img)

    print("     * OCR")
    print("---------------------------------------------------------------------")
    print(parsed_ocr)
    print("---------------------------------------------------------------------")

    parsed_account_number = get_account_number_from_raw_ocr(parsed_ocr)

    print("     * Validation")
    account_number_validation(account_to_check, parsed_account_number)
