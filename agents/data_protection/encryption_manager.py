from fastapi import APIRouter
from cryptography.fernet import Fernet

router = APIRouter()

class EncryptionManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_data(self, data):
        encrypted_data = self.cipher.encrypt(data.encode())
        return {"encrypted_data": encrypted_data.decode()}

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher.decrypt(encrypted_data.encode())
        return {"decrypted_data": decrypted_data.decode()}

manager = EncryptionManager()

@router.post("/encrypt")
async def encrypt(data: str):
    return manager.encrypt_data(data)

@router.post("/decrypt")
async def decrypt(encrypted_data: str):
    return manager.decrypt_data(encrypted_data)