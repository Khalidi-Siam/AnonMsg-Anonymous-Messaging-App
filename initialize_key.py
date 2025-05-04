# key_manager.py
import os
import base64
from django.conf import settings
from Crypto.Random import get_random_bytes

ENV_VAR_NAME = "AES_SECRET_KEY"

def generate_key():
    """
    Generates a secure 32-byte AES key (for AES-256).
    Returns base64-encoded string for safe .env usage.
    """
    key = get_random_bytes(32)
    return base64.b64encode(key).decode('utf-8')


def write_key_to_env(env_file_path=".env"):
    """
    Writes a freshly generated key to the .env file.
    Only run this ONCE during setup.
    """
    key = generate_key()

    # Prevent duplicate key
    with open(env_file_path, 'r') as f:
        lines = f.readlines()
    if any(ENV_VAR_NAME in line for line in lines):
        raise Exception(f"{ENV_VAR_NAME} already exists in .env")

    with open(env_file_path, 'a') as f:
        f.write(f"\n{ENV_VAR_NAME}={key}\n")

    print(f"{ENV_VAR_NAME} written to .env")


def get_key():
    """
    Retrieves and decodes the base64-encoded key from settings.py
    """
    key_b64 = getattr(settings, ENV_VAR_NAME, None)
    if key_b64 is None:
        raise ValueError("AES key not found in settings.")

    try:
        return base64.b64decode(key_b64)
    except Exception:
        raise ValueError("AES key in settings is not valid base64.")


if __name__ == "__main__":
    # This is just for demonstration purposes. In a real application, you would not run this directly.
    write_key_to_env()
    print("Key generation complete. Please restart your server.")


# AES_SECRET_KEY=JTCqiJfyteq13c7kQD10ib528DGkLSNF+4VRHm7TMP4=