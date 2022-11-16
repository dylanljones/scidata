# SciData

> Python framework for storing scientific data in a directory structure

## Usage

### Simple data storage

````python
from scidata import set_rootdir, DataDirectory

# Set global root directory
# by default, 'data' is used as data directory
set_rootdir("data")

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
