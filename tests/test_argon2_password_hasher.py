# from taskflow.password_hasher import PasswordHasher
from taskflow.argon2_password_hasher import Argon2PasswordHasher


def test_hash_and_verify_password() -> None:
    hasher = Argon2PasswordHasher()
    password = "TestPasswort123"
    password_hash = hasher.hash(password)
    assert hasher.verify(password, password_hash)


def test_rejects_wrong_password() -> None:
    hasher = Argon2PasswordHasher()
    password = "TestPasswort123"
    password_hash = hasher.hash(password)
    assert not hasher.verify("FalschesPasswort", password_hash)
