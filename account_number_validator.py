import os
import re

# XX XXXX XXXX XXXX XXXX XXXX XXXX
ACCOUNT_NUMBER_PATTERN = r"\d{2}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}"

# XXXXXXXXXXXXXXXXXXXXXXXXXX
ACCOUNT_NUMBER_PATTERN_2 = r"\d{26}"


class AccountNumberValidator:
    def __init__(self, input_account_number):
        self._re_account_number_pattern = ''
        self._determine_type_of_account_number(input_account_number)
        self._input_account_number = input_account_number
        self._account_number_to_check = ''
        self._percentage_of_correctness = 0.0
        self._incorrect_digit_position_index = []

    def _determine_type_of_account_number(self, input_account_number):
        if not input_account_number:
            assert False, "Input account number is empty"
        if input_account_number[0] == ' ' or input_account_number[len(input_account_number) - 1] == ' ':
            assert False, "Please remove trailing space before/after the account number"
        account_number_type_1 = re.search(ACCOUNT_NUMBER_PATTERN, input_account_number)
        account_number_type_2 = re.search(ACCOUNT_NUMBER_PATTERN_2, input_account_number)

        if not account_number_type_1 and not account_number_type_2:
            assert False, (
                "The input account number is not valid. It should be in the following format:XX XXXX XXXX XXXX "
                "XXXX XXXX XXXX or XXXXXXXXXXXXXXXXXXXXXXXXXX")

        if account_number_type_1:
            self._re_account_number_pattern = ACCOUNT_NUMBER_PATTERN
        else:
            self._re_account_number_pattern = ACCOUNT_NUMBER_PATTERN_2

    def get_account_number_pattern(self):
        return self._re_account_number_pattern

    def is_valid(self, account_number_to_check):
        if len(self._input_account_number) != len(account_number_to_check):
            print("Number of digits or format does not match")
            return False

        number_of_validated_digits = 0
        self._account_number_to_check = account_number_to_check

        for index in range(0, len(self._input_account_number)):
            if self._input_account_number[index] == account_number_to_check[index]:
                if self._input_account_number[index].isdigit() and account_number_to_check[index].isdigit():
                    number_of_validated_digits = number_of_validated_digits + 1
            else:
                self._incorrect_digit_position_index.append(index)

        self._percentage_of_correctness = (number_of_validated_digits * 100 / 26)
        if self._percentage_of_correctness != 100.0:
            return False
        return True

    def generate_report(self):
        print("\n============  REPORT ============")
        print("Input Account number:")
        print(self._input_account_number)
        print("Parsed account number:")
        if len(self._incorrect_digit_position_index) != 0:
            for i in range(0, len(self._account_number_to_check)):
                if i in self._incorrect_digit_position_index:
                    print("\x1b[31m", self._account_number_to_check[i], "\x1b[0m", end='')
                else:
                    print(self._account_number_to_check[i], end='')
        else:
            print(self._account_number_to_check)

        if self._percentage_of_correctness != 100.0:
            print("\nMatched in \x1b[33m", self._percentage_of_correctness, "%\x1b[0m")
            print("Account Number Validation: \x1b[31mBAD\x1b[0m")
            return

        print("\nMatched in \x1b[32m", self._percentage_of_correctness, "%\x1b[0m")
        print("Account Number \x1b[32mGOOD\x1b[0m")
        print("=================================")
