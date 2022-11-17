# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones

import os
import hashlib
from abc import ABC, abstractmethod
from .root import get_rootdir
from .file import get_file_handler


def dirtreestr(path, lvl: int = 0, indent: int = 4, maxdepth=None) -> str:
    vline = "│" + " " * (indent - 1)
    hline = "├" + "─" * (indent - 2) + " "
    name = os.path.split(path)[1]
    if lvl == 0:
        s = f"{name}\n"
    else:
        s = vline * (lvl - 1) + f"{hline}{name}\n"

    if os.path.isdir(path):
        if maxdepth is None or lvl < maxdepth:
            for name in os.listdir(path):
                new_path = os.path.join(path, name)
                s += dirtreestr(new_path, lvl + 1, indent, maxdepth)
    if lvl == 0:
        s = s.rstrip("\n")
    return s


class WorkingDirectory:
    def __init__(self, wd):
        self._old = os.getcwd()
        os.chdir(wd)

    def reset(self):
        os.chdir(self._old)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()


def string_key(*args, **kwargs):
    delim = "_"
    equal = "="
    s = delim.join(str(x) for x in args) if args else ""
    if kwargs:
        if s:
            s += delim
        s += delim.join(f"{k}{equal}{kwargs[k]}" for k in sorted(kwargs.keys()))
    return s


def hash_key(*args, method_="md5", **kwargs):
    delim = ""
    s = delim.join(str(x) for x in args) if args else ""
    if kwargs:
        keys = sorted(list(kwargs.keys()))
        s += delim + delim.join(f"{kwargs[k]}" for k in keys)

    h = hashlib.new(method_, s.encode())
    return str(h.hexdigest())


def argname(name, *args, method_="str", **kwargs):
    if "string".startswith(method_):
        k = string_key(*args, **kwargs)
    else:
        k = hash_key(*args, method_=method_, **kwargs)
    return f"{name}_{k}"


class RootDirectory:

    location = ""

    def __init__(self, name="", location=None, root=None, **kwargs):
        root = root if root is not None else get_rootdir()
        location = location if location is not None else self.location
        self.rootdir = os.path.join(root, location, name).format(**kwargs)
        self.name = os.path.split(self.rootdir)[1]

    @classmethod
    def fromargs(cls, name, *args, method_="md5", location=None, root=None, **kwargs):
        name = argname(name, *args, method_=method_, **kwargs)
        return cls(name, location, root, **kwargs)

    def exists(self, relpath=""):
        return os.path.exists(os.path.join(self.rootdir, relpath))

    def makedirs(self, relpath=""):
        path = os.path.join(self.rootdir, relpath)
        os.makedirs(path)

    def ensuredir(self, relpath=""):
        path = os.path.join(self.rootdir, relpath)
        if not os.path.exists(path):
            os.makedirs(path)

    def listdir(self, relpath=""):
        return os.listdir(os.path.join(self.rootdir, relpath))

    def walk(self, relpath=""):
        return os.walk(os.path.join(self.rootdir, relpath))

    def changedir(self, relpath=""):
        path = os.path.join(self.rootdir, relpath)
        if not os.path.exists(path):
            os.makedirs(path)
        return WorkingDirectory(path)

    def treestr(self, relpath="", indent=4, maxdepth=None):
        path = os.path.join(self.rootdir, relpath)
        return dirtreestr(path, indent=indent, maxdepth=maxdepth)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.rootdir})>"


class DataDirectory(RootDirectory, ABC):

    location = ""
    required = []

    def content_exists(self, overwrite=False):
        if overwrite:
            return False
        if not os.path.exists(self.rootdir):
            return False
        for relpath in self.required:
            if not os.path.exists(os.path.join(self.rootdir, relpath)):
                return False
        return True

    def save_file(self, relpath, *args, **kwargs):
        path = os.path.join(self.rootdir, relpath)
        file_handler = get_file_handler(path)
        file_handler.write(*args, **kwargs)

    def load_file(self, relpath):
        path = os.path.join(self.rootdir, relpath)
        file_handler = get_file_handler(path)
        return file_handler.read()

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def load(self):
        pass
