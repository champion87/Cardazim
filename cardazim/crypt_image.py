"""Implementation of the CrypteImage module."""
from __future__ import annotations
from os import PathLike
from PIL import Image
from Crypto.Cipher import AES
from io import BytesIO
import hashlib
from enum import Enum
import struct

class CryptoAction(Enum):
    ENCRYPT = 1
    DECRYPT = 2

def double_hash(key:str) -> bytes:
    key_bytes = key.encode("utf-8")
    first_hash_object = hashlib.sha256(key_bytes)
    first_hash = first_hash_object.digest()
    second_hash_object = hashlib.sha256(first_hash)
    return second_hash_object.digest()

def perform_crypto_on_image(key_hash:bytes, image:Image, action:CryptoAction) -> Image:
    cipher = AES.new(key_hash, AES.MODE_EAX, nonce=b'arazim')
    size, mode = image.size, image.mode
    data = image.tobytes()

    proccessed = b""
    if action == CryptoAction.DECRYPT:
        proccessed = cipher.encrypt(data)
    if action == CryptoAction.ENCRYPT:
        proccessed = cipher.decrypt(data)

    return Image.frombytes(mode, size, proccessed)


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

    def serialize(self):
        """
        Serializes the image data into a byte sequence.

        The serialized data format:
        - Image height (4 bytes)
        - Image width (4 bytes)
        - Pixel data (h * w * 3 bytes for RGB mode)
        - Key hash (32 bytes)
        """
        # Extract the image data
        width, height = self.image.size
        pixel_data = self.image.tobytes()

        # Serialize the image data
        data = struct.pack("II", height, width) + pixel_data + self.key_hash
        return data

    @classmethod
    def create_from_bytes(cls, data:bytes):
        """
        The serialized data format:
        - Image height (4 bytes)
        - Image width (4 bytes)
        - Pixel data (h * w * 3 bytes for RGB mode)
        - Key hash (32 bytes)

        :return: The created Image, and the amount of bytes used.
        """
        # First, unpack the height and width of the image
        height, width = struct.unpack("II", data[:8])

        # Calculate pixel data size for RGB (3 bytes per pixel)
        pixel_data_size = height * width * 3
        pixel_data_start = 8
        pixel_data_end = pixel_data_start + pixel_data_size
        pixel_data = data[pixel_data_start:pixel_data_end]

         # Reconstruct the image using PIL
        image = Image.frombytes("RGB", (width, height), pixel_data)

        # Extract the key hash (32 bytes)
        key_hash_start = pixel_data_end
        key_hash_end = key_hash_start + 32
        key_hash = data[key_hash_start:key_hash_end]

        total_data_len = key_hash_end

        return cls(image, key_hash), total_data_len

    def encrypt(self, key:str) -> None:
        """Encrypts the binary data of the image using AES over the hash of the given key."""
        self.key_hash = double_hash(key)
        encrypted = perform_crypto_on_image(self.key_hash, self.image, CryptoAction.ENCRYPT)
        self.image = encrypted
        

    def decrypt(self, key:str) -> bool:
        """Decrypts the binary of the image with the given key's hash."""
        if self.key_hash != double_hash(key):
            return False
        
        decrypted = perform_crypto_on_image(self.key_hash, self.image, CryptoAction.DECRYPT)
        self.image = decrypted
        return True

    
