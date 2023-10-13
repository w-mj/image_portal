from abc import abstractmethod
from typing import List, IO, AnyStr


class Image:
    def __init__(self, name, size, _hash):
        self._name = name
        self._size = size
        self._hash = _hash

    def name(self):
        return self._name

    def size(self):
        return self._size

    def hash(self):
        return self._hash


class Endpoint:
    def __init__(self, _type, _addr, _user, _pass):
        self.type = _type

    @abstractmethod
    def get_images(self) -> List[Image]:
        pass

    @abstractmethod
    def get_image_stream(self, image: Image) -> IO[AnyStr]:
        pass

    @abstractmethod
    def create_image_stream(self, image: Image) -> IO[AnyStr]:
        pass

    @abstractmethod
    def error(self) -> str:
        pass
