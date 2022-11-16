# SciData

> Python framework for storing scientific data in a directory structure

## Usage

### Simple data storage

````python
from scidata import set_rootdir, DataDirectory

set_rootdir("data")  # this is the default, change as you like


class DataDir(DataDirectory):

    location = "test_data"

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
