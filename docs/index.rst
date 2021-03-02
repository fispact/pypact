.. pypact documentation master file, created by
   sphinx-quickstart on Tue Feb 23 20:00:45 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypact's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Pypact's original aim was to make FISPACT-II output files easy to parse so that more time can be spent on analysis,
and much less time on interrogating the output file. No more convoluted scripts, just one simple to use package!
However, it has evolved beyond that to provide a utility library for FISPACT-II, not just parsing output files,
but also writing input files (fluxes, files, inputs), data manipulation, group convert, plotting, and more!

These documentation pages will hopefully show you how it works and provide examples how you can use it.


.. image:: ../examples/figures/periodictableanimation.gif


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

Installation
===============
Pypact is pure python3 only with very minimal dependencies - only numpy!

If you want to install the latest release you can do so by using pip:

::

   pip3 install pypact

You can alternatively just clone this repository and install from source:

::

   git clone https://github.com/fispact/pypact
   cd pypact
   pip3 install .

Getting Started
===============
There are many things to do with pypact which are subsequently discussed and
there are many examples at: https://github.com/fispact/pypact/tree/master/examples,
but a very first example would be to read an existing FISPACT-II file and get the
nuclides at the first timestep.

::

   import pypact as pp

   # the standard output file from FISPACT-II
   # test files exist in 'references' directory
   filename = 'myfispactrun.out'

   with pp.Reader(filename) as output:
      nuclides = output[0].nuclides
      for nuc in nuclides:
         print(f"{nuc.name} = {nuc.atoms:.3e} atoms")