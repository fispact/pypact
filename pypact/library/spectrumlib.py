import json
import os

from pypact.util.exceptions import PypactSpectrumDoesNotExistException
from pypact.library.groupstructures import ALL_GROUPS
import pypact.library.groupconvert as gc

_this_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
__SPECTRUM_JSON_LIB_FILE__ = os.path.join(_this_dir, "data", "spectrumlib.min.json")


class SpectrumLibJSONReader:
    def __init__(self, filename=__SPECTRUM_JSON_LIB_FILE__):
        self.filename = filename

    def __enter__(self):
        data = {}
        with open(self.filename, "rt") as f:
            data = json.load(f)

        return data

    def __exit__(self, *args):
        pass


class SpectrumLibManager:
    def __init__(self, data):
        self._data = data

    def list(self):
        return list(self._data.keys())

    def get(self, name):
        if name not in self._data:
            raise PypactSpectrumDoesNotExistException(f"{name} does not exist in data")

        sdata = self._data[name]
        return sdata["energies"], sdata["values"]

    def get_and_convert(self, name, group=709, method="by_lethargy"):
        if name not in self._data:
            raise PypactSpectrumDoesNotExistException(f"{name} does not exist in data")

        sdata = self._data[name]
        newenergies = ALL_GROUPS[-group]
        newvalues = getattr(gc, method)(sdata["energies"], sdata["values"], newenergies)
        return newenergies, newvalues
