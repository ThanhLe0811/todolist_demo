from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _

class UppercaseAndSpecialCharacterValidator(BaseValidator):
    message = _(
        "The password must contain at least one uppercase letter and one special character."
    )
    code = "password_no_uppercase_or_special_character"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(self.message, code=self.code)

        special_characters = set("!@#$%^&*()_-+=<>?/[]{}|")
        if not any(char in special_characters for char in password):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message