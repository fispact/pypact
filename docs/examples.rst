Examples and Cookbooks
======================

This section provides practical examples and "cookbook" recipes for common tasks with pypact.

Quick Examples
--------------

Print Run Name
~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       print(output.run_data.run_name)

Loop Over Timesteps
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       for timestep in output.inventory_data:
           print(f"Time: {timestep.irradiation_time} s")
           print(f"Flux: {timestep.flux} n/cm²/s")
           print(f"Total heat: {timestep.total_heat} W")

Count Nuclides
~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       for timestep in output.inventory_data:
           print(f"Timestep has {len(timestep.nuclides)} nuclides")

Get Dominant Nuclides
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Sort by activity
       sorted_nuclides = sorted(timestep.nuclides, 
                               key=lambda n: n.activity, 
                               reverse=True)
       
       # Get top 10
       for i, nuc in enumerate(sorted_nuclides[:10], 1):
           print(f"{i}. {nuc.name}: {nuc.activity:.3e} Bq")

Output Analysis Recipes
-----------------------

Recipe 1: Decay Heat Over Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Track how decay heat changes during cooling:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   with pp.Reader('myoutput.out') as output:
       times = []
       heats = []
       
       for timestep in output.inventory_data:
           # Use cooling time (or total time)
           time = timestep.cooling_time if timestep.cooling_time > 0 else timestep.irradiation_time
           times.append(time)
           heats.append(timestep.total_heat)
       
       # Plot
       plt.figure(figsize=(10, 6))
       plt.loglog(times, heats, 'o-')
       plt.xlabel('Time (s)')
       plt.ylabel('Total Heat (W)')
       plt.title('Decay Heat Over Time')
       plt.grid(True)
       plt.show()

Recipe 2: Activity by Element
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sum activity for each element at a given timestep:

.. code-block:: python

   import pypact as pp
   from collections import defaultdict

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Sum activity by element
       activity_by_element = defaultdict(float)
       for nuclide in timestep.nuclides:
           activity_by_element[nuclide.element] += nuclide.activity
       
       # Sort by activity
       sorted_elements = sorted(activity_by_element.items(), 
                               key=lambda x: x[1], 
                               reverse=True)
       
       # Print top 10 elements
       for element, activity in sorted_elements[:10]:
           print(f"{element}: {activity:.3e} Bq")

Recipe 3: Fractional Contributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate what fraction each nuclide contributes to total heat:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       total_heat = timestep.total_heat
       
       # Calculate fractions
       contributions = []
       for nuclide in timestep.nuclides:
           fraction = nuclide.heat / total_heat
           contributions.append((nuclide.name, fraction))
       
       # Sort by contribution
       contributions.sort(key=lambda x: x[1], reverse=True)
       
       # Print nuclides contributing > 1%
       print("Nuclides contributing > 1% to heat:")
       for name, fraction in contributions:
           if fraction > 0.01:
               print(f"{name}: {fraction*100:.2f}%")

Recipe 4: Dose Rate Evolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Track dose rate over time:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   with pp.Reader('myoutput.out') as output:
       times = []
       doses = []
       
       for timestep in output.inventory_data:
           time = timestep.cooling_time if timestep.cooling_time > 0 else timestep.irradiation_time
           times.append(time)
           
           if timestep.dose_rate:
               doses.append(timestep.dose_rate.dose)
           else:
               doses.append(0.0)
       
       # Plot
       plt.figure(figsize=(10, 6))
       plt.loglog(times, doses, 'o-')
       plt.xlabel('Time (s)')
       plt.ylabel('Dose Rate (Sv/h)')
       plt.title('Dose Rate Evolution')
       plt.grid(True)
       plt.show()

Recipe 5: Compare Multiple Runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare results from different FISPACT-II runs:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   files = ['run1.out', 'run2.out', 'run3.out']
   labels = ['Case 1', 'Case 2', 'Case 3']
   
   plt.figure(figsize=(10, 6))
   
   for filename, label in zip(files, labels):
       with pp.Reader(filename) as output:
           times = []
           heats = []
           
           for timestep in output.inventory_data:
               time = timestep.cooling_time if timestep.cooling_time > 0 else timestep.irradiation_time
               times.append(time)
               heats.append(timestep.total_heat)
           
           plt.loglog(times, heats, 'o-', label=label)
   
   plt.xlabel('Time (s)')
   plt.ylabel('Total Heat (W)')
   plt.title('Decay Heat Comparison')
   plt.legend()
   plt.grid(True)
   plt.show()

Input File Creation Recipes
----------------------------

Recipe 6: Create Basic Input File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a simple FISPACT-II input file:

.. code-block:: python

   import pypact as pp

   # Create input data
   input_data = pp.InputData(name='my_run')
   
   # Basic setup
   input_data.overwriteExisting()
   input_data.enableJSON()
   input_data.readXSData(709)
   input_data.readDecayData()
   
   # Set material (steel example)
   input_data.setDensity(7.8)
   input_data.setMass(1.0)
   input_data.addElement('Fe', percentage=85.0)
   input_data.addElement('Cr', percentage=12.0)
   input_data.addElement('Ni', percentage=3.0)
   
   # Irradiation and cooling
   input_data.addIrradiation(time=3600.0, flux=1e14)
   input_data.addCooling(86400.0)  # 1 day
   input_data.addCooling(604800.0)  # 1 week
   
   # Validate and write
   input_data.validate()
   pp.to_file(input_data, 'my_run.i')

Recipe 7: Create Flux File
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a custom flux file:

.. code-block:: python

   import pypact as pp
   import numpy as np

   # Create flux data
   flux_data = pp.FluxesData()
   
   # Define energy groups (example: 3 groups)
   flux_data.num_groups = 3
   flux_data.boundaries = [1e-10, 1e-5, 1e0, 20.0]  # MeV
   flux_data.values = [1e13, 5e13, 2e13]  # n/cm²/s
   
   # Write to file
   pp.to_file(flux_data, 'myflux.flux')

Recipe 8: Create Files File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a files file (I/O paths):

.. code-block:: python

   import pypact as pp

   # Create files data
   files_data = pp.FilesData()
   
   # Set paths
   files_data.xs_library = '/path/to/xs_library'
   files_data.decay_library = '/path/to/decay_library'
   files_data.output = 'output.out'
   files_data.json_output = 'output.json'
   
   # Write to file
   pp.to_file(files_data, 'files')

Recipe 9: Modify Existing Input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read and modify an existing input file:

.. code-block:: python

   import pypact as pp

   # Read existing input
   input_data = pp.InputData.from_file('existing.i')
   
   # Modify parameters
   input_data.setMass(2.0)  # Change mass
   input_data.addCooling(1e6)  # Add cooling time
   
   # Write to new file
   input_data.validate()
   pp.to_file(input_data, 'modified.i')

Visualization Recipes
---------------------

Recipe 10: Plot Nuclide Inventory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize nuclide inventory as a bar chart:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Get top 20 nuclides by mass
       sorted_nuclides = sorted(timestep.nuclides, 
                               key=lambda n: n.grams, 
                               reverse=True)[:20]
       
       names = [n.name for n in sorted_nuclides]
       masses = [n.grams for n in sorted_nuclides]
       
       # Plot
       plt.figure(figsize=(12, 6))
       plt.bar(names, masses)
       plt.xlabel('Nuclide')
       plt.ylabel('Mass (g)')
       plt.title('Top 20 Nuclides by Mass')
       plt.xticks(rotation=45)
       plt.tight_layout()
       plt.show()

Recipe 11: Gamma Spectrum Plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Plot gamma spectrum:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt
   import numpy as np

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       gs = timestep.gamma_spectrum
       
       if gs and gs.values:
           # Calculate bin centers
           centers = [(gs.boundaries[i] + gs.boundaries[i+1]) / 2 
                     for i in range(len(gs.values))]
           
           # Plot
           plt.figure(figsize=(10, 6))
           plt.loglog(centers, gs.values, 'o-')
           plt.xlabel('Energy (MeV)')
           plt.ylabel('Gamma Intensity')
           plt.title('Gamma Spectrum')
           plt.grid(True)
           plt.show()

Recipe 12: Periodic Table Heatmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a periodic table heatmap of activity:

.. code-block:: python

   import pypact as pp
   import pypact.analysis as ppa
   import matplotlib.pyplot as plt
   from collections import defaultdict

   with pp.Reader('myoutput.out') as output:
       timestep = output[0]
       
       # Sum activity by element
       activity_by_z = defaultdict(float)
       for nuclide in timestep.nuclides:
           z = ppa.find_z(nuclide.element)
           activity_by_z[z] += nuclide.activity
       
       # Create visualization (simplified example)
       z_values = list(activity_by_z.keys())
       activities = list(activity_by_z.values())
       
       plt.figure(figsize=(12, 6))
       plt.scatter(z_values, activities, s=100)
       plt.xlabel('Atomic Number (Z)')
       plt.ylabel('Total Activity (Bq)')
       plt.title('Activity by Element')
       plt.yscale('log')
       plt.grid(True)
       plt.show()

Data Export Recipes
-------------------

Recipe 13: Export to CSV
~~~~~~~~~~~~~~~~~~~~~~~~

Export timestep data to CSV:

.. code-block:: python

   import pypact as pp
   import csv

   with pp.Reader('myoutput.out') as output:
       with open('output.csv', 'w', newline='') as csvfile:
           writer = csv.writer(csvfile)
           
           # Write header
           writer.writerow(['Element', 'Isotope', 'Mass (g)', 
                          'Activity (Bq)', 'Heat (W)'])
           
           # Write data for first timestep
           timestep = output[0]
           for nuclide in timestep.nuclides:
               writer.writerow([nuclide.element, nuclide.isotope, 
                              nuclide.grams, nuclide.activity, 
                              nuclide.heat])

Recipe 14: Export to JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~

Export complete output to JSON:

.. code-block:: python

   import pypact as pp
   import json

   with pp.Reader('myoutput.out') as output:
       data = {
           'run_name': output.run_data.run_name,
           'timestamp': output.run_data.timestamp,
           'timesteps': []
       }
       
       for timestep in output.inventory_data:
           data['timesteps'].append({
               'irradiation_time': timestep.irradiation_time,
               'cooling_time': timestep.cooling_time,
               'total_heat': timestep.total_heat,
               'nuclide_count': len(timestep.nuclides)
           })
       
       with open('output.json', 'w') as f:
           json.dump(data, f, indent=2)

Recipe 15: Generate Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a text report:

.. code-block:: python

   import pypact as pp

   with pp.Reader('myoutput.out') as output:
       with open('report.txt', 'w') as f:
           # Header
           f.write("FISPACT-II Analysis Report\n")
           f.write("=" * 50 + "\n\n")
           
           # Run info
           f.write(f"Run: {output.run_data.run_name}\n")
           f.write(f"Date: {output.run_data.timestamp}\n\n")
           
           # Summary for each timestep
           for i, timestep in enumerate(output.inventory_data):
               f.write(f"Timestep {i+1}\n")
               f.write("-" * 50 + "\n")
               f.write(f"Time: {timestep.irradiation_time} s\n")
               f.write(f"Nuclides: {len(timestep.nuclides)}\n")
               f.write(f"Total heat: {timestep.total_heat:.3e} W\n")
               f.write(f"Total activity: {sum(n.activity for n in timestep.nuclides):.3e} Bq\n\n")

Advanced Recipes
----------------

Recipe 16: Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Process multiple output files:

.. code-block:: python

   import pypact as pp
   import glob
   import pandas as pd

   results = []
   
   for filename in glob.glob('*.out'):
       with pp.Reader(filename) as output:
           # Extract key results
           final_timestep = output.inventory_data[-1]
           results.append({
               'filename': filename,
               'run_name': output.run_data.run_name,
               'final_heat': final_timestep.total_heat,
               'nuclide_count': len(final_timestep.nuclides)
           })
   
   # Create DataFrame
   df = pd.DataFrame(results)
   df.to_csv('batch_results.csv', index=False)
   print(df)

Recipe 17: Time-Dependent Isotope Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Track specific isotopes over time:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   isotopes_to_track = ['Co60', 'Fe55', 'Ni63']
   
   with pp.Reader('myoutput.out') as output:
       data = {iso: {'times': [], 'activities': []} 
               for iso in isotopes_to_track}
       
       for timestep in output.inventory_data:
           time = timestep.cooling_time if timestep.cooling_time > 0 else timestep.irradiation_time
           
           for iso in isotopes_to_track:
               activity = 0.0
               for nuclide in timestep.nuclides:
                   if nuclide.name == iso:
                       activity = nuclide.activity
                       break
               
               data[iso]['times'].append(time)
               data[iso]['activities'].append(activity)
       
       # Plot
       plt.figure(figsize=(10, 6))
       for iso in isotopes_to_track:
           plt.loglog(data[iso]['times'], data[iso]['activities'], 
                     'o-', label=iso)
       
       plt.xlabel('Time (s)')
       plt.ylabel('Activity (Bq)')
       plt.title('Isotope Activity Evolution')
       plt.legend()
       plt.grid(True)
       plt.show()

Recipe 18: Uncertainty Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare results with uncertainties:

.. code-block:: python

   import pypact as pp
   import numpy as np
   import matplotlib.pyplot as plt

   # Multiple runs with parameter variations
   runs = ['nominal.out', 'high.out', 'low.out']
   
   times_list = []
   heats_list = []
   
   for filename in runs:
       with pp.Reader(filename) as output:
           times = []
           heats = []
           for timestep in output.inventory_data:
               time = timestep.cooling_time if timestep.cooling_time > 0 else timestep.irradiation_time
               times.append(time)
               heats.append(timestep.total_heat)
           times_list.append(times)
           heats_list.append(heats)
   
   # Calculate mean and std
   heats_array = np.array(heats_list)
   mean_heats = np.mean(heats_array, axis=0)
   std_heats = np.std(heats_array, axis=0)
   
   # Plot with uncertainty band
   plt.figure(figsize=(10, 6))
   plt.loglog(times_list[0], mean_heats, 'o-', label='Mean')
   plt.fill_between(times_list[0], 
                     mean_heats - std_heats, 
                     mean_heats + std_heats, 
                     alpha=0.3, label='±1σ')
   plt.xlabel('Time (s)')
   plt.ylabel('Total Heat (W)')
   plt.title('Decay Heat with Uncertainty')
   plt.legend()
   plt.grid(True)
   plt.show()

More Examples
-------------

The pypact repository contains many more examples in the ``examples/`` directory:

- **Simple examples**: Basic usage patterns (examples/simple/)
- **Plotting examples**: Visualization techniques (examples/outputplotting/)
- **Input creation**: Creating FISPACT-II input files (examples/inputcreation/)
- **CSV export**: Exporting data to CSV format (examples/csv/)
- **PrintLib examples**: Working with PRINTLIB outputs (examples/printlib/)

You can find these at: https://github.com/fispact/pypact/tree/master/examples
