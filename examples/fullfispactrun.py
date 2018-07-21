#!/usr/bin/env python3

import os
import subprocess
import pypact as pp
import matplotlib.pyplot as plt


show_plot = False
group = 709
inventory = [('Fe', 1.0)]

# default filenames
files_filename = "files"
input_filename = "run.i"
fluxes_filename = "fluxes"

# files file
def createfiles():
    nuclear_data_base = os.getenv('NUCLEAR_DATA', os.path.join(os.sep, 'opt', 'fispact', 'nuclear_data'))
    
    ff = pp.FilesFile(base_dir=nuclear_data_base)
    
    ff.setXS('TENDL2015')
    ff.setFissionYield('GEFY52')
    ff.setProbTab('TENDL2015')
    ff.setDecay('DECAY')
    ff.setRegulatory('DECAY')
    ff.setGammaAbsorb('DECAY')
    ff.fluxes = fluxes_filename
    for invalid in ff.invalidpaths():
        print("FilesFile:: missing file: {}".format(invalid))

    return ff

# input file
def createinput():
    id = pp.InputData(name=input_filename.strip('.i'))
    
    id.overwriteExisting()
    id.enableJSON()
    id.approxGammaSpectrum()
    id.collapse(group)
    id.condense()
    id.enableMonitor()
    id.outputHalflife()
    id.outputHazards()
    id.useNeutron()
    id.outputInitialInventory()
    id.setLogLevel(pp.LOG_SEVERITY_ERROR)
    id.setAtomsThreshold(1.0e-3)
    id.setDensity(7.875)
    id.setMass(1.0e-3)
    for e, r in inventory:
        id.addElement(e, percentage=r*100.0)

    id.addIrradiation(300.0, 1.1e15)
    id.addCooling(10.0)
    id.addCooling(100.0)
    id.addCooling(1000.0)
    id.addCooling(10000.0)
    id.addCooling(100000.0)
    
    id.validate()

    return id

# fluxes file
def createflux():
    # set monoenergetic flux at 14 MeV for group 709
    flux = pp.FluxesFile(name="14 MeV (almost) monoenergetic", norm=1.0)
    
    flux.setGroup(group)
    flux.setValue(12.0e6, 0.1)
    flux.setValue(13.0e6, 0.4)
    flux.setValue(14.0e6, 1.0)

    flux.validate()

    return flux

def fispact_compute(input, files, fluxes):
    # write all files
    pp.serialize(input, input_filename)
    pp.serialize(files, files_filename)
    pp.serialize(fluxes, fluxes_filename)

    # run fispact
    fispact_exe = os.getenv('FISPACT', os.path.join(os.sep, 'opt', 'fispact', 'bin', 'fispact'))
    proc = subprocess.check_call("{} {} {}".format(fispact_exe, input.name, files_filename), shell=True)

    # check for log file
    logfile = "{}.log".format(input_filename.strip('.i'))
    if not os.path.isfile(logfile):
        raise RuntimeError("No log file produced.")

    outfile = "{}.json".format(input.name)
    with pp.Reader(outfile) as output:
        return output

# perform analysis on the output
def analyse(output):
    # plot the final inventory ignoring the initial elements
    elements = {}
    ignore_elements = list(map(list, zip(*inventory)))[0]
    if len(output) == 0:
        print("No valid inventory output, exiting")
        exit

    for n in output[-1].nuclides:
        if n.element not in ignore_elements:
            if n.element in elements:
                elements[n.element] += n.grams
            else:
                elements[n.element] = n.grams

    total_grams = sum([g for e, g in elements.items()])
    for e, g in elements.items():
        print("{} {:.2f}%".format(e, g*100.0/total_grams))
        # we must rescale the values
        elements[e] = g/total_grams

    labels, values = list(zip(*(list(elements.items()))))
    if show_plot:
        plt.pie(list(values), labels=list(labels), autopct='%2.2f%%', shadow=False)
        plt.show()

# main script
input  = createinput()
files  = createfiles()
fluxes = createflux()
output = fispact_compute(input, files, fluxes)
analyse(output)
