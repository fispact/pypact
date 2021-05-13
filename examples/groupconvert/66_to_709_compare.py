import os
import math
import matplotlib.pyplot as plt
import pypact as pp

iflux = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fluxes66.in")

# convert to group 709 via energy
OUTPUT_GROUP = 709

iff = pp.ArbFluxesFile()
pp.from_file(iff, iflux)


def convert_flux(input_flux, group, by_energy=False):
    output_group_bounds = pp.ALL_GROUPS[-group]
    values = getattr(pp.groupconvert, "by_energy" if by_energy else "by_lethargy")(
        input_flux.boundaries, input_flux.values, output_group_bounds
    )
    output_flux = pp.FluxesFile()
    output_flux.setGroup(group)
    output_flux.values = values
    return output_flux


def getraw(fluxes):
    x = []
    y = []
    norm = 1.0 / sum(fluxes.values)
    for i in range(len(fluxes)):
        x.append(fluxes.boundaries[i])
        y.append(fluxes.values[i] * norm)
        x.append(fluxes.boundaries[i + 1])
        y.append(fluxes.values[i] * norm)
    return x, y


def getscaled(fluxes):
    # scale the values by bin width
    x = []
    y = []
    for i in range(len(fluxes)):
        scaledValue = fluxes.values[i] / (
            fluxes.boundaries[i + 1] - fluxes.boundaries[i]
        )
        x.append(fluxes.boundaries[i])
        y.append(scaledValue)
        x.append(fluxes.boundaries[i + 1])
        y.append(scaledValue)
    return x, y


def getbylethargy(fluxes):
    # scale the values by lethargy
    x = []
    y = []
    for i in range(len(fluxes)):
        scaledValue = lethargy = fluxes.values[i] / math.log(
            fluxes.boundaries[i + 1] / fluxes.boundaries[i]
        )
        x.append(fluxes.boundaries[i])
        y.append(scaledValue)
        x.append(fluxes.boundaries[i + 1])
        y.append(scaledValue)
    return x, y


off1 = convert_flux(iff, OUTPUT_GROUP, by_energy=False)
off2 = convert_flux(iff, OUTPUT_GROUP, by_energy=True)

FS = 18
f1 = plt.figure()
plt.loglog(*getraw(iff), "k", label="66")
plt.loglog(*getraw(off1), "r", label="709 (lethargy)")
plt.loglog(*getraw(off2), "g", label="709 (energy)")
plt.xlabel("Energy (eV)", fontsize=FS)
plt.ylabel("Normalised units", fontsize=FS)
plt.legend()

f2 = plt.figure()
plt.loglog(*getscaled(iff), "k", label="66")
plt.loglog(*getscaled(off1), "r", label="709 (lethargy)")
plt.loglog(*getscaled(off2), "g", label="709 (energy)")
plt.xlabel("Energy (eV)", fontsize=FS)
plt.ylabel("Normalised units per unit energy", fontsize=FS)
plt.legend()

f3 = plt.figure()
plt.loglog(*getbylethargy(iff), "k", label="66")
plt.loglog(*getbylethargy(off1), "r", label="709 (lethargy)")
plt.loglog(*getbylethargy(off2), "g", label="709 (energy)")
plt.xlabel("Energy (eV)", fontsize=FS)
plt.ylabel("Normalised units per unit lethargy", fontsize=FS)
plt.legend()

plt.show()
