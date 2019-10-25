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
MIN_VALUE = 1e4
MAX_VALUE = 1e24
Z_RANGE = [0, 30.5]
A_RANGE = [0, 60.5]
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
        rect = patches.Rectangle((i-0.5, d['Z']-0.5), 1, 1, linewidth=1, edgecolor='k',facecolor='none')
        ax.add_patch(rect)

        rx, ry = rect.get_xy()
        cx = rx + rect.get_width()/2.0
        cy = ry + rect.get_height()/2.0

        ax.annotate("{}{}".format(d['element'], i), (cx, cy), color='k', weight='bold', fontsize=5, ha='center', va='center')

# define an empty matrix
data_matrix = np.zeros(shape=(maxZ+1, maxA+1))
data_matrix[:, :] = 0.0

time_text = ax.text(A_RANGE[0]+5, Z_RANGE[1], '', fontsize=18)
im = plt.imshow(data_matrix, cmap='gnuplot', norm=LogNorm(vmin=MIN_VALUE, vmax=MAX_VALUE))
ax.invert_yaxis()
ax.axis('off')
plt.xlabel("A", fontsize=16)
plt.ylabel("Z", fontsize=16)
plt.xlim(A_RANGE)
plt.ylim(Z_RANGE)
# plt.title(PROPERTY)
fig.colorbar(im, cax = fig.add_axes([0.91, 0.2, 0.03, 0.6]))

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

    anim = animation.FuncAnimation(fig, animate, output, interval=20, blit=False)
    # anim.save('./chartofnuclidesanimation.gif', writer='imagemagick', fps=10)

plt.show()
