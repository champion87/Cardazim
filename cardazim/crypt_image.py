"""Implementation of the CrypteImage module."""
from __future__ import annotations
from os import PathLike
from PIL import Image
from Crypto.Cipher import AES
from io import BytesIO
import hashlib

class CryptImage:
    """Class for CryptImage."""
    def __init__(self, image:Image, key_hash:bytes|None):
        self.image:Image = image
        self.key_hash:bytes|None = key_hash

    @classmethod
    def create_from_path(cls, path:str|PathLike) -> CryptImage:
        """Loads an image from a given path."""
        image = Image.open(path)
        return cls(image, None)

    def encrypt(self, key:str) -> None:
        """Encrypts the binary data of the image using AES over the hash of the given key."""
        ### Update key hash ###
        key_bytes = key.encode("utf-8")
        first_hash_object = hashlib.sha256(key_bytes)
        first_hash = first_hash_object.digest()
        second_hash_object = hashlib.sha256(first_hash)
        second_hash = second_hash_object.digest()
        self.key_hash = second_hash

        ### Encrypt the image with the updated key_hash ##
        plaintext, size, mode = self._get_image_in_bytes()
        cipher = AES.new(self.key_hash, AES.MODE_EAX, nonce=b'arazim')
        # encrypted = cipher.encrypt(plaintext)
        # encrypted = plaintext
        self.image = Image.frombytes(mode, size, encrypted)

    def _get_image_in_bytes(self) -> bytes:
        with BytesIO() as byte_io:
            self.image.save(byte_io, format='PNG')  # Save image as PNG or any other format
            return byte_io.getvalue(), self.image.size, self.image.mode

    def decrypt(self, key:str) -> bool:
        """Decrypts the binary of the image with the given key's hash."""

    
