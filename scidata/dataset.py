# coding: utf-8
#
# This code is part of scidata.
#
# Copyright (c) 2022, Dylan Jones

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from .data import DataDirectory


class Dataset(DataDirectory, ABC):
    def __init__(self, name, location=None, root=None, **kwargs):
        DataDirectory.__init__(self, name, location, root, **kwargs)
        self.info = dict()

    @abstractmethod
    def set(self, *args, **kwargs):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

    def save_info(self):
        self.save_file("info.json", self.info)

    def load_info(self):
        self.info = dict(self.load_file("info.json"))

    def subplots(self):
        return plt.subplots()

    def plot(self, ax: plt.Axes):
        pass

    def plot_data(self):
        fig, ax = self.subplots()
        self.plot(ax)
        return fig, ax
