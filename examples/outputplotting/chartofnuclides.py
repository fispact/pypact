import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
import pypact as pp


FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'reference', 'AlVC.json')

PROPERTY = 'atoms'
MIN_VALUE = 1e2
MAX_VALUE = 1e22
Z_RANGE = [0, 30]
A_RANGE = [0, 60]
ELEMENTS_OF_INTEREST = ['V', 'Al', 'C']

# make the plot
fig, ax = plt.subplots(figsize=(14, 8))

# make a matrix from all isotopes
all_isotopes = []
maxZ = -1
maxA = -1
for d in pp.NUCLIDE_DICTIONARY:
    for i in d['isotopes']:
        all_isotopes.append((d['Z'], i))
        maxZ = max(maxZ, d['Z'])
        maxA = max(maxA, i)

        # Create a Rectangle patch
        # and add the patch to the Axes
        rect = patches.Rectangle((i-0.5, d['Z']-0.5), 1, 1, linewidth=2, edgecolor='k',facecolor='none')
        ax.add_patch(rect)

# draw notable elements
for e in ELEMENTS_OF_INTEREST:
    z = pp.find_z(e)
    if z >= Z_RANGE[0] and z <= Z_RANGE[1]:
        ax.axhline(y=z)
        ax.text(1, z, e, fontsize=14)

# define an empty matrix
data_matrix = np.zeros(shape=(maxZ+1, maxA+1))
data_matrix[:, :] = 0.0

time_text = ax.text(A_RANGE[0]+5, Z_RANGE[1], '', fontsize=18)
im = plt.imshow(data_matrix, cmap='gnuplot', norm=LogNorm(vmin=MIN_VALUE, vmax=MAX_VALUE))
ax.invert_yaxis()
plt.xlabel("A", fontsize=16)
plt.ylabel("Z", fontsize=16)
plt.xlim(A_RANGE)
plt.ylim(Z_RANGE)
# plt.title(PROPERTY)
plt.grid()
fig.colorbar(im)

# iterate over data in the file
with pp.JSONReader(FILENAME) as output:
    def animate(timestamp):
        data_matrix[:, :] = 0.0
        for nuclide in timestamp.nuclides:
            z = pp.find_z(nuclide.element)
            a = nuclide.isotope
            value = getattr(nuclide, PROPERTY)
            if value > 0.0:
                data_matrix[z, a] = value
        im.set_array(data_matrix)
        time_text.set_text("{} s - activity={:.3e} Bq".format(
            timestamp.cooling_time+timestamp.irradiation_time,
            timestamp.total_activity))
        return [im, time_text]

    anim = animation.FuncAnimation(fig, animate, output, interval=200, blit=False)
    # anim.save('./chartofnuclidesanimation.gif', writer='imagemagick', fps=3)

plt.show()