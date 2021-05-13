import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
import pypact as pp


FILENAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "AlVC.json"
)

PROPERTY = "activity"
MIN_VALUE = 1e1
MAX_VALUE = 1e11

# make the plot
fig, ax = plt.subplots(figsize=(14, 8))


def makeperiodictable():
    START_INDEX = 1
    END_INDEX = 18
    elements = {}

    def addelement(Z, row, column):
        # Create a Rectangle patch
        # and add the patch to the Axes
        rect = patches.Rectangle(
            (column + 0.5, row + 0.5),
            0.95,
            0.9,
            linewidth=1,
            edgecolor="k",
            facecolor="none",
        )
        rx, ry = rect.get_xy()
        cx = rx + rect.get_width() / 2.0
        cy = ry + rect.get_height() / 2.0

        ax.add_patch(rect)
        ax.annotate(
            pp.find_element(Z),
            (cx, cy),
            color="k",
            weight="bold",
            fontsize=11,
            ha="center",
            va="center",
        )
        ax.annotate(
            str(Z),
            (cx - 0.25, cy - 0.25),
            color="k",
            fontsize=8,
            ha="center",
            va="center",
        )
        elements[Z] = {"rect": rect, "value": 0.0}
        return Z + 1

    # first row is trivial
    nextZ = 1

    skip_indicies = [
        (1, 18),
        (2, 13),
        (2, 13),
        (-1, -1),
        (-1, -1),
    ]

    for row, (s, e) in enumerate(skip_indicies):
        for i in range(START_INDEX, END_INDEX + 1):
            if i > s and i < e:
                continue
            nextZ = addelement(nextZ, row, i)

    # last 2 rows are a bit different - do them separately
    row = len(skip_indicies)
    OFFSET = 17
    for row in [len(skip_indicies), len(skip_indicies) + 1]:
        for i in range(START_INDEX, END_INDEX + OFFSET - 2):
            if i < 3:
                nextZ = addelement(nextZ, row, i)
            elif i < OFFSET + 1:
                nextZ = addelement(nextZ, row + 2, i)
            else:
                nextZ = addelement(nextZ, row, i - OFFSET + 3)

    plt.xlim([START_INDEX, END_INDEX + 2])
    plt.ylim([0, 10])
    ax.axis("off")
    ax.invert_yaxis()
    return elements


elements = makeperiodictable()

time_text = ax.text(4, 0.5, "", fontsize=18)
cmap = mpl.cm.get_cmap("gnuplot")
logcmap = LogNorm(vmin=MIN_VALUE, vmax=MAX_VALUE)
sm = mpl.cm.ScalarMappable(norm=logcmap, cmap=cmap)
sm.set_array([])
fig.colorbar(sm, ax=ax)
# iterate over data in the file first
times = []
activities = []
data = []
with pp.JSONReader(FILENAME) as output:
    for timestamp in output:
        # reset values and colors
        for _, v in elements.items():
            v["rect"].set_facecolor("none")
            v["value"] = 0.0

        for nuclide in timestamp.nuclides:
            z = pp.find_z(nuclide.element)
            value = getattr(nuclide, PROPERTY)
            if value > 0.0:
                elements[z]["value"] += value
                elements[z]["rect"].set_facecolor(cmap(logcmap(value)))

        data.append([(k, v["rect"].get_facecolor()) for k, v in elements.items()])
        times.append(timestamp.cooling_time + timestamp.irradiation_time)
        activities.append(timestamp.total_activity)

# then animate
def animate(tindx):
    for entry in data[tindx]:
        elements[entry[0]]["rect"].set_facecolor(entry[1])

    time = times[tindx]
    unit = "secs"
    if time > 60:
        time = time / 60
        unit = "mins"

    if time > 60:
        time = time / 60
        unit = "hours"

    if time > 24:
        time = time / 24
        unit = "days"

    if time > 365.25:
        time = time / 365.25
        unit = "years"
    time_text.set_text(
        "{:.2f} {} - activity={:.3e} Bq".format(time, unit, activities[tindx])
    )
    return [time_text]


anim = animation.FuncAnimation(fig, animate, range(len(times)), interval=1, blit=False)
# very slow to save the animation (about 10 mins)
# anim.save('./periodictableanimation.gif', writer='imagemagick', fps=10)

plt.show()
