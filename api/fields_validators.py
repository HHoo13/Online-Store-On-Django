import re
from django.core.exceptions import ValidationError
from django.forms import NumberInput, CharField

from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _


class PhoneValidator:
    test_value = None
    message = _("Enter a valid phone number.")
    code = "invalid"
    user_regex = _lazy_re_compile(
        # dot-atom
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])'
        r'*"\Z)',
        re.IGNORECASE,
    )

    def __init__(self, number=None):
        if number is not None:
            self.number = number

    def __call__(self, value):
        if not value or len(value) != 12:
            raise ValidationError(self.message, code=self.code, params={"value": value})
        self.test_value = value


phone_validator = PhoneValidator()


class PhoneField(CharField):
    widget = NumberInput
    default_validators = [phone_validator]
    default_error_messages = {
        "invalid": _("Enter a valid phone number."),
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 12)
        super().__init__(**kwargs)
