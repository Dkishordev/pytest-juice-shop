import random
import string
from faker import Faker

fake = Faker()


def random_email() -> str:
    return f"sectest_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"


def random_password() -> str:
    return "P@ss" + "".join(random.choices(string.ascii_letters + string.digits, k=8))


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


