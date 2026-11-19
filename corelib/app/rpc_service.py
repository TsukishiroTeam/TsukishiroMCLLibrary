import socket
import ctypes
from io import TextIOWrapper
from abc import ABC, abstractmethod

class PipeWrapper:
    def __init__():
        pass

class RpcBase(ABC):
    @abstractmethod
    def __init__(self, process_id: int):
        pass
    @abstractmethod
    def listen():
        pass
    @abstractmethod
    def read():
        pass
    @abstractmethod
    def write():
        pass

class RpcServer(RpcBase):
    def __init__(self, process_id: int):
        pass


class RpcClient(RpcBase):
    pass
