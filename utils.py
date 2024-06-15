from datetime import datetime
from random import randint
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


def load_private_key():
    try:
        with open("keys/private.pem", "rb") as key_file:
            return serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
    except FileNotFoundError:
        return None


def load_public_key():
    try:
        with open("keys/public.pem", "rb") as key_file:
            return serialization.load_pem_public_key(
                key_file.read(),
            )
    except FileNotFoundError:
        return None


def rsa_encrypt(message: str, public_key: RSAPublicKey) -> bytes:
    return public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(ciphertext: bytes, private_key: RSAPrivateKey) -> str:
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    ).decode()


def generate_registration_date() -> str:
    return str(datetime.now().date())


def generate_membership_id(self, registration_date: str) -> str:
    initial = registration_date[2:4]
    random_digits = "".join([str(randint(0, 9)) for _ in range(7)])
    membership_id = f"{initial}{random_digits}"
    checksum = sum(int(digit) for digit in membership_id) % 10
    return f"{membership_id}{checksum}"
