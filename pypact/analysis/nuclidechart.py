from __future__ import division

try:
    import numpy as np
except:
    raise ImportError("Numpy cannot be found. It is required for analysis.")


def nuclidechart(matrix, xlabel=None, ylabel=None, zstep=2, nstep=2, colourmap=cm.cool):
    """
        Plot a matrix using matplotlob rectangles
        Will take weightings between [0,1]
    """
    f = plt.figure(figsize=(14, 10))

    ax = plt.gca()
    r, c = matrix.shape

    ax.set_aspect('equal', 'box')
    boxsize = 1
    for (x, y), w in np.ndenumerate(matrix):
        if w <= 0.0:
            continue
        rect = plt.Rectangle([x - boxsize / 2, y - boxsize / 2],
                             boxsize, boxsize,
                             facecolor=colourmap(w),
                             edgecolor='black')
        ax.add_patch(rect)

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    ax.xaxis.set_ticks(np.arange(0, r+1, nstep))
    ax.yaxis.set_ticks(np.arange(0, c+1, zstep))
    ax.autoscale_view()

    plt.tight_layout()
    return f
