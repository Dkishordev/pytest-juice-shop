import random
import string


def random_email():
    letters = ''.join(random.choices(string.ascii_lowercase, k=8))
    return "sectest_" + letters + "@example.com"



def random_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=8))
    return "P@ss" + password


def random_string(length=10):
    letters = ''.join(random.choices(string.ascii_letters, k=length))
    return letters


