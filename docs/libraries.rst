Libraries and Data Structures
==============================

Pypact provides several utility libraries and data structures for working with nuclear data.

Nuclide Library
---------------

Pypact includes a comprehensive nuclide library containing data for all isotopes from 
Hydrogen (Z=1) to Oganesson (Z=118), totaling 3352 isotopes.

Getting All Isotopes
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.analysis as ppa

   # Get all isotopes in the library
   all_isotopes = ppa.get_all_isotopes()
   print(f"Total isotopes: {len(all_isotopes)}")

Filtering Isotopes
~~~~~~~~~~~~~~~~~~

You can filter isotopes by atomic number:

.. code-block:: python

   import pypact.analysis as ppa

   # Get isotopes with atomic number <= 10 (H to Ne)
   light_isotopes = [i for i in ppa.get_all_isotopes() 
                     if ppa.find_z(i[0]) <= 10]
   
   print(f"Light isotopes (Z<=10): {len(light_isotopes)}")

Creating Nuclide Data Entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.analysis as ppa

   # Create nuclide data entries
   isotopes = [ppa.NuclideDataEntry(i) for i in ppa.get_all_isotopes() 
               if ppa.find_z(i[0]) <= 10]

Element Lookup
~~~~~~~~~~~~~~

Find atomic number from element symbol:

.. code-block:: python

   import pypact.analysis as ppa

   # Get atomic number for element
   z_carbon = ppa.find_z('C')
   z_iron = ppa.find_z('Fe')
   z_uranium = ppa.find_z('U')
   
   print(f"Carbon: Z={z_carbon}")
   print(f"Iron: Z={z_iron}")
   print(f"Uranium: Z={z_uranium}")

Group Conversion
----------------

Pypact provides utilities for converting between different energy group structures.

Group Structure Utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.groupconvert as gc

   # Load a group structure file
   group_structure = gc.load_group_structure('mygroups.txt')
   
   # Convert between different group structures
   converted = gc.convert_groups(data, from_structure, to_structure)

Common Group Structures
~~~~~~~~~~~~~~~~~~~~~~~

FISPACT-II supports various energy group structures:

- CCFE 709 group structure (default for fusion applications)
- CCFE 315 group structure
- VITAMIN-J 175 group structure
- Custom user-defined structures

.. code-block:: python

   import pypact.groupconvert as gc

   # Example: Converting from 709 to 315 groups
   data_709 = load_709_group_data()
   data_315 = gc.convert_groups(data_709, 
                                  from_groups=709, 
                                  to_groups=315)

Analysis Utilities
------------------

The ``pypact.analysis`` module provides various utilities for analyzing FISPACT-II results.

Time Zones
~~~~~~~~~~

Define different time periods for analysis:

.. code-block:: python

   import pypact.analysis as ppa

   # Time zones
   tz_irradiation = ppa.TimeZone.IRRAD  # During irradiation
   tz_cooling = ppa.TimeZone.COOL       # During cooling
   tz_all = ppa.TimeZone.ALL            # All timesteps

Plotting Properties
~~~~~~~~~~~~~~~~~~~

Plot various properties over time:

.. code-block:: python

   import pypact as pp
   import pypact.analysis as ppa

   filename = 'myoutput.out'
   
   with pp.Reader(filename) as output:
       # Define properties to plot
       properties = ['heat', 'grams', 'activity']
       
       # Filter isotopes (e.g., Z <= 10)
       isotopes = [ppa.NuclideDataEntry(i) 
                   for i in ppa.get_all_isotopes() 
                   if ppa.find_z(i[0]) <= 10]
       
       # Create plotter
       plotter = ppa.LinePlotAdapter()
       
       # Plot each property
       for prop in properties:
           ppa.plotproperty(output=output,
                           property=prop,
                           isotopes=isotopes,
                           plotter=plotter,
                           fractional=True,
                           timeperiod=ppa.TimeZone.COOL)
       
       plotter.show()

Fractional Contributions
~~~~~~~~~~~~~~~~~~~~~~~~

Calculate fractional contributions of nuclides to total property:

.. code-block:: python

   import pypact as pp
   import pypact.analysis as ppa

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Get total heat
       total_heat = timestep.total_heat
       
       # Calculate fractional heat for each nuclide
       for nuclide in timestep.nuclides:
           fraction = nuclide.heat / total_heat
           if fraction > 0.01:  # Show only contributions > 1%
               print(f"{nuclide.element}{nuclide.isotope}: {fraction*100:.2f}%")

Dominant Nuclides
~~~~~~~~~~~~~~~~~

Find dominant contributors to a property:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Sort nuclides by heat
       sorted_by_heat = sorted(timestep.nuclides, 
                               key=lambda n: n.heat, 
                               reverse=True)
       
       # Get top 10 contributors
       top_10 = sorted_by_heat[:10]
       
       for i, nuclide in enumerate(top_10, 1):
           print(f"{i}. {nuclide.element}{nuclide.isotope}: {nuclide.heat:.3e} W")

Data Structures
---------------

Pypact uses several key data structures to represent FISPACT-II data.

Output Object
~~~~~~~~~~~~~

The main container for all output data:

.. code-block:: python

   # Properties:
   # - run_data: RunData object
   # - inventory_data: List of TimeStep objects
   # - __getitem__(index): Get timestep by index

RunData Object
~~~~~~~~~~~~~~

Contains metadata about the run:

.. code-block:: python

   # Properties:
   # - run_name: str
   # - timestamp: str
   # - flux_name: str

TimeStep Object
~~~~~~~~~~~~~~~

Contains inventory data for a single timestep:

.. code-block:: python

   # Properties:
   # - irradiation_time: float (seconds)
   # - cooling_time: float (seconds)
   # - flux: float (n/cm²/s)
   # - total_heat: float (W)
   # - alpha_heat: float (W)
   # - beta_heat: float (W)
   # - gamma_heat: float (W)
   # - ingestion_dose: float (Sv)
   # - inhalation_dose: float (Sv)
   # - gamma_spectrum: GammaSpectrum object
   # - dose_rate: DoseRate object
   # - nuclides: List of Nuclide objects

Nuclide Object
~~~~~~~~~~~~~~

Contains data for a single nuclide:

.. code-block:: python

   # Properties:
   # - element: str (e.g., 'Fe')
   # - isotope: int (e.g., 56)
   # - state: str (e.g., 'm' for metastable)
   # - half_life: float (seconds)
   # - grams: float
   # - atoms: int
   # - activity: float (Bq)
   # - heat: float (W)
   # - alpha_heat: float (W)
   # - beta_heat: float (W)
   # - gamma_heat: float (W)
   # - dose: float (Sv/h)
   # - ingestion: float (Sv/Bq)
   # - inhalation: float (Sv/Bq)
   # - name: str (e.g., 'Fe56')

GammaSpectrum Object
~~~~~~~~~~~~~~~~~~~~

Contains gamma spectrum data:

.. code-block:: python

   # Properties:
   # - boundaries: List[float] (energy bin boundaries, length n+1)
   # - values: List[float] (spectrum values, length n)

DoseRate Object
~~~~~~~~~~~~~~~

Contains dose rate information:

.. code-block:: python

   # Properties:
   # - type: str (e.g., 'PLANE SOURCE')
   # - distance: float (cm)
   # - mass: float (g)
   # - dose: float (Sv/h)

Working with JSON
-----------------

All data structures support JSON serialization:

.. code-block:: python

   import pypact as pp
   import json

   with pp.Reader('myoutput.out') as output:
       # Serialize any object
       data = {
           'run': output.run_data.json_serialize(),
           'first_timestep': output[0].json_serialize(),
           'first_nuclide': output[0].nuclides[0].json_serialize()
       }
       
       # Write to file
       with open('output.json', 'w') as f:
           json.dump(data, f, indent=2)

Utility Functions
-----------------

Pypact provides various utility functions for common tasks.

File Record
~~~~~~~~~~~

The FileRecord class provides low-level access to output files:

.. code-block:: python

   import pypact as pp

   # Create a file record
   fr = pp.FileRecord('myoutput.out')
   
   # Use with other parsers
   dr = pp.DoseRate()
   dr.fispact_deserialize(fr, interval=2)

This is useful for selective parsing when you only need specific data 
and don't want to parse the entire file.
