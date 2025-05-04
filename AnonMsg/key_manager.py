# user_app/utils.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from django.conf import settings

def aes_encrypt(data: str) -> tuple[bytes, bytes]:
    try:
        data = data.encode('utf-8')
        nonce = get_random_bytes(16)  # Generate a random nonce
        cipher = AES.new(settings.AES_SECRET_KEY, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        encrypted_data = ciphertext + tag  # Combine ciphertext and tag for storage
        return encrypted_data, nonce
    except (ValueError, UnicodeEncodeError) as e:
        raise ValueError(f"Encryption failed: {str(e)}")


def aes_decrypt(ciphertext: bytes, nonce: bytes) -> str:
    try:
        tag = ciphertext[-16:]  # Extract the last 16 bytes as the tag
        ciphertext = ciphertext[:-16]  # Remove the tag from the ciphertext
        cipher = AES.new(settings.AES_SECRET_KEY, AES.MODE_EAX, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode('utf-8')
    except (ValueError, UnicodeDecodeError) as e:
        raise ValueError(f"Decryption failed: {str(e)}")
