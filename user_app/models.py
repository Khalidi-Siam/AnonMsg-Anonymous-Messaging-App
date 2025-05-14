from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from AnonMsg.key_manager import aes_encrypt, aes_decrypt

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username or not email:
            raise ValueError("Username and email are required")
        user = self.model(username=username)
        user.set_password(password) # Uses PBKDF2 with SHA256 with random salting by default
        user.set_email(email)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email_encrypted = models.BinaryField()
    email_nonce = models.BinaryField()
    is_active = models.BooleanField(default=True)
    profile_picture_encrypted = models.BinaryField(blank=True, null=True)
    profile_picture_nonce = models.BinaryField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()


    # AES encrypted email
    def set_email(self, email: str):
        ciphertext, nonce = aes_encrypt(email)
        self.email_encrypted = ciphertext
        self.email_nonce = nonce

    def get_email(self) -> str:
        decrypted = aes_decrypt(self.email_encrypted, self.email_nonce)
        if isinstance(decrypted, bytes):
            return decrypted.decode('utf-8')
        return decrypted

    # AES encrypted profile picture
    def set_profile_picture(self, image_bytes: bytes):
        ciphertext, nonce = aes_encrypt(image_bytes)
        self.profile_picture_encrypted = ciphertext
        self.profile_picture_nonce = nonce

    def get_profile_picture(self) -> bytes:
        if self.profile_picture_encrypted and self.profile_picture_nonce:
            data = aes_decrypt(self.profile_picture_encrypted, self.profile_picture_nonce)
            # If decryption returns str (from .decode('utf-8')), convert back to bytes for image
            if isinstance(data, str):
                # Most browsers expect image bytes, not base64-encoded or latin1-encoded strings
                # Try latin1 first (most likely for binary data stored as str)
                try:
                    return data.encode('latin1')
                except Exception:
                    return None
            return data
        return None

    def __str__(self):
        return self.username
