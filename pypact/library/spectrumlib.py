import json
import os

from ..util.exceptions import PypactSpectrumDoesNotExistException


_this_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
SPECTRUM_JSON_LIB_FILE = os.path.join(_this_dir, 'spectrumlib.min.json')


class SpectrumLibJSONReader:

    def __init__(self, filename=SPECTRUM_JSON_LIB_FILE):
        self.filename = filename

    def __enter__(self):
        data = {}
        with open(self.filename, 'rt') as f:
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
            raise PypactSpectrumDoesNotExistException(
                f"{name} does not exist in data")

        sdata = self._data[name]
        return sdata["energies"], sdata["values"]
