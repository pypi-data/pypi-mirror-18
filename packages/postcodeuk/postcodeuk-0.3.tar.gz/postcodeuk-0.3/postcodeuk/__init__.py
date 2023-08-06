"""
Write a library that supports validating and formatting post codes for UK.
The details of which post codes are valid and which are the parts they consist of can be
found at https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting.
The API that this library provides is your choice.
"""
import re
from rstr import xeger


class PostCodeUk:
    N = '[0-9]'
    A1 = '[A-PR-UWYZ]'
    A2 = '[A-HK-Y]'
    A3 = '[ABCDEFGHJKPSTUW]'
    A4 = '[ABEHMNPRVWXY]'

    OUTWARD_PATTERNS = {
        'AN': A1+N,
        'ANN': A1+(N*2),
        'AAN': A1+A2+N,
        'ANA': A1+N+A3,
        'AANN': A1+A2+(N*2),
        'AANA': A1+A2+N+A4
    }
    INWARD_PATTERN = '[0-9][ABD-HJLNP-UW-Z]{2}'
    OUTWARD_PATTERN = '|'.join(list(OUTWARD_PATTERNS.values()))
    VALID_POSTCODE_PATTERN = r"^("+OUTWARD_PATTERN+")[ ]*("+INWARD_PATTERN+"$)"
    _inward = None
    _outward = None

    def __init__(self, post_code):
        if not isinstance(post_code, str):
            raise TypeError(
                'postcode should be instance of "str" but received a "{}"'.format(
                    type(post_code).__name__
                )
            )
        self.post_code = post_code

    def is_valid(self):
        if not self.post_code:
            return False

        regex_postcode = re.match(PostCodeUk.VALID_POSTCODE_PATTERN, self.post_code)
        if not regex_postcode:
            return False

        self._outward, self._inward = regex_postcode.groups()
        return True

    def get_outward(self):
        return self._outward if self.is_valid() else None

    def get_inward(self):
        return self._inward if self.is_valid() else None

    @staticmethod
    def random_postcode():
        pattern = r"^("+PostCodeUk.OUTWARD_PATTERN+")[ ]("+PostCodeUk.INWARD_PATTERN+"$)"
        return xeger(pattern)
