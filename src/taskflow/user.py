from uuid import UUID, uuid4

from taskflow.exceptions import InvalidEmailError, InvalidPasswordError


class User:
    def __init__(
        self,
        email: str,
        password_hash: str,
        user_id: UUID | None = None,
    ) -> None:
        cleaned_email = email.strip().lower()
        if not cleaned_email:
            raise InvalidEmailError("Die E-Mail-Adresse darf nicht leer sein.")
        self.id = user_id or uuid4()
        self.email = cleaned_email
        cleaned_password_hash = password_hash.strip()
        if not cleaned_password_hash:
            raise InvalidPasswordError("Der Passwort-Hash darf nicht leer sein.")
        self.password_hash = cleaned_password_hash
