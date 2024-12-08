"""Implementation of class Card"""
from __future__ import annotations
from crypt_image import CryptImage
import struct
from os import PathLike

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
        name_len = len(self.name)
        creator_len = len(self.creator)
        w,h = self.image.image.size
        len_of_riddle = len(self.riddle)
        return struct.pack(
            f"I{name_len}sI{creator_len}sII{h*w*3}s32sI{len_of_riddle}s",
            name_len,
            self.name.encode("utf-8"),
            creator_len,
            self.creator.encode("utf-8"),
            h,
            w,
            self.image.image.tobytes(),
            self.image.key_hash,
            len_of_riddle,
            self.riddle.encode("utf-8")
        )
    
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
        # Extract the name length
        name_length_start = 0
        name_length_end = name_length_start + 4
        (name_length,) = struct.unpack("I", data[name_length_start:name_length_end])

        # Extract the name string
        name_start = name_length_end
        name_end = name_start + name_length
        name = data[name_start:name_end].decode("utf-8")

        # Extract the creator length
        creator_length_start = name_end
        creator_length_end = creator_length_start + 4
        (creator_length,) = struct.unpack("I", data[creator_length_start:creator_length_end])

        # Extract the creator string
        creator_start = creator_length_end
        creator_end = creator_start + creator_length

        print(f"Name length: {name_length}")
        print(f"Name slice: {name_start} {name_end}")
        print(f"Creator length: {creator_length}")
        print(f"Creator slice: {creator_start} {creator_end}")

        creator = data[creator_start:creator_end].decode("utf-8")

        image, image_data_len = CryptImage.create_from_bytes(data[creator_end:])
        riddle_length_start = creator_end + image_data_len
        # Extract the riddle length
        riddle_length_end = riddle_length_start + 4
        (riddle_length,) = struct.unpack("I", data[riddle_length_start:riddle_length_end])

        # Extract the riddle string
        riddle_start = riddle_length_end
        riddle_end = riddle_start + riddle_length
        riddle = data[riddle_start:riddle_end].decode("utf-8")

    

        # Return the reconstructed Card instance
        return cls(name, creator, image, riddle, None)