# SciData

> Python framework for storing scientific data in a directory structure

## Usage

### Global data root

Set global root directory for saving and loading data. By default,
the sub-directory ``data/`` is used
````python
from scidata import set_rootdir

set_rootdir("data2")
````

### Simple data storage

````python
from scidata import DataDirectory

class DataDir(DataDirectory):

    location = "test_data"
    required = ["data.npz"]

    def save(self, x, y):
        self.ensuredir()
        self.save_file("data.npz", x=x, y=y)

    def load(self):
        data = self.load_file("data.npz")
        return data["x"], data["y"]
````

Path of directory is constructed according to class attribbutes and arguments
````python
>>> d = DataDir("test1")
>>> d.path
data/test_data/test1
````

Save data:
````python
>>> x = np.linspace(-5, +5, 1000)
>>> y = np.sin(x)
>>> d.save(x, y)
````

List files:
````python
>>> list(d.listdir())
["data.npz"]
````

Load data:
````python
>>> x, y = d.load()
````

### Datasets

In contrast to the ``DataDirectory`` object, ``Dataset`` instances store the state of
the values:

````python
from scidata import Dataset

class Dset(Dataset):

    location = "tests"
    required = ["data.npz"]

    def __init__(self, name=""):
        super().__init__(name)
        self.x = None
        self.y = None

    def save(self):
        self.ensuredir()
        self.save_file("data.npz", x=self.x, y=self.y)

    def load(self):
        data = self.load_file("data.npz")
        self.x, self.y = data["x"], data["y"]

    def set(self, x, y):
        self.x = x
        self.y = y

    def plot(self, ax):
        ax.plot(self.x, self.y)
````

Set and save data:
````python
>>> d = Dset("test2")
>>> x = np.linspace(-5, +5, 1000)
>>> y = np.sin(x)
>>> d.set(x, y)
>>> d.save()
````

List files:
````python
>>> list(d.listdir())
["data.npz"]
````

Load and access data:
````python
>>> d.load()
>>> d.x.shape
(1000,)
````

### Registering custom file handlers


````python
from scidata import FileHandler, register_file_handler

class CustomFileHandler(FileHandler):

    def read(self):
        with open(self.path, "r") as fh:
            data = fh.read()
        return data

    def write(self, data):
        with open(self.path, "w") as fh:
            fh.write(data)

register_file_handler(".dat", CustomFileHandler)
````
