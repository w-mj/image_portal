import subprocess
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


class HostItem:
    def __init__(self, d=None):
        if d is None:
            d = dict()
        self.data = d

    def get_name(self):
        return self.data.get("name", self.data.get("addr", "unnamed"))

    def get(self, key):
        return self.data.get(key, "")

    def set(self, key, value):
        self.data[key] = value

    def get_type(self):
        return self.get("type")

    def get_user(self):
        return self.get("user")

    def get_pass(self):
        return self.get("pass")

    def get_addr(self):
        return self.get("addr")


class Endpoint:
    def __init__(self, host: HostItem):
        pass

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
