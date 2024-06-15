from sqlite3 import Connection
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


class Config:
    def __init__(
        self, con: Connection, public_key: RSAPublicKey, private_key: RSAPrivateKey
    ):
        self.con = con
        self.con.execute("PRAGMA foreign_keys = ON;")
        self.con.commit()

        self.public_key = public_key
        self.private_key = private_key
