from abc import ABC, abstractmethod


class IEncryptor(ABC):
    @abstractmethod
    def encrypt(self, key: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, key: str) -> str:
        pass
