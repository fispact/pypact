import math
import matplotlib.pyplot as plt
import pypact as pp


# convert to a common group
compare_group = 709
common_energies = list(reversed(pp.ALL_GROUPS[compare_group]))


def plotbylethargy(energies, values, common_group=common_energies):
    # scale the values by lethargy
    newvalues = pp.groupconvert.by_lethargy(
        energies, values, common_group)
    x = []
    y = []
    for i, value in enumerate(newvalues):
        scaledValue = lethargy = value / \
            math.log(common_group[i+1]/common_group[i])
        x.append(common_group[i])
        y.append(scaledValue)
        x.append(common_group[i+1])
        y.append(scaledValue)
    return x, y


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


f1 = plt.figure()
with pp.SpectrumLibJSONReader() as lib:
    manager = pp.SpectrumLibManager(lib)
    cmap = get_cmap(len(manager.list()))
    for i, spectrum in enumerate(manager.list()):
        energies, values = manager.get(spectrum)
        x, y = plotbylethargy(energies, values)
        plt.loglog(x, y, cmap(i), label=spectrum)


plt.xlabel("Energy (eV)", fontsize=16)
plt.ylabel("Normalised units", fontsize=16)
# plt.legend()

plt.show()
