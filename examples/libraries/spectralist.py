import pypact as pp


with pp.SpectrumLibJSONReader() as lib:
    manager = pp.SpectrumLibManager(lib)
    for spectrum in manager.list():
        print(spectrum)
