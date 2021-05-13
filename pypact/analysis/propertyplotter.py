from __future__ import division

from pypact.analysis.timezone import TimeZone


class NuclideDataEntry(object):
    def __init__(self, nuclide):
        self.element = nuclide[0]
        self.isotope = nuclide[1]

        self.reset()

    def reset(self):
        self.times = []
        self.values = []

    def __str__(self):
        return str.format(
            "Isotope {0}-{1} values: {2}", self.element, self.isotope, self.values
        )


def plotproperty(
    output, property, isotopes, plotter, fractional=False, timeperiod=TimeZone.BOTH
):

    plotter.newcanvas()
    [i.reset() for i in isotopes]

    # process the data
    for t in output:
        if (t.cooling_time > 0.0 and timeperiod == TimeZone.IRRAD) or (
            t.cooling_time == 0.0 and timeperiod == TimeZone.COOL
        ):
            continue

        total = 0.0
        for n in t.nuclides:
            value = getattr(n, property)
            total += value
            for i in isotopes:
                if n.element == i.element and n.isotope == i.isotope:
                    i.times.append(t.irradiation_time + t.cooling_time)
                    i.values.append(value)

        if fractional and total > 0:
            for i in isotopes:
                for v in i.values:
                    v = v / total

    # style the plot
    for i in isotopes:
        if not i.values or not all(j > 0 for j in i.values):
            continue

        yaxislabel = str.format("{0}", property)
        if fractional:
            yaxislabel = str.format("fractional {0}", property)

        f = plotter.lineplot(
            x=i.times,
            y=i.values,
            datalabel=str.format("{0}-{1}", i.element, i.isotope),
            xlabel="time [s]",
            ylabel=yaxislabel,
            logx=(timeperiod != TimeZone.IRRAD),
            logy=True,
            overlay=True,
        )

    if timeperiod == TimeZone.BOTH:
        plotter.custom(
            "axvline",
            x=output[-1].irradiation_time,
            color="k",
            linestyle="--",
            label="cooling",
        )
    plotter.addlegend(location="lower right")

    return f
