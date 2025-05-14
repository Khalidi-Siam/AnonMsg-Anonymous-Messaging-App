from django.db import models
from AnonMsg.key_manager import aes_encrypt, aes_decrypt
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    encrypted_content = models.BinaryField()
    nonce = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def encrypt_content(self, content: str):
        ciphertext, nonce = aes_encrypt(content)
        self.encrypted_content = ciphertext
        self.nonce = nonce

    def decrypt_content(self) -> str:
        decrypted = aes_decrypt(self.encrypted_content, self.nonce)
        # Make sure we always return a string, not bytes
        if isinstance(decrypted, bytes):
            return decrypted.decode('utf-8')
        return decrypted