import re

from constants import Codes
from database import BlockedNumbers

PHONE_NUMBER_PATTERN_WITH_PLUS = re.compile('^[0-9\-\+]{11,15}$')
PHONE_NUMBER_PATTERN_WITH_MINUS = re.compile('^[0-9\-\+]{11,14}$')


class PhoneNumberAPIException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message
        super(PhoneNumberAPIException, self).__init__(error_message)

    def __str__(self):
        return f'Something is wrong with your data: {self.error_message}'


class PhoneNumberValidationError(PhoneNumberAPIException):
    pass


async def check_if_phone_number_exist_in_stop_list(phone_number: str) -> int:
    """Check if phone number is in stop list or not"""
    changed_number_may_be = check_if_phone_number_is_valid(phone_number)
    if not await BlockedNumbers.check_if_number_is_blocked(changed_number_may_be):
        return Codes.PHONE_NUMBER_IS_NOT_BLOCKED.value
    return Codes.PHONE_NUMBER_IS_BLOCKED.value


def check_if_phone_number_is_valid(phone_number: str) -> str:
    """Check if phone number is valid to process further"""
    pattern = PHONE_NUMBER_PATTERN_WITH_MINUS if phone_number[0] == '+' else PHONE_NUMBER_PATTERN_WITH_MINUS
    if not pattern.match(phone_number):
        raise PhoneNumberValidationError('Phone number is not correct')
    return phone_number[1:] if phone_number[0] == '+' else phone_number  # Deleting + if it exists in number because in
    # db we dont have them
