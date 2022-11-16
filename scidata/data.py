# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones

import os
from abc import ABC, abstractmethod
from .root import get_rootdir
from .file import get_file_handler


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


class RootDirectory:

    location = ""

    def __init__(self, name="", location=None, root=None, **kwargs):
        root = root if root is not None else get_rootdir()
        location = location if location is not None else self.location
        self.rootdir = os.path.join(root, location, name).format(**kwargs)
        self.name = os.path.split(self.rootdir)[1]

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

    def workingdir(self, relpath=""):
        path = os.path.join(self.rootdir, relpath)
        if not os.path.exists(path):
            os.makedirs(path)
        return WorkingDirectory(path)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.rootdir})>"


class DataDirectory(RootDirectory, ABC):

    location = ""
    required = []

    def __init__(self, name="", location=None, root=None, **kwargs):
        super().__init__(name, location, root, **kwargs)

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
