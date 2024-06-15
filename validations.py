import re


def validate_username(username):
    pattern = r"^(?!.*[_.]{2})[a-zA-Z_](?:[\w.\'-]{6,8})$"
    return bool(re.match(pattern, username))


def validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/]{12,30}$"
    return bool(re.match(pattern, password))


def validate_name(name):
    pattern = r"^[a-zA-Z]{2,20}$"
    return bool(re.match(pattern, name))


def validate_age(age):
    pattern = r"^(?:[1-9][0-9]?|100)$"
    return bool(re.match(pattern, age))


def validate_weight(weight):
    pattern = r"^(?:[1-9][0-9]?|1[0-9]{2}|200|201)$"  # 1-201 KG
    return bool(re.match(pattern, str(weight)))


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_phone_number(phone_number):
    pattern = r"^(?:\+?31|0)(?:[1-9][0-9]?|6[1-6])\d{7}$"  # Dutch phone number
    return bool(re.match(pattern, phone_number))


def validate_street_name(street_name):
    pattern = r"^[a-zA-Z0-9\s]{2,30}$"
    return bool(re.match(pattern, street_name))


def validate_house_number(house_number):
    pattern = r"^[1-9][0-9]{0,3}[a-zA-Z]{0,1}$"
    return bool(re.match(pattern, house_number))


def validate_zip_code(zip_code):
    pattern = r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$"
    return bool(re.match(pattern, zip_code))
