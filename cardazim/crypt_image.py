"""Implementation of the CrypteImage module."""
from __future__ import annotations
from os import PathLike
import hashlib
from Crypto.Cipher import AES
from PIL import Image

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

    def decrypt(self, key:str) -> bool:
        """Decrypts the binary of the image with the given key's hash."""

    
