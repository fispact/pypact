Parsers
=======

Pypact provides several parsers to read different types of FISPACT-II output files.

Standard Output Parser
----------------------

The most commonly used parser is the ``Reader`` class which parses the standard FISPACT-II output file (.out).

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   # Read a FISPACT-II output file
   with pp.Reader('myoutput.out') as output:
       # Access run data
       print(output.run_data.run_name)
       print(output.run_data.timestamp)
       
       # Access inventory data at different timesteps
       for timestep in output.inventory_data:
           print(f"Time: {timestep.irradiation_time} s")
           print(f"Total heat: {timestep.total_heat} W")

Accessing Timestep Data
~~~~~~~~~~~~~~~~~~~~~~~~

You can access timestep data by index:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       # Get the first timestep
       first_timestep = output[0]
       
       # Get nuclides at this timestep
       for nuclide in first_timestep.nuclides:
           print(f"{nuclide.element}{nuclide.isotope}: {nuclide.grams} g")

Run Data
~~~~~~~~

The run data contains metadata about the FISPACT-II run:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       rd = output.run_data
       print(f"Run name: {rd.run_name}")
       print(f"Timestamp: {rd.timestamp}")
       print(f"Flux name: {rd.flux_name}")

Inventory Data
~~~~~~~~~~~~~~

Each timestep contains inventory data with various properties:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       for timestep in output.inventory_data:
           print(f"Irradiation time: {timestep.irradiation_time} s")
           print(f"Cooling time: {timestep.cooling_time} s")
           print(f"Flux: {timestep.flux} n/cm²/s")
           print(f"Total heat: {timestep.total_heat} W")
           print(f"Alpha heat: {timestep.alpha_heat} W")
           print(f"Beta heat: {timestep.beta_heat} W")
           print(f"Gamma heat: {timestep.gamma_heat} W")
           print(f"Ingestion dose: {timestep.ingestion_dose} Sv")
           print(f"Inhalation dose: {timestep.inhalation_dose} Sv")

Nuclide Data
~~~~~~~~~~~~

Each timestep contains a list of nuclides with their properties:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       for nuclide in timestep.nuclides:
           print(f"Element: {nuclide.element}")
           print(f"Isotope: {nuclide.isotope}")
           print(f"State: {nuclide.state}")
           print(f"Half-life: {nuclide.half_life} s")
           print(f"Grams: {nuclide.grams} g")
           print(f"Activity: {nuclide.activity} Bq")
           print(f"Heat: {nuclide.heat} W")
           print(f"Alpha heat: {nuclide.alpha_heat} W")
           print(f"Beta heat: {nuclide.beta_heat} W")
           print(f"Gamma heat: {nuclide.gamma_heat} W")

Gamma Spectrum
~~~~~~~~~~~~~~

Pypact can parse gamma spectrum data from the output:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       gs = timestep.gamma_spectrum
       
       # Boundaries has n+1 elements for n bins
       print(f"Number of bins: {len(gs.values)}")
       print(f"Boundaries: {gs.boundaries}")
       print(f"Values: {gs.values}")

Dose Rate Data
~~~~~~~~~~~~~~

Dose rate information is available at each timestep:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       dr = timestep.dose_rate
       
       print(f"Type: {dr.type}")
       print(f"Distance: {dr.distance} cm")
       print(f"Mass: {dr.mass} g")
       print(f"Dose: {dr.dose} Sv/h")

JSON Output Parser
------------------

FISPACT-II version 4.0+ can produce JSON output which provides higher precision:

.. code-block:: python

   import pypact as pp

   # Read JSON output file
   with pp.Reader('myoutput.json') as output:
       # Same API as standard output
       for timestep in output.inventory_data:
           print(timestep.total_heat)

PrintLib Parsers
----------------

Pypact provides specialized parsers for PRINTLIB output files.

PrintLib 4 Parser
~~~~~~~~~~~~~~~~~

PRINTLIB 4 provides collapsed cross section data:

.. code-block:: python

   import pypact as pp

   # Read PRINTLIB 4 output
   with pp.PrintLib4Reader('printlib4.out') as output:
       # Process cross section data
       for data in output.cross_section_data:
           print(data.json_serialize())

PrintLib 5 Parser
~~~~~~~~~~~~~~~~~

PRINTLIB 5 provides spectral line data for gamma spectroscopy:

.. code-block:: python

   import pypact as pp

   # Read PRINTLIB 5 output
   with pp.PrintLib5Reader('printlib5.out') as output:
       # Get spectral data
       for spectrum in output.spectral_data:
           # Filter for specific isotopes (e.g., U-235)
           if spectrum.zai == 922350:
               print(f"ZAI: {spectrum.zai}")
               print(spectrum.json_serialize())

Example: Plotting Spectral Lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   with pp.PrintLib5Reader('printlib5.out') as output:
       for spectrum in output.spectral_data:
           if spectrum.zai == 922350:  # U-235
               # Plot the spectral lines
               energies = [line.energy for line in spectrum.lines]
               intensities = [line.intensity for line in spectrum.lines]
               
               plt.figure(figsize=(10, 6))
               plt.bar(energies, intensities, width=0.1)
               plt.xlabel('Energy (MeV)')
               plt.ylabel('Intensity')
               plt.title('U-235 Gamma Spectrum')
               plt.show()

JSON Serialization
------------------

All parsed data can be serialized to JSON format:

.. code-block:: python

   import pypact as pp
   import json

   with pp.Reader('myoutput.out') as output:
       # Serialize run data to JSON
       run_data_json = output.run_data.json_serialize()
       print(json.dumps(run_data_json, indent=2))
       
       # Serialize a timestep to JSON
       timestep_json = output[0].json_serialize()
       print(json.dumps(timestep_json, indent=2))
       
       # Serialize a nuclide to JSON
       nuclide_json = output[0].nuclides[0].json_serialize()
       print(json.dumps(nuclide_json, indent=2))

File Converter Tool
-------------------

Pypact includes a command-line tool to convert FISPACT-II output to JSON:

.. code-block:: bash

   # Convert output file to JSON
   fispactconverter.py myoutput.out myoutput.json

This is useful for:

- Converting output files for use in other tools
- Preserving output data in a structured format
- Sharing results in a more accessible format

Accuracy Considerations
-----------------------

When using pypact to parse standard .out files, be aware that the precision is limited 
by the output format. For example, nuclide heats are typically given to 3-4 significant 
figures in the .out file.

For higher precision (approximately 16 significant figures), use the JSON output format 
available in FISPACT-II version 4.0+. This uses double precision and provides more 
accurate results for complex calculations.

Example comparison:

**Standard .out file (parsed by pypact):**

.. code-block:: json

   {
       "element": "Si",
       "isotope": 31,
       "heat": 5.046e-14
   }

**JSON output (from FISPACT-II):**

.. code-block:: json

   {
       "element": "Si",
       "isotope": 31,
       "heat": 0.50459332881338111E-13
   }
