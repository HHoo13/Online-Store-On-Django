from django.core.exceptions import ValidationError
from django.test import TestCase

from api.fields_validators import PhoneValidator


class PhoneValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = PhoneValidator()
    def test_validator_true(self):
        number = '992999887766'
        self.validator.__call__(value=number)
        self.assertEqual(number, self.validator.test_value)

    def test_validator_false_min(self):
        try:
            number = '99299988776'
            self.validator.__call__(value=number)

        except ValidationError as e:
            self.assertEqual("['Enter a valid phone number.']", f"{e}")
    def test_validator_false_max(self):
        try:
            number = '9929998877665'
            self.validator.__call__(value=number)
        except ValidationError as e:
            self.assertEqual("['Enter a valid phone number.']", f"{e}")


