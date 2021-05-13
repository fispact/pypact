#!/usr/bin/env python3

"""
    Make a heatmap like plot (imshow) with a sliding window over
    time series data
"""

import os
import numpy as np
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

import pypact as pp
from pypact.util.time import get_time_string


def highlight_cell(x, y, ax=None, **kwargs):
    rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect


def sorted_top_nuclides(output, ntop=100, prop="atoms", show_stable=False):
    allnuclides = defaultdict()
    for timestamp in output:
        for nuclide in timestamp.nuclides:
            name = nuclide.name
            value = getattr(nuclide, prop)
            # ignore unstable nuclides which have short halflives
            # compared to the timestep - take 10% of timestep here as cutoff
            ss = show_stable and nuclide.half_life == 0.0
            if value > 0 and ((nuclide.half_life > timestamp.duration * 0.1) or ss):
                allnuclides[name] = max(allnuclides.get(name, 0), value)

    # sort nuclides based on the property
    sortednuclides = sorted(allnuclides, key=allnuclides.get, reverse=True)
    return sortednuclides[:ntop]


def make_mat(
    output, ax=None, prop="atoms", ntop=40, max_timesteps=200, cell_border=True
):
    min_value, max_value = 0.0, 0.0
    nuclides = sorted_top_nuclides(output, ntop=ntop, prop=prop)
    ntimesteps = min(max_timesteps, len(output))
    mat = np.zeros((ntimesteps, ntop + 1))
    times = []
    for i, timestamp in enumerate(output[:ntimesteps]):
        times.append(get_time_string(timestamp.currenttime))
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
            if cell_border:
                highlight_cell(i, index, ax=ax, color="k", linewidth=0.2)
    return mat.T, nuclides, times, min_value, max_value


def process_and_plot(
    output,
    prop="activity",
    log_norm=True,
    ntop=40,
    max_timesteps=200,
    save_plot="coronaplot.png",
    dpi=200,
    cmap="gnuplot2_r",
    cell_border=True,
    vmin=None,
    vmax=None
):
    fig, ax = plt.subplots(figsize=(1500 / dpi, 800 / dpi), dpi=dpi)

    mat, nuclides, times, min_value, max_value = make_mat(
        output,
        prop=prop,
        ax=ax,
        ntop=ntop,
        max_timesteps=max_timesteps,
        cell_border=cell_border,
    )
    vmin = max(1, min_value) if vmin is None else vmin
    vmax = max_value if vmin is None else vmax
    norm = (
        LogNorm(vmin=vmin, vmax=vmax)
        if log_norm
        else Normalize(vmin=max(0, vmin), vmax=vmax)
    )

    im = ax.imshow(mat, cmap=cmap, norm=norm, aspect="auto")

    plt.title(f"Top {len(nuclides)} ranked by {prop}", fontsize=12)
    plt.xlabel("time", fontsize=10)
    plt.ylabel("nuclide", fontsize=10)

    # show only every nth tick
    ticktimes = [time if i % 5 == 0 else "" for i, time in enumerate(times)]
    ax.set_xticks(np.arange(len(ticktimes)))
    ax.set_xticklabels(ticktimes, ha="right", fontsize=4, rotation=-90)
    ax.set_yticks(np.arange(len(nuclides)))
    ax.set_yticklabels([f"{n}" for n in nuclides], ha="right", fontsize=4)
    ax.set_ylim(len(nuclides), -1)

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax, fraction=0.046, pad=0.04)
    plt.tight_layout()

    if save_plot is not None:
        plt.savefig(save_plot, dpi=dpi)
    else:
        plt.show()


# main
runname = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "AlVC.json"
)

rdr = pp.JSONReader if runname.endswith(".json") else pp.Reader
with rdr(runname) as output:
    process_and_plot(
        output,
        prop="activity",
        ntop=100,
        max_timesteps=600,
        save_plot="coronaplot.png",
        dpi=200,
        cmap="gnuplot2_r",
        cell_border=False,
        vmin=1,
        vmax=1e18
    )
