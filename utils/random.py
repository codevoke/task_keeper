import random
import string


def make_code() -> str:
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
