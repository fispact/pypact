#!/usr/bin/env python3

import os
import pypact as pp
import matplotlib.pyplot as plt


filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "test31"
)

SECS_TO_YEAR = 1.0 / (60.0 * 60.0 * 24.0 * 365.0)


class PlotData(object):
    """
    Simple data structure to hold the data
    we want to plot
    """

    def __init__(self):
        """
        Initialise data structures
        """
        # run name
        self.title = ""

        # the x-y data we want to plot
        self.time = []  # in years
        self.heat = []  # kW/kg

        # half life values for certain isotopes with their heat output
        # from the first irradiation step
        self.isotope_values = {}

    def plot(self):
        """
        Handles the plotting
        """
        f = plt.figure()

        # plot the data using matplotlib
        plt.xscale("log")
        plt.yscale("log")
        plt.title(self.title, fontsize=22)
        plt.xlabel("Time after irradiation (years)", fontsize=18)
        plt.ylabel("Heat output (kW/kg)", fontsize=18)
        plt.plot(self.time, self.heat, linestyle="--", marker="o", color="k")

        # add the data points from isotope values
        for k, v in self.isotope_values.items():
            plt.plot(v[0], v[1], label=k, marker="+", color="g", markersize=8)
            plt.annotate(k, xy=v)

        # add a grid
        plt.grid(True, which="both")

        return f


def process_output(output):
    """
    Process the output to get what we need
    JSON doesn't contain the mass (yet)
    if it is not read use 1 gram
    """
    pd = PlotData()

    data = output.inventory_data
    # check that the output exists
    if data:
        max_irrad_time = max(d.irradiation_time for d in data)
        min_cooling_time = min(d.cooling_time for d in data if d.cooling_time != 0.0)

        pd.title = output.run_data.run_name

        for d in data:
            # JSON file doesn't yet contain mass, assume 1g for this case
            mass = d.total_mass if d.total_mass > 0.0 else 1e-3
            if d.cooling_time == 0.0:
                for n in d.nuclides:
                    i = "{}{}{}".format(n.element, n.isotope, n.state)
                    if n.half_life >= min_cooling_time and n.heat > 1e-13:
                        pd.isotope_values[i] = n.half_life * SECS_TO_YEAR, n.heat / mass

            if d.cooling_time > 0.0:
                pd.time.append(d.cooling_time * SECS_TO_YEAR)
                pd.heat.append(d.total_heat / mass)

    return pd


def use_jsonfile(filename):
    """
    Reads the .json file with pypact
    """
    output = pp.Output()
    output.json_deserialize(open("{}.json".format(filename)).read())
    return process_output(output)


def use_outfile(filename):
    """
    Reads the .out file with pypact
    """
    with pp.Reader("{}.out".format(filename)) as output:
        return process_output(output)


#### main script ####
# use out file with pypact
fig1 = use_outfile(filename).plot()
# then use JSON file with pypact
fig2 = use_jsonfile(filename).plot()
# figures should be the same

# show plots
plt.show()
