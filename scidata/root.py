# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones

import os

_DATA_DIR = "data"
_FIGS_DIR = os.path.join(_DATA_DIR, "figs")


def set_rootdir(path):
    global _DATA_DIR
    _DATA_DIR = path


def get_rootdir():
    return _DATA_DIR


def set_figdir(path):
    global _FIGS_DIR
    _FIGS_DIR = path


def get_figdir():
    return _FIGS_DIR
