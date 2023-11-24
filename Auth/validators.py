from re import compile as recompile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PinValidator:
    pin_regex = recompile('\d{6}')

    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not self.pin_regex.fullmatch(password):
            raise ValidationError(
                _('The password must contain exactly six digit'),
                code='pin_6_digits',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )
