from abc import abstractmethod
from typing import List, IO, AnyStr

import utils


class Image:
    def __init__(self, endpoint, name, size, _hash):
        self._name = name
        self._size = size
        self._hash = _hash
        self.endpoint = endpoint

    def name(self):
        return self._name

    def size(self):
        return self._size

    def hash(self):
        return self._hash

    def size_str(self) -> str:
        return utils.size_str(self.size())

    def get_stream(self) -> IO[AnyStr]:
        return self.endpoint.get_image_stream(self)


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
