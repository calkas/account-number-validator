from unittest import TestCase
import account_number_validator
from account_number_validator import AccountNumberValidator

REF_ACCOUNT_NUMBER_1 = "10 1111 2222 3333 4444 5555 6666"
REF_ACCOUNT_NUMBER_2 = "12345678901234567890123456"


class TestAccountNumberValidator(TestCase):
    def test_account_number_with_space_validation(self):
        anv = AccountNumberValidator()
        anv.determine_type_of_account_number(REF_ACCOUNT_NUMBER_1)
        self.assertFalse(anv.is_valid(""))
        self.assertFalse(anv.is_valid("10 1111 2222 3333"))
        self.assertFalse(anv.is_valid("10 1111 2222 3333 4444 5555 7777"))
        self.assertTrue(anv.is_valid(REF_ACCOUNT_NUMBER_1))

    def test_account_number_without_space_validation(self):
        anv = AccountNumberValidator()
        anv.determine_type_of_account_number(REF_ACCOUNT_NUMBER_2)
        self.assertFalse(anv.is_valid("12345678901234567890123451"))
        self.assertTrue(anv.is_valid(REF_ACCOUNT_NUMBER_2))

    def test_account_number_pattern_with_space(self):
        anv = AccountNumberValidator()
        anv.determine_type_of_account_number(REF_ACCOUNT_NUMBER_1)
        self.assertEqual(anv.get_account_number_pattern(), account_number_validator.ACCOUNT_NUMBER_PATTERN)

    def test_account_number_pattern_without_space(self):
        anv = AccountNumberValidator()
        anv.determine_type_of_account_number(REF_ACCOUNT_NUMBER_2)
        self.assertEqual(anv.get_account_number_pattern(), account_number_validator.ACCOUNT_NUMBER_PATTERN_2)
