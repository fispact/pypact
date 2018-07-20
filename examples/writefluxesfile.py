import pypact as pp

filename = "fluxes"
# set monoenergetic flux at 14 MeV for group 709
desired_energy = 14.0e6
group = 709

# group structures are in reverse order
g = list(reversed(pp.ALL_GROUPS[group]))

# set your flux spectrum
energies = [(g[i] + g[i+1])/2.0 for i in range(0, group)]
flux     = [0.0]*group
for i in range(0, group):
    if g[i] > desired_energy:
        flux[i] = 1.0
        break

# write it afterwards
# looks illy looping twice but for complicated flux configuration it is cleaner to understand
# cost is nothing since list is tiny < 1000
with open(filename, 'wt') as f:
    for e in flux:
        f.write("{}\n".format(e))
    f.write("{}\n".format(1))
    f.write("Sample flux at 14MeV only")


