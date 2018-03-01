class PlotEngine(object):
    """
        A base class for representing a plotter object
        Provides a standard interface for any plotting library
        To add a new plotting library, extend this base class
    """
    _engine_name = None
    _engine = None

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.enginename)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.enginename == other.enginename

    def lineplot(self, x, y,
                 datalabel="",
                 xlabel="",
                 ylabel="",
                 logx=False,
                 logy=False,
                 overlay=True):
        raise NotImplementedError

    def newcanvas(self):
        raise NotImplementedError        

    def addlegend(self, location=None):
        raise NotImplementedError

    def custom(self, func, *args, **kwargs):
        return getattr(self.engine, func)(*args, **kwargs)

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

    @property
    def data(self):
        """
        The plotter engine
        """
        return self._data

    def save(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
