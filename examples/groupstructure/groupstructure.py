import matplotlib.pyplot as plt
import math
import numpy as np
import pypact as pp

logX = True

# Energy range upto 1 GeV
erange = np.linspace(0, 1e9, 1000)
if logX:
    erange = np.logspace(-5, 9, 1000)
    
# cumulative plot    
COLORS = ['k:', 'r:', 'b:', 'm:', 'c:', 'y:', 'g:', 'm', 'c', 'y','k', 'r', 'b', 'g' ]
_ = plt.figure()
ascendinggroups = [(-k, v) for k, v in pp.ALL_GROUPS.items() if k < 0]
for i, (group, renergies) in enumerate(ascendinggroups):
    cumulative = []
    energies = list(reversed(renergies))
    for x in erange:
        count = np.count_nonzero(energies < x)
        cumulative.append(count)
    if logX:
        plt.loglog(erange, cumulative, COLORS[i%len(COLORS)], label=str(group))
    else:
        plt.semilogy(erange, cumulative, COLORS[i%len(COLORS)], label=str(group))

# line markers
plt.axvline(x=1, color='r', linewidth=2)
plt.text(1, 1.3e3, "eV", color='r', rotation=90)
plt.axvline(x=1e3, color='r', linewidth=2)
plt.text(1e3, 1.3e3, "keV", color='r', rotation=90)
plt.axvline(x=1e6, color='r', linewidth=2)
plt.text(1e6, 1.3e3, "MeV", color='r', rotation=90)
plt.axvline(x=2e7, color='r', linewidth=1)
plt.text(2e7, 1.3e3, "20 MeV", color='r', rotation=90)
plt.axvline(x=1e9, color='r', linewidth=2)
plt.text(1e9, 1.3e3, "GeV", color='r', rotation=90)

plt.xlabel("Energy (eV)", fontsize=16)
plt.ylabel("Cumulative count", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.legend()

plt.show()