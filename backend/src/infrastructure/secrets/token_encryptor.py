from cryptography.fernet import Fernet
from settings import settings

from src.core.interfaces.secrets.i_encryptor import IEncryptor


class Encryptor(IEncryptor):
    def __init__(self, key: str):
        self.fernet = Fernet(key)

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode()).decode()


encryptor = Encryptor(settings.app.SECRET_KEY)
