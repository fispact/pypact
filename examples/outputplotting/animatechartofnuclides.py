import os
import numpy as np
import pypact as pp
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class ColouredChartOfNuclidesPlot:
    """
    A simple object that produces a chart of the nuclides
    plot.

    TODO: Currently builds on matplotlib, but need to allow for
    other plotting libraries.
    """

    color_engine = colors
    plt_engine = plt

    def __init__(
        self,
        data_matrix=None,
        figsize=(12, 8),
        cmap="gnuplot_r",
        vmin=1e10,
        vmax=1e20,
        prop="atoms",
        colourbar=True,
    ):

        # must contain white
        self._cmap = mpl.cm.get_cmap(cmap)
        self._cmap.set_under("w")

        self.property = prop

        self.vmin = vmin
        self.vmax = vmax

        self.norm = colors.LogNorm(vmin=vmin, vmax=vmax)

        # make a chart of the nuclides
        self.fig, self.ax = self.plt_engine.subplots(figsize=figsize)

        self.colourbar = colourbar
        if colourbar:
            sm = mpl.cm.ScalarMappable(norm=self.norm, cmap=self._cmap)
            sm.set_array([])
            self.fig.colorbar(sm, ax=self.ax, fraction=0.046, pad=0.1)

        # all isotopes
        self.all_isotopes = []

        self.im = None

        # do not change these values without knowing what you are doing
        # bespokely made for splitting into four pieces to plot well
        self.__XSIZE = 140
        self.__YSIZE = 90

        # define an empty matrix of size (self.__YSIZE, self.__XSIZE)
        # X and Y are inverted
        self.data_matrix = data_matrix
        if self.data_matrix is None:
            self.data_matrix = np.zeros(shape=(self.__YSIZE, self.__XSIZE))
            self.data_matrix[:, :] = -1.0

        assert self.data_matrix.shape == (self.__YSIZE, self.__XSIZE)

    @classmethod
    def _mappingfunc(cls, Z, A):
        """
        Return X, Y position where A is on X
        and Z is on Y.

        Note different to input!
        """
        # split chart into four pieces
        if Z <= 24:
            return int(A + 15), int(Z + 58)
        elif Z <= 64:
            return int(A - 40), int(Z + 8)
        elif Z <= 94:
            return int(A - 125), int(Z - 52)
        else:
            return int(A - 178), int(Z - 90)

    def _makelabels(self):
        X, Y = self._mappingfunc(1, 1)
        self.plt_engine.text(X - 4, Y, r"Z", fontsize=18)
        self.plt_engine.text(X, Y - 4, r"N", fontsize=18)

        # Z arrow
        self.plt_engine.arrow(
            X - 3,
            Y + 3,
            0,
            4,
            fc="k",
            ec="k",
            alpha=1.0,
            width=0.1,
            head_width=1,
            head_length=None,
        )

        # N arrow
        self.plt_engine.arrow(
            X + 3,
            Y - 3,
            4,
            0,
            fc="k",
            ec="k",
            alpha=1.0,
            width=0.1,
            head_width=1,
            head_length=None,
        )

        # identify key elements
        # Hydrogen
        X, Y = self._mappingfunc(1, 5)
        self.plt_engine.text(X - 0.5 + 10, Y - 0.5, r"Hydrogen", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            10,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Chromium
        X, Y = self._mappingfunc(24, 54)
        self.plt_engine.text(X - 0.5 + 20, Y - 0.5, r"Chromium", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            20,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Manganese
        X, Y = self._mappingfunc(25, 60)
        self.plt_engine.text(X - 0.5 + 20, Y - 0.5, r"Manganese", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            20,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Gadolinium
        X, Y = self._mappingfunc(64, 160)
        self.plt_engine.text(X - 0.5 + 10, Y - 0.5, r"Gadolinium", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            10,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Terbium
        X, Y = self._mappingfunc(65, 160)
        self.plt_engine.text(X - 0.5 + 20, Y - 0.5, r"Terbium", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            20,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Plutonium
        X, Y = self._mappingfunc(94, 235)
        self.plt_engine.text(X - 0.5 + 15, Y - 0.5, r"Plutonium", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            15,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Americium
        X, Y = self._mappingfunc(95, 240)
        self.plt_engine.text(X - 0.5 + 20, Y - 0.5, r"Americium", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            20,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

        # Oganesson
        X, Y = self._mappingfunc(118, 294)
        self.plt_engine.text(X - 0.5 + 5, Y - 0.5, r"Oganesson", fontsize=10)
        self.plt_engine.arrow(
            X - 0.5,
            Y - 0.5,
            5,
            0,
            fc="k",
            ec="k",
            alpha=0.5,
            width=0.05,
            head_width=0,
            head_length=0,
        )

    def _makechart(self):
        import matplotlib.patches as patches

        self.all_isotopes = []

        mZ = -1
        mA = -1
        for d in pp.NUCLIDE_DICTIONARY:
            for i in d["isotopes"]:
                mZ = max(mZ, d["Z"])
                mA = max(mA, i)

                X, Y = self._mappingfunc(d["Z"], i)
                self.all_isotopes.append((X, Y))
                self.ax.add_patch(
                    patches.Rectangle(
                        (X - 0.5, Y - 0.5),
                        1,
                        1,
                        linewidth=2,
                        edgecolor="k",
                        facecolor="none",
                    )
                )

    def _setbackground(self):
        """
        Since we make use of imshow and the whole figure
        is a matrix, we need to change the background colour
        to white to hide the fact we are using imshow
        """
        # set everything that is not in the nuclide chart to white
        for x in range(self.__XSIZE):
            for y in range(self.__YSIZE):
                if (x, y) not in self.all_isotopes:
                    self.data_matrix[y, x] = -1.0

    def setnuclidevalue(self, z, a, value):
        x, y = self._mappingfunc(z, a)
        self.data_matrix[y, x] = value

    def reset(self):
        self.data_matrix[:, :] = -1.0

    def setcolourallnuclides(self, colour="grey"):
        self._cmap.set_over(colour)
        self.data_matrix[:, :] = 1e100
        self._setbackground()

    def setupplot(self, *args, includelabels=True, **kwargs):
        self._makechart()
        self._setbackground()

        # draw Z and N labels with arrows near H1
        if includelabels:
            self._makelabels()

        self.im = self.plt_engine.imshow(
            self.data_matrix, cmap=self._cmap, norm=self.norm
        )
        self.ax.axis("off")
        self.plt_engine.xlabel("A", fontsize=16)
        self.plt_engine.ylabel("Z", fontsize=16)
        self.plt_engine.xlim([0, self.__XSIZE])
        self.plt_engine.ylim([0, self.__YSIZE])
        right = 0.99
        top = 0.99
        bottom = 0.01
        if self.colourbar:
            right = 0.95
            top = 0.95
            bottom = 0.05
        self.plt_engine.subplots_adjust(
            left=0.01, bottom=bottom, right=right, top=top, wspace=None, hspace=None
        )
        # fig.colorbar(im, cax = fig.add_axes([0.91, 0.2, 0.03, 0.6]))

        return self.im

    def update(self, matrix):
        self.im.set_array(matrix)
        return self.im

    def show(self):
        self.plt_engine.show()


"""
    Main script 
"""
FILENAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "AlVC.json"
)

PROPERTY = "activity"
THRESHOLD = 1e1

data_matrices = []

chart = ColouredChartOfNuclidesPlot(
    cmap="gnuplot_r", vmin=THRESHOLD, vmax=1e11, prop=PROPERTY
)
# chart.setcolourallnuclides('grey')
chart.setupplot(includelabels=True)

# iterate over data in the file and store all matrices
# to a list first to have a quicker plot
with pp.JSONReader(FILENAME) as output:
    for timestamp in output:
        chart.reset()
        for nuclide in timestamp.nuclides:
            z = pp.find_z(nuclide.element)
            a = nuclide.isotope
            value = getattr(nuclide, PROPERTY)
            if value > chart.vmin:
                chart.setnuclidevalue(z, a, value)
        data_matrices.append(np.copy(chart.data_matrix))


def animate(matrix):
    return (chart.update(matrix),)


anim = animation.FuncAnimation(
    chart.fig, animate, data_matrices, interval=1, blit=False
)

# anim.save('anim.gif', writer='imagemagick', fps=10)
chart.show()
