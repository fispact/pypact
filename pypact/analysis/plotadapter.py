try:
    import matplotlib.pyplot
    from matplotlib import cm
    from matplotlib.colors import LogNorm
    import matplotlib.animation as animation
    from matplotlib.patches import Rectangle
    from matplotlib.collections import PatchCollection
except:
    raise ImportError("Matplotlib cannot be found. It is required for plotting.")

try:
    import numpy as np
except:
    raise ImportError("Numpy cannot be found. It is required for plotting.")


class PlotAdapter(object):
    """
        Wraps the Matplotlib plotter
    """
    _engine_name = 'matplotlib'
    _engine = matplotlib.pyplot

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.enginename)

    @property
    def enginename(self):
        """
        The name of the plotting engine
        """
        return self._engine_name

    @property
    def engine(self):
        """
        The plotter engine
        """
        return self._engine

    def show(self):
        self.engine.show()

    def grid(self, show=True):
        self.engine.grid(show)

    def addlegend(self, location):
        self.engine.legend(loc=location)

    def newcanvas(self, *args, **kwargs):
        self._figure = self.engine.figure(*args, **kwargs)
        return self._figure

    def custom(self, *args, **kwargs):
        pass
    
class LinePlotAdapter(PlotAdapter):
    def lineplot(self, x, y, datalabel="", xlabel="", ylabel="",
                 logx=False, logy=False, overlay=True):

        if not overlay:
            self.newcanvas()

        self.engine.xlabel(xlabel)
        self.engine.ylabel(ylabel)

        if logx:
            self.engine.xscale('log')
        if logy:
            self.engine.yscale('log')

        self.engine.plot(x, y, label=datalabel)

    def custom(self, attr, *args, **kwargs):
        getattr(self.engine, attr)(*args,**kwargs)


class MatrixPlotAdapter(PlotAdapter):

    def nuclidechart(self, matrix, xlabel="", ylabel="",
                     nstep=2, zstep=2, minX=0,  maxX=288,
                     minY=0, maxY=118, colourmap=cm.cool):
        self.newcanvas()
        self.grid()

        ax = self.engine.gca()
        r, c = matrix.shape

        ax.set_aspect('equal', 'box')
        boxsize = 1
        for (x, y), w in np.ndenumerate(matrix):
            if w <= 0.0:
                continue
            rect = Rectangle([x - boxsize / 2, y - boxsize / 2],
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
        ax.set_xlim((max(minX-1,0), maxX+1))
        ax.set_ylim((max(minY-1,0), maxY+1))
        ax.autoscale_view()

        self.engine.tight_layout()

    def matrixplot(self, matrix):
        self.newcanvas()
        self.grid()
        self.engine.imshow(matrix.T, origin='lower',
                           norm=LogNorm(vmin=10e-24, vmax=1),
                           cmap=cm.cool)
        self.engine.colorbar()

class AnimatedMatrixPlotAdapter(PlotAdapter):

    def animatedchart(self, matricies, xlabel="", ylabel="",
                      nstep=2, zstep=2, minX=0, maxX=100,
                      minY=0, maxY=100, colourmap=cm.cool,
                      timeinterval=100, figuresize=((15,10))):
        fig = self.newcanvas(figsize=figuresize)
        ax = self.engine.gca()
        self.grid()

        ax.xaxis.set_ticks(np.arange(0, maxX+1, nstep))
        ax.yaxis.set_ticks(np.arange(0, maxY+1, zstep))
        ax.set_xlim((max(minX-1,0), maxX+1))
        ax.set_ylim((max(minY-1,0), maxY+1))

        ax.set_aspect('equal', 'box')
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)

        boxsize = 1
        def animate(i):
            [c.remove() for c in ax.collections]

            patches = []
            for (x, y), w in np.ndenumerate(matricies[i]):
                if w != 0.0:
                    patches.append(Rectangle([x - boxsize / 2, y - boxsize / 2],
                                     boxsize, boxsize,
                                     fc=colourmap(w),
                                     ec='black'))

            colors = np.logspace(10e-30, 1, 100, endpoint=True)
            p = PatchCollection(patches)
            p.set_edgecolor('black')
            p.set_array(np.array(colors))
            ax.add_collection(p)
            return ax,

        anim = animation.FuncAnimation(fig, animate,
                                       frames=len(matricies),
                                       interval=timeinterval,
                                       repeat_delay=timeinterval*3,
                                       blit=False)
        return anim
