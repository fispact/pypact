import math
import matplotlib.pyplot as plt
import pypact as pp


name_spectrum1 = '1102_PWR-MOX-40'
name_spectrum2 = '616_HCLL-FW'

# convert to a common group
compare_group = 709
common_energies = list(reversed(pp.ALL_GROUPS[compare_group]))

energies1, values1 = None, None
energies2, values2 = None, None

with pp.SpectrumLibJSONReader() as lib:
    manager = pp.SpectrumLibManager(lib)
    energies1, values1 = manager.get(name_spectrum1)
    energies2, values2 = manager.get(name_spectrum2)


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


x1, y1 = plotbylethargy(energies1, values1)
x2, y2 = plotbylethargy(energies2, values2)

f1 = plt.figure()
plt.loglog(x1, y1, 'k', label=name_spectrum1)
plt.loglog(x2, y2, 'r', label=name_spectrum2)
plt.xlabel("Energy (eV)", fontsize=16)
plt.ylabel("Normalised units", fontsize=16)
plt.legend()

plt.show()
