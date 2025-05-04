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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()


    # AES encrypted email
    def set_email(self, email: str):
        ciphertext, nonce = aes_encrypt(email)
        self.email_encrypted = ciphertext
        self.email_nonce = nonce

    def get_email(self) -> str:
        return aes_decrypt(self.email_encrypted, self.email_nonce)    

    def __str__(self):
        return self.username
