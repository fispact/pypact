import os
import pypact as pp
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Rectangle


filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'reference', 'test127.out')

MAX_A = 295
MAX_Z = pp.NUMBER_OF_ELEMENTS

RUN_DATA = None
with pp.Reader(filename) as output:
    RUN_DATA = output

def plot_chart(index, prop='activity', z_range=[0, 50], a_range=[1, 100]):
    targetnames = []
    targetvalues = []

    for n in RUN_DATA[index].nuclides:
        Z = pp.find_z(n.element)
        A = n.isotope
        targetnames.append("{}{}".format(n.element, A))
        targetvalues.append(getattr(n, prop))
    
    rectangles = []
    names = []
    
    norm = colors.LogNorm(vmin=max(0, min(targetvalues)), vmax=max(targetvalues))
    data = pp.NUCLIDE_DICTIONARY
    for d in data:
        for i in d['isotopes']:
            if int(d['Z']) >= z_range[0] and int(d['Z']) <= z_range[-1] and \
                int(i) >= a_range[0] and int(i) <= a_range[-1]:
                names.append(r'{}$^{{{}}}$'.format(d['element'], i))
                if "{}{}".format(d['element'], i) in targetnames:
                    indx = targetnames.index("{}{}".format(d['element'], i))
                #     print("{}{}".format(d['element'], i))
                    rectangles.append(Rectangle((float(i) - 0.5, float(d['Z']) - 0.5), 1.0, 1.0, 
                        edgecolor='k', alpha=0.7, facecolor=norm(targetvalues[indx]), linewidth=0.1))
                else:
                    rectangles.append(Rectangle((float(i) - 0.5, float(d['Z']) - 0.5), 1.0, 1.0, 
                        edgecolor='k', alpha=0.7, facecolor='none', linewidth=0.1))

    fig, ax = plt.subplots()
    for n, r in zip(names, rectangles):
        ax.add_patch(r)
        rx, ry = r.get_xy()
        cx = rx + r.get_width()/2.0
        cy = ry + r.get_height()/2.0
        ax.annotate(n, (cx, cy), color='k', fontsize=1, ha='center', va='center')
    
    ax.set_xlim(a_range)
    ax.set_ylim(z_range)
#     ax.plot([0, 2*MAX_A], [0, MAX_A], 'b:', alpha=0.4)
#     ax.plot([0, MAX_A], [0, pp.NUMBER_OF_ELEMENTS], 'r--', alpha=0.3)
    ax.set_xlabel("nucleons")
    ax.set_ylabel("protons")
    ax.grid()

for t in range(len(RUN_DATA))[:2]:
    plot_chart(t)

plt.show()
