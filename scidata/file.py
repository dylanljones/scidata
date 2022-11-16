# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones

import json
import pickle
from abc import ABC, abstractmethod
import numpy as np

_FILE_HANDLERS = dict()


# noinspection PyUnusedLocal
class FileHandler(ABC):
    def __init__(self, path, *args, **kwargs):
        self.path = path

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, *args, **kwargs):
        pass


def register_file_handler(ext, handler):
    global _FILE_HANDLERS
    _FILE_HANDLERS[ext] = handler


def unregister_file_handler(ext):
    global _FILE_HANDLERS
    del _FILE_HANDLERS[ext]


def get_file_handler(path, *args, **kwargs) -> FileHandler:
    ext = "." + path.split(".")[-1]
    handler = _FILE_HANDLERS[ext]
    return handler(path, *args, **kwargs)


class Text(FileHandler):
    def read(self):
        with open(self.path, "r") as fh:
            data = fh.read()
        return data

    def write(self, data):
        with open(self.path, "w") as fh:
            fh.write(data)


class Binary(FileHandler):
    def read(self):
        with open(self.path, "rb") as fh:
            data = fh.read()
        return data

    def write(self, data):
        with open(self.path, "wb") as fh:
            fh.write(data)


class Json(FileHandler):
    def read(self):
        with open(self.path, "r") as fh:
            data = json.load(fh)
        return data

    def write(self, data):
        with open(self.path, "w") as fh:
            json.dump(data, fh)


class Pickle(FileHandler):
    def read(self):
        with open(self.path, "rb") as fh:
            data = pickle.load(fh)
        return data

    def write(self, data):
        with open(self.path, "wb") as fh:
            pickle.dump(data, fh)


class Npz(FileHandler):
    def read(self):
        return np.load(self.path)

    def write(self, *args, **kwargs):
        np.savez(self.path, *args, **kwargs)


# Register default file handlers
register_file_handler(".txt", Text)
register_file_handler(".json", Json)
register_file_handler(".npz", Npz)
register_file_handler(".pkl", Pickle)
