Quick Start Guide
=================

This guide will help you get started with pypact quickly.

Installation
------------

Pypact requires Python 3.8 or later and has minimal dependencies (only numpy).

Using pip
~~~~~~~~~

The easiest way to install pypact is using pip:

.. code-block:: bash

   pip3 install pypact

From Source
~~~~~~~~~~~

Alternatively, you can install from source:

.. code-block:: bash

   git clone https://github.com/fispact/pypact
   cd pypact
   pip3 install .

Verify Installation
~~~~~~~~~~~~~~~~~~~

After installation, verify that pypact is installed correctly:

.. code-block:: bash

   # Check the command-line tool
   fispactconverter.py -h

   # Or in Python
   python3 -c "import pypact; print('pypact version:', pypact.__version__)"

Your First pypact Script
-------------------------

Let's create a simple script to read a FISPACT-II output file.

Step 1: Import pypact
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

Step 2: Read an Output File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   # Read a FISPACT-II output file
   with pp.Reader('myoutput.out') as output:
       # Print run information
       print(f"Run name: {output.run_data.run_name}")
       print(f"Timestamp: {output.run_data.timestamp}")
       
       # Print number of timesteps
       print(f"Number of timesteps: {len(output.inventory_data)}")

Step 3: Access Timestep Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       # Get the first timestep
       timestep = output[0]
       
       # Print key properties
       print(f"Irradiation time: {timestep.irradiation_time} s")
       print(f"Total heat: {timestep.total_heat} W")
       print(f"Number of nuclides: {len(timestep.nuclides)}")

Step 4: Work with Nuclides
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Loop through nuclides
       for nuclide in timestep.nuclides[:5]:  # First 5 nuclides
           print(f"{nuclide.name}: {nuclide.grams:.3e} g, {nuclide.activity:.3e} Bq")

Common Tasks
------------

Reading Different File Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pypact can read both standard .out files and JSON output:

.. code-block:: python

   import pypact as pp

   # Standard output file
   with pp.Reader('output.out') as output:
       print("Standard output")
   
   # JSON output (FISPACT-II 4.0+)
   with pp.Reader('output.json') as output:
       print("JSON output")

Looping Over Timesteps
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       for i, timestep in enumerate(output.inventory_data):
           print(f"Timestep {i+1}:")
           print(f"  Time: {timestep.irradiation_time} s")
           print(f"  Heat: {timestep.total_heat} W")

Finding Dominant Nuclides
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Sort by activity
       sorted_nuclides = sorted(timestep.nuclides, 
                               key=lambda n: n.activity, 
                               reverse=True)
       
       # Print top 10
       print("Top 10 nuclides by activity:")
       for i, nuc in enumerate(sorted_nuclides[:10], 1):
           print(f"{i}. {nuc.name}: {nuc.activity:.3e} Bq")

Converting to JSON
~~~~~~~~~~~~~~~~~~

Export data to JSON format:

.. code-block:: python

   import pypact as pp
   import json

   with pp.Reader('myoutput.out') as output:
       # Serialize run data
       run_json = output.run_data.json_serialize()
       
       # Serialize a timestep
       timestep_json = output[0].json_serialize()
       
       # Write to file
       with open('output.json', 'w') as f:
           json.dump(timestep_json, f, indent=2)

Or use the command-line tool:

.. code-block:: bash

   fispactconverter.py myoutput.out myoutput.json

Simple Visualization
~~~~~~~~~~~~~~~~~~~~

Create a basic plot of decay heat:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   with pp.Reader('myoutput.out') as output:
       times = []
       heats = []
       
       for timestep in output.inventory_data:
           time = timestep.cooling_time if timestep.cooling_time > 0 else timestep.irradiation_time
           times.append(time)
           heats.append(timestep.total_heat)
       
       plt.figure(figsize=(10, 6))
       plt.loglog(times, heats, 'o-')
       plt.xlabel('Time (s)')
       plt.ylabel('Total Heat (W)')
       plt.title('Decay Heat Over Time')
       plt.grid(True)
       plt.show()

Creating Input Files
--------------------

Pypact can also create FISPACT-II input files.

Basic Input File
~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   # Create input data
   input_data = pp.InputData(name='my_run')
   
   # Basic configuration
   input_data.overwriteExisting()
   input_data.enableJSON()
   input_data.readXSData(709)
   input_data.readDecayData()
   
   # Set material (example: steel)
   input_data.setDensity(7.8)  # g/cm³
   input_data.setMass(1.0)     # kg
   input_data.addElement('Fe', percentage=85.0)
   input_data.addElement('Cr', percentage=12.0)
   input_data.addElement('Ni', percentage=3.0)
   
   # Add irradiation
   input_data.addIrradiation(time=3600.0, flux=1e14)  # 1 hour, 10^14 n/cm²/s
   
   # Add cooling times
   input_data.addCooling(86400.0)    # 1 day
   input_data.addCooling(604800.0)   # 1 week
   input_data.addCooling(2592000.0)  # 30 days
   
   # Validate and write
   input_data.validate()
   pp.to_file(input_data, 'my_run.i')

Command-Line Tools
------------------

File Converter
~~~~~~~~~~~~~~

Convert FISPACT-II output to JSON:

.. code-block:: bash

   fispactconverter.py input.out output.json

This creates a JSON file that can be easily parsed by other tools or programming languages.

Working with Test Files
-----------------------

The pypact repository includes test files in the ``reference/`` directory that you can use 
to practice:

.. code-block:: python

   import pypact as pp
   import os

   # Path to test file (adjust as needed)
   test_file = os.path.join('reference', 'test91.out')
   
   with pp.Reader(test_file) as output:
       print(f"Run: {output.run_data.run_name}")
       print(f"Timesteps: {len(output.inventory_data)}")

Best Practices
--------------

1. **Use context managers**: Always use ``with`` statements when reading files:

   .. code-block:: python

      with pp.Reader('myfile.out') as output:
          # Your code here
          pass

2. **Check data availability**: Not all properties are available in all outputs:

   .. code-block:: python

      if timestep.dose_rate:
          print(f"Dose: {timestep.dose_rate.dose}")

3. **Handle large files**: For very large files, consider processing timesteps sequentially 
   rather than loading everything into memory.

4. **Validate input files**: Always validate input files before writing:

   .. code-block:: python

      input_data.validate()
      pp.to_file(input_data, 'myfile.i')

Common Errors and Solutions
----------------------------

File Not Found
~~~~~~~~~~~~~~

**Error**: ``FileNotFoundError: [Errno 2] No such file or directory: 'myfile.out'``

**Solution**: Make sure the file path is correct. Use absolute paths if needed:

.. code-block:: python

   import os
   
   filepath = os.path.abspath('myfile.out')
   with pp.Reader(filepath) as output:
       pass

Invalid File Format
~~~~~~~~~~~~~~~~~~~

**Error**: ``ValueError: Invalid FISPACT-II output format``

**Solution**: Make sure the file is a valid FISPACT-II output file. Check that FISPACT-II 
completed successfully.

Missing Dependencies
~~~~~~~~~~~~~~~~~~~~

**Error**: ``ModuleNotFoundError: No module named 'numpy'``

**Solution**: Install required dependencies:

.. code-block:: bash

   pip3 install numpy

Next Steps
----------

Now that you've learned the basics, you can:

1. Explore the :doc:`examples` section for more complex use cases
2. Read the :doc:`parsers` documentation for detailed API information
3. Learn about :doc:`libraries` for advanced analysis
4. Check out the GitHub repository for more examples: https://github.com/fispact/pypact/tree/master/examples

Tips for Learning
-----------------

- **Start simple**: Begin with basic file reading and gradually add complexity
- **Use examples**: The examples directory has many working examples
- **Check the data**: Print data structures to understand what's available
- **Read the code**: Pypact is open source - reading the source can help you understand it better

Getting Help
------------

If you need help:

1. Check the documentation: https://pypact.readthedocs.io
2. Look at examples: https://github.com/fispact/pypact/tree/master/examples
3. Open an issue: https://github.com/fispact/pypact/issues
4. Contact FISPACT team: https://fispact.ukaea.uk/contact

What's Next?
------------

Try modifying the examples above with your own FISPACT-II output files. Experiment with:

- Different ways to filter nuclides
- Creating plots of various properties
- Exporting data in different formats
- Creating your own input files

Happy analyzing!
