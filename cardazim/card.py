"""Implementation of class Card"""
from __future__ import annotations
from crypt_image import CryptImage
import struct
from os import PathLike

def round_up_to_multiple(n: int, multiple: int) -> int:
    """
    Rounds up the given number to the nearest multiple of the specified value.

    :param n: The number to be rounded up.
    :type n: int
    :param multiple: The multiple to which the number should be rounded up.
    :type multiple: int
    :return: The rounded up number.
    :rtype: int
    """
    return n + multiple - 1 - (n - 1) % multiple

def pack_str(s: str) -> bytes:
    return struct.pack(f"I{len(s)}s", len(s), s.encode("utf-8"))

def unpack_str(data: bytes) -> tuple[bytes, str]:
    """
    Unpacks a byte sequence into a tuple containing the remaining bytes and a decoded string.

    :param data: The byte sequence to unpack. The first 4 bytes represent the length of the string.
    :return: A tuple where the first element is the remaining bytes after the string, and the second element is the decoded string.
    """
    (length,) = struct.unpack("I", data[:4])

    return data[4 + round_up_to_multiple(4, length):], data[4:4 + length].decode("utf-8")

class Card:
    "a class representing a card with image and a riddle."
    def __init__(self, name:str, creator:str, image:CryptImage, riddle:str, solution:str|None):
        self.name:str = name
        self.creator:str = creator
        self.image:CryptImage = image
        self.riddle:str = riddle
        self.solution:str|None = solution

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name}, creator={self.creator}>"

    def __str__(self) -> str:
        solution_status = self.solution if self.solution else "unsolved"
        return (
            f"{self.__class__.__name__} {self.name} by {self.creator}\n"
            f"  Riddle: {self.riddle}\n"
            f"  Solution: {solution_status}"
        )

    @classmethod
    def create_from_path(cls, name:str, creator:str, path:str|PathLike, riddle:str, solution:str) -> Card:
        """"""
        return cls(name, creator, CryptImage.create_from_path(path), riddle, solution)
        
    def serialize(self) -> bytes:
        """"""
        res = pack_str(self.name) + pack_str(self.creator) + self.image.serialize() + pack_str(self.riddle)
        return res
    
    @classmethod
    def deserialize(cls, data: bytes) -> Card:
        """
        Deserializes the provided bytes into a Card instance.

        The serialized data format:
        - Image height (4 bytes)
        - Image width (4 bytes)
        - Pixel data (h * w * 3 bytes for RGB mode)
        - Key hash (32 bytes)
        - Riddle length (4 bytes)
        - Riddle (UTF-8 encoded string)

        :param data: The serialized data.
        :type data: bytes
        :return: The deserialized Card instance.
        :rtype: Card
        """
        def extract_string(data: bytes, start: int) -> tuple[str, int]:
            length = struct.unpack("I", data[start:start + 4])[0]
            end = start + 4 + length
            return data[start + 4:end].decode("utf-8"), end

        name, name_end = extract_string(data, 0)
        creator, creator_end = extract_string(data, name_end)

        image, image_data_len = CryptImage.create_from_bytes(data[creator_end:])
        riddle, _ = extract_string(data, creator_end + image_data_len)

        return cls(name, creator, image, riddle, None)