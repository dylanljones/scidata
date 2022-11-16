# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones


_ROOT_DIR = "data"


def set_rootdir(path):
    global _ROOT_DIR
    _ROOT_DIR = path


def get_rootdir():
    return _ROOT_DIR
