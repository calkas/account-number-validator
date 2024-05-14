from account_number_validator import AccountNumberValidator
import ocr_account_number_processor
import argparse
import os

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image",
                    required=True,
                    help="Path to the image")
    ap.add_argument("-an", "--account_number",
                    required=True,
                    help="the account number for validation")
    args = vars(ap.parse_args())

    input_account_number = args['account_number']
    image_file = args['image'].format(os.getpid())

    print(
        "\x1b[94m=================================\n..::Account Number "
        "Validation::..\n=================================\x1b[0m")
    anv = AccountNumberValidator(input_account_number)
    account_format_pattern_type = anv.get_account_number_pattern()

    parsed_account_number = ocr_account_number_processor.get_number_account_from_image(image_file,
                                                                                       account_format_pattern_type)

    is_good = anv.is_valid(parsed_account_number)
    if is_good:
        print("Validation process - \x1b[32mPASSED\x1b[0m")
    else:
        print("Validation process - \x1b[31mFAILED\x1b[0m")

    anv.generate_report()
