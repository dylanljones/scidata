# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones

from .root import set_rootdir, get_rootdir, set_figdir, get_figdir
from .file import (
    FileHandler,
    register_file_handler,
    unregister_file_handler,
    get_file_handler,
)
from .data import DataDirectory, get_data_objects
from .dataset import Dataset
