"""Implementation of class Card"""
from __future__ import annotations
from crypt_image import CryptImage
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
        raise NotImplementedError
        return ""

    @classmethod
    def create_from_path(cls, name:str, creator:str, path:str|PathLike, riddle:str, solution:str) -> Card:
        """"""
        pass

    def serialize(self) -> bytes:
        """"""
        pass
    
    @classmethod
    def deserialize(cls, data:bytes) -> Card:
        """"""
        pass