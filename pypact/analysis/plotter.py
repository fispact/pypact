import matplotlib.pyplot as plt
from pypact.analysis.timezone import TimeZone

class Entry:
    def __init__(self, nuclide):
        self.e = nuclide[0]
        self.i = nuclide[1]

        self.reset()

    def reset(self):
        self.times = []
        self.values = []

    def __str__(self):
        return str.format("Isotope {0}-{1} values: {2}", self.e, self.i, self.values)


def plotproperty(output, isotopes, prop, fractional=False, timeperiod=TimeZone.BOTH):
    for i in range(0, len(isotopes)):
        isotopes[i].reset()

    for t in output.inventory_data:
        if t.cooling_time > 0.0 and timeperiod == TimeZone.IRRAD:
            continue
        if t.cooling_time == 0.0 and timeperiod == TimeZone.COOL:
            continue

        total = 0.0
        for n in t.nuclides.nuclides:
            value = getattr(n, prop)
            total += value
            for i in range(0, len(isotopes)):
                if n.element == isotopes[i].e and n.isotope == isotopes[i].i:
                    isotopes[i].times.append(t.irradiation_time + t.cooling_time)
                    isotopes[i].values.append(value)

        if fractional and total > 0:
            for i in range(0, len(isotopes)):
                for v in isotopes[i].values:
                    v = v / total

    f = plt.figure()
    for i in isotopes:
        if not i.values or not all(j > 0 for j in i.values):
            continue

        yaxislabel = str.format('{0}', prop)
        if fractional:
            yaxislabel = str.format('fractional {0}', prop)
        plt.xlabel('time [s]')
        plt.ylabel(yaxislabel)
        if timeperiod != TimeZone.IRRAD:
            plt.xscale('log')
        plt.yscale('log')

        plt.plot(i.times, i.values, label=str.format('{0}-{1}', i.e, i.i))

    if timeperiod == TimeZone.BOTH:
        plt.axvline(x=output.inventory_data[-1].irradiation_time, color='k', linestyle='--', label='cooling')
    plt.legend(loc='lower right')
    return f


def showplots():
    plt.show()
