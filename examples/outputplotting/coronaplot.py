#!/usr/bin/env python3

"""
    Make a heatmap like plot (imshow) with a sliding window over
    time series data
"""

import os
import math
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pypact as pp

# change the filename here
runname = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "Ti.out"
)

MAX_TIMESTEPS = 200
TOP_NUCLIDES = 40
PROP = "activity"
LOG = True
CMAP = "gnuplot2_r"
SHOW_STABLE = False

SECS_IN_HOUR = 60 * 60
SECS_IN_DAY = 24 * SECS_IN_HOUR
SECS_IN_WEEK = 7 * SECS_IN_DAY
SECS_IN_MONTH = 30 * SECS_IN_DAY
SECS_IN_YEAR = 365.25 * SECS_IN_DAY
SECS_IN_DECADE = 10 * SECS_IN_YEAR
SECS_IN_MILLENIUM = 100 * SECS_IN_DECADE


def get_time_unit(time):
    # very dumb code...
    if time < SECS_IN_HOUR:
        return f"{time:.1f} s"
    if time < SECS_IN_DAY:
        return f"{time/SECS_IN_HOUR:.1f} hours"
    if time < SECS_IN_WEEK:
        return f"{time/SECS_IN_DAY:.1f} days"
    if time < SECS_IN_MONTH:
        return f"{time/SECS_IN_WEEK:.1f} weeks"
    if time < SECS_IN_YEAR:
        return f"{time/SECS_IN_MONTH:.1f} months"
    if time < SECS_IN_DECADE:
        return f"{time/SECS_IN_YEAR:.1f} years"
    if time < SECS_IN_MILLENIUM:
        return f"{time/SECS_IN_DECADE:.1f} decades"
    return f"{time/SECS_IN_DECADE:.1f} millenia"


def highlight_cell(x, y, ax=None, **kwargs):
    rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect


def make_mat(output, ax=None, prop="atoms"):
    min_value, max_value = 0.0, 0.0
    nuclides = sorted_top_nuclides(output, ntop=TOP_NUCLIDES, prop=prop)
    ntimesteps = min(MAX_TIMESTEPS, len(output))
    mat = np.zeros((ntimesteps, TOP_NUCLIDES + 1))
    times = []
    for i, timestamp in enumerate(output[:ntimesteps]):
        times.append(get_time_unit(timestamp.currenttime))
        for j, nuclide in enumerate(timestamp.nuclides):
            # find index of nuclide in sorted nuclides
            index = next(
                (n for n, item in enumerate(nuclides) if item == nuclide.name),
                -1,
            )

            if index == -1:
                continue
            mat_value = getattr(nuclide, prop)
            min_value = min(min_value, mat_value)
            max_value = max(max_value, mat_value)
            mat[i, index] = mat_value
            highlight_cell(i, index, ax=ax, color="k", linewidth=1)
    return mat.T, nuclides, times, min_value, max_value


def sorted_top_nuclides(output, ntop=100, prop="atoms"):
    allnuclides = defaultdict()
    for timestamp in output:
        for nuclide in timestamp.nuclides:
            name = nuclide.name
            value = getattr(nuclide, prop)
            # ignore unstable nuclides which have short halflives
            # compared to the timestep - take 10% of timestep here as cutoff
            show_stable = SHOW_STABLE and nuclide.half_life == 0.0
            if value > 0 and (
                (nuclide.half_life > timestamp.duration * 0.1) or show_stable
            ):
                allnuclides[name] = max(allnuclides.get(name, 0), value)

    # sort nuclides based on the property
    sortednuclides = sorted(allnuclides, key=allnuclides.get, reverse=True)
    return sortednuclides[:ntop]


fig, ax = plt.subplots(figsize=(10, 8))

with pp.Reader(runname) as output:
    mat, nuclides, times, min_value, max_value = make_mat(output, prop=PROP, ax=ax)
    # if LOG and max_value > 0:
    #     max_value = math.log10(max_value)
    norm = (
        LogNorm(vmin=max(1, min_value), vmax=max_value)
        if LOG
        else Normalize(vmin=max(0, min_value), vmax=max_value)
    )

    im = ax.imshow(mat, cmap=CMAP, norm=norm, aspect="auto")


titlestr = "log" if LOG else ""
plt.title(f"Top {TOP_NUCLIDES} ranked by {titlestr} {PROP}")
plt.xlabel("time index", fontsize=18)
plt.ylabel("nuclide", fontsize=18)

# show only every nth tick
ticktimes = [time if i % 25 == 0 else "" for i, time in enumerate(times)]
ax.set_xticks(np.arange(len(ticktimes)))
ax.set_xticklabels(ticktimes, ha="right", fontsize=8)
ax.set_yticks(np.arange(TOP_NUCLIDES))
ax.set_yticklabels([f"{n}" for n in nuclides], ha="right", fontsize=8)
# ax.set_ylim(-1, TOP_NUCLIDES)
ax.set_ylim(TOP_NUCLIDES, -1)

# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax, fraction=0.046, pad=0.04)

plt.show()
