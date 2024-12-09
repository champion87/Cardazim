"""Implementation of the CrypteImage module."""

from __future__ import annotations

import hashlib
import struct
from enum import Enum
from os import PathLike

from Crypto.Cipher import AES
from PIL import Image


class CryptoAction(Enum):
    """An enumeration representing the action to perform on the image."""

    ENCRYPT = 1
    DECRYPT = 2


def double_hash(key: str) -> bytes:
    """
    Generates a double SHA-256 hash of the given key.

    :param key: The key to hash.
    :return: The double hashed key as bytes.
    """
    key_bytes = key.encode("utf-8")
    first_hash_object = hashlib.sha256(key_bytes)
    first_hash = first_hash_object.digest()
    second_hash_object = hashlib.sha256(first_hash)
    return second_hash_object.digest()


def perform_crypto_on_image(
    key_hash: bytes, image: Image, action: CryptoAction
) -> Image:
    """
    Performs encryption or decryption on the given image using the provided key hash.

    :param key_hash: The hash of the key to use for encryption/decryption.
    :param image: The image to encrypt/decrypt.
    :param action: The action to perform (CryptoAction.ENCRYPT or CryptoAction.DECRYPT).
    :return: The processed image.
    """
    cipher = AES.new(key_hash, AES.MODE_EAX, nonce=b"arazim")
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

    def __init__(self, image: Image, key_hash: bytes | None):
        """
        Initializes the CryptImage instance.

        :param image: The image to be encrypted/decrypted.
        :param key_hash: The hash of the key used for encryption/decryption.
        """
        self.image: Image = image
        self.key_hash: bytes | None = key_hash

    @classmethod
    def create_from_path(cls, path: str | PathLike) -> CryptImage:
        """
        Loads an image from a given path.

        :param path: The path to the image file.
        :return: An instance of CryptImage.
        """
        image = Image.open(path)
        return cls(image, None)

    def serialize(self) -> bytes:
        """
        Serializes the image data into a byte sequence.

        The serialized data format:
        - Image height (4 bytes)
        - Image width (4 bytes)
        - Pixel data (h * w * 3 bytes for RGB mode)
        - Key hash (32 bytes)

        :return: The serialized byte sequence.
        """
        # Extract the image data
        width, height = self.image.size
        pixel_data = self.image.tobytes()

        # Serialize the image data
        key_hash = self.key_hash if self.key_hash else b"\x00" * 32
        data = struct.pack("II", height, width) + pixel_data + key_hash
        return data

    @classmethod
    def create_from_bytes(cls, data: bytes) -> tuple[CryptImage, int]:
        """
        Creates a CryptImage instance from a byte sequence.

        The serialized data format:
        - Image height (4 bytes)
        - Image width (4 bytes)
        - Pixel data (h * w * 3 bytes for RGB mode)
        - Key hash (32 bytes)

        :param data: The byte sequence to deserialize.
        :return: A tuple containing the created CryptImage instance and the number of bytes used.
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

    def encrypt(self, key: str) -> None:
        """
        Encrypts the binary data of the image using AES over the hash of the given key.

        :param key: The key to use for encryption.
        """
        self.key_hash = double_hash(key)
        encrypted = perform_crypto_on_image(
            self.key_hash, self.image, CryptoAction.ENCRYPT
        )
        self.image = encrypted

    def decrypt(self, key: str) -> bool:
        """
        Decrypts the binary of the image with the given key's hash.

        :param key: The key to use for decryption.
        :return: True if decryption was successful, False otherwise.
        """
        if self.key_hash != double_hash(key):
            return False

        decrypted = perform_crypto_on_image(
            self.key_hash, self.image, CryptoAction.DECRYPT
        )
        self.image = decrypted
        return True
