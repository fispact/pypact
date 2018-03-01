from pypact.analysis.plotengine import PlotEngine


class MatplotLibPlotEngine(PlotEngine):
    """
        Matplotlib plotter
        Only supports single figure plotting
    """
    try:
        import matplotlib.pyplot
        from matplotlib import cm
    except:
        raise ImportError("Matplotlib cannot be found. It is required for plotting.")

    _engine_name = 'matplotlib'
    _engine = matplotlib.pyplot

    show = lambda self: self.engine.show()

    def lineplot(self, x, y,
                 datalabel="",
                 xlabel="",
                 ylabel="",
                 logx=False,
                 logy=False,
                 overlay=True):

        if not overlay:
            self.newcanvas()

        self.engine.xlabel(xlabel)
        self.engine.ylabel(ylabel)

        if logx:
            self.engine.xscale('log')
        if logy:
            self.engine.yscale('log')

        self.engine.plot(x, y, label=datalabel)

    def addlegend(self, location):
        self.engine.legend(loc=location)

    def newcanvas(self):
        self._figure = self.engine.figure()
