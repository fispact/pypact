import math
import matplotlib.pyplot as plt
import pypact as pp


name_spectrum1 = '1102_PWR-UO2-0'
name_spectrum2 = '1102_PWR-UO2-15'
name_spectrum3 = '1102_PWR-UO2-40'

# convert to a common group
compare_group = 709
common_energies = list(reversed(pp.ALL_GROUPS[compare_group]))

energies1, values1 = None, None
energies2, values2 = None, None
energies3, values3 = None, None

with pp.SpectrumLibJSONReader() as lib:
    manager = pp.SpectrumLibManager(lib)
    energies1, values1 = manager.get(name_spectrum1)
    energies2, values2 = manager.get(name_spectrum2)
    energies3, values3 = manager.get(name_spectrum3)


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
x3, y3 = plotbylethargy(energies3, values3)

f1 = plt.figure()
plt.loglog(x1, y1, 'k', label=name_spectrum1)
plt.loglog(x2, y2, 'r', label=name_spectrum2)
plt.loglog(x3, y3, 'g', label=name_spectrum3)
plt.xlabel("Energy (eV)", fontsize=16)
plt.ylabel("Normalised units", fontsize=16)
plt.legend()

plt.show()
