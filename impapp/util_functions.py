__author__ = 'Abdul'
from django.core.validators import validate_email as v_email, URLValidator
from django.core.exceptions import ValidationError


def check_email(email):
    try:
        v_email(email)
        return True
    except:
        return False


def validate_age(age):
    try:
        age = int(age)
        return 18 <= age < 100
    except Exception:
        return False

def validate_url(url):
    try:
        validate = URLValidator()
        validate(url)
        return True
    except ValidationError:
        return False


def validate_float(num):
    try:
        num = float(num)
        return 0 < num <= 5
    except Exception:
        return False