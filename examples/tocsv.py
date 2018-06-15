import pypact as pp

# change the filename here
runname = 'inventory'

# if you change this you must also
# change the list at the bottom!
headers = [
    'nuclides',
    'activity (Bq)',
    'grams',
    'alpha heat (kW)',
    'beta heat (kW)',
    'gamma heat (kW)',
    'cumulative time (secs)',
    'is irradiation'
]

def fmt(items):
    str = "{:>20}".format(items[0])
    for i in items:
        str += ", {:>20}".format(i)
    return "{}\n".format(str)

with pp.Reader('{}.out'.format(runname)) as output:
    with open('{}.csv'.format(runname), 'wt') as f:
        f.write(fmt(headers))
        for t in output:
            for n in t.nuclides:
                name = '{}{}{}'.format(n.element, n.isotope, n.state)
                # if you changed the headers you must change this too!!
                #
                f.write(fmt([name,
                             n.activity,
                             n.grams,
                             n.alpha_heat,
                             n.beta_heat,
                             n.gamma_heat,
                             t.currenttime,
                             t.isirradiation()]))
