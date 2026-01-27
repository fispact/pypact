Group Conversion
================

Pypact provides utilities for converting data between different neutron energy group structures. 
This is essential when you need to process cross sections or flux data in different formats.

Overview
--------

FISPACT-II uses multi-group neutron cross section libraries with different energy group structures. 
Common structures include:

- **709 groups**: CCFE 709 group structure (default for fusion applications)
- **315 groups**: CCFE 315 group structure
- **175 groups**: VITAMIN-J 175 group structure
- **Custom structures**: User-defined energy group boundaries

The group conversion utilities help convert data between these different structures, which is 
useful when:

- Comparing results from different libraries
- Processing flux spectra from different sources
- Adapting cross section data for different applications

Basic Usage
-----------

Loading Group Structures
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.groupconvert as gc

   # Load a group structure from file
   # File format: one energy boundary per line (MeV)
   group_structure = gc.load_group_structure('mygroups.txt')
   
   print(f"Number of groups: {len(group_structure) - 1}")
   print(f"Energy range: {group_structure[0]} - {group_structure[-1]} MeV")

Group Structure Format
~~~~~~~~~~~~~~~~~~~~~~

Group structure files contain energy boundaries in MeV, one per line. 
For n groups, you need n+1 boundaries:

.. code-block:: text

   1.0e-10
   1.0e-9
   1.0e-8
   ...
   2.0e1

Converting Between Group Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.groupconvert as gc

   # Example: Convert flux spectrum from 709 to 315 groups
   flux_709 = [...]  # 709 values
   groups_709 = gc.load_group_structure('ccfe709.txt')
   groups_315 = gc.load_group_structure('ccfe315.txt')
   
   flux_315 = gc.convert_groups(flux_709, groups_709, groups_315)

Interpolation Methods
~~~~~~~~~~~~~~~~~~~~~~

The group conversion uses various interpolation methods depending on the data type:

.. code-block:: python

   import pypact.groupconvert as gc

   # Linear interpolation (default)
   converted = gc.convert_groups(data, from_groups, to_groups, 
                                 method='linear')
   
   # Logarithmic interpolation (for energy-dependent data)
   converted = gc.convert_groups(data, from_groups, to_groups, 
                                 method='log')

Working with Flux Data
----------------------

Converting Flux Spectra
~~~~~~~~~~~~~~~~~~~~~~~~

Flux spectra often need to be converted between group structures:

.. code-block:: python

   import pypact.groupconvert as gc
   import pypact as pp

   # Read flux from FISPACT input file
   input_data = pp.InputData.from_file('myinput.i')
   flux_values = input_data.flux_values
   
   # Convert to different group structure
   new_groups = gc.load_group_structure('new_structure.txt')
   converted_flux = gc.convert_groups(flux_values, 
                                      input_data.group_structure, 
                                      new_groups)

Normalizing Flux
~~~~~~~~~~~~~~~~

After conversion, you may need to normalize the flux:

.. code-block:: python

   import numpy as np

   # Normalize to total flux
   total_flux = np.sum(converted_flux)
   normalized_flux = converted_flux / total_flux * target_total

Collapsing Groups
~~~~~~~~~~~~~~~~~

Sometimes you want to reduce the number of groups by collapsing:

.. code-block:: python

   import pypact.groupconvert as gc

   # Collapse fine groups into coarser structure
   fine_groups = 709
   coarse_groups = 175
   
   collapsed_data = gc.collapse_groups(fine_data, 
                                       fine_structure, 
                                       coarse_structure)

Working with Cross Sections
----------------------------

Converting Cross Section Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cross sections can be converted between group structures:

.. code-block:: python

   import pypact.groupconvert as gc

   # Load cross section data in 709 groups
   xs_709 = load_cross_section_data()
   
   # Convert to 315 groups
   groups_709 = gc.load_group_structure('ccfe709.txt')
   groups_315 = gc.load_group_structure('ccfe315.txt')
   
   xs_315 = gc.convert_groups(xs_709, groups_709, groups_315)

Weighting by Flux
~~~~~~~~~~~~~~~~~

Cross sections are often weighted by flux during conversion:

.. code-block:: python

   import pypact.groupconvert as gc

   # Flux-weighted cross section conversion
   xs_converted = gc.convert_groups_weighted(xs_data, 
                                              from_groups, 
                                              to_groups,
                                              flux_spectrum)

Practical Examples
------------------

Example 1: Converting CCFE 709 to 315 Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.groupconvert as gc
   import numpy as np

   # Load group structures
   groups_709 = gc.load_group_structure('ccfe709.txt')
   groups_315 = gc.load_group_structure('ccfe315.txt')
   
   # Example flux data (709 groups)
   flux_709 = np.ones(709)  # Flat spectrum for demonstration
   
   # Convert
   flux_315 = gc.convert_groups(flux_709, groups_709, groups_315)
   
   print(f"Original groups: {len(flux_709)}")
   print(f"Converted groups: {len(flux_315)}")
   print(f"Total flux preserved: {np.sum(flux_709):.3e} vs {np.sum(flux_315):.3e}")

Example 2: Custom Group Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.groupconvert as gc
   import numpy as np

   # Define custom group structure (thermal to fast)
   custom_groups = np.logspace(-10, 1, 51)  # 50 groups
   
   # Load standard structure
   groups_709 = gc.load_group_structure('ccfe709.txt')
   
   # Convert data to custom structure
   custom_data = gc.convert_groups(standard_data, 
                                    groups_709, 
                                    custom_groups)

Example 3: Analyzing Group Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact.groupconvert as gc
   import matplotlib.pyplot as plt

   # Load group structure
   groups = gc.load_group_structure('ccfe709.txt')
   
   # Calculate group widths
   widths = [groups[i+1] - groups[i] for i in range(len(groups)-1)]
   
   # Plot group structure
   plt.figure(figsize=(10, 6))
   plt.semilogx(groups[:-1], widths)
   plt.xlabel('Energy (MeV)')
   plt.ylabel('Group Width (MeV)')
   plt.title('CCFE 709 Group Structure')
   plt.grid(True)
   plt.show()

Validation and Checks
---------------------

Checking Conservation
~~~~~~~~~~~~~~~~~~~~~

After conversion, verify that important quantities are conserved:

.. code-block:: python

   import pypact.groupconvert as gc
   import numpy as np

   # Convert data
   converted = gc.convert_groups(original, from_groups, to_groups)
   
   # Check conservation (e.g., total flux)
   original_total = np.sum(original)
   converted_total = np.sum(converted)
   
   relative_error = abs(converted_total - original_total) / original_total
   print(f"Relative error: {relative_error:.2e}")
   
   if relative_error > 1e-3:
       print("WARNING: Significant error in conversion!")

Boundary Alignment
~~~~~~~~~~~~~~~~~~

Check if group boundaries are aligned:

.. code-block:: python

   import pypact.groupconvert as gc

   def check_alignment(groups1, groups2, tolerance=1e-6):
       """Check if group structures have aligned boundaries"""
       aligned = []
       for b1 in groups1:
           for b2 in groups2:
               if abs(b1 - b2) < tolerance:
                   aligned.append(b1)
                   break
       return aligned

   groups_709 = gc.load_group_structure('ccfe709.txt')
   groups_315 = gc.load_group_structure('ccfe315.txt')
   
   aligned = check_alignment(groups_709, groups_315)
   print(f"Number of aligned boundaries: {len(aligned)}")

Advanced Topics
---------------

Energy Binning
~~~~~~~~~~~~~~

Understanding how energy bins work in multi-group calculations:

.. code-block:: python

   import numpy as np

   # Group boundaries (n+1 values for n groups)
   boundaries = [0.0, 1.0, 10.0, 100.0]  # 3 groups
   
   # Group values (n values)
   values = [1.0, 2.0, 3.0]
   
   # Each value corresponds to the interval:
   # values[0] -> [boundaries[0], boundaries[1]]
   # values[1] -> [boundaries[1], boundaries[2]]
   # values[2] -> [boundaries[2], boundaries[3]]

Lethargy Representation
~~~~~~~~~~~~~~~~~~~~~~~

Sometimes data is represented in lethargy rather than energy:

.. code-block:: python

   import numpy as np

   def energy_to_lethargy(energy, e_ref=1.0):
       """Convert energy to lethargy"""
       return np.log(e_ref / energy)

   def lethargy_to_energy(lethargy, e_ref=1.0):
       """Convert lethargy to energy"""
       return e_ref * np.exp(-lethargy)

   # Convert group structure to lethargy
   energy_groups = [1e-10, 1e-5, 1e0, 1e1]
   lethargy_groups = [energy_to_lethargy(e) for e in energy_groups]

Flux Weighting
~~~~~~~~~~~~~~

Proper flux weighting for cross section conversion:

.. code-block:: python

   import numpy as np

   def flux_weighted_average(xs, flux, boundaries):
       """Calculate flux-weighted average cross section"""
       total_flux = np.sum(flux)
       weighted_xs = np.sum(xs * flux) / total_flux
       return weighted_xs

Best Practices
--------------

1. **Always validate conversions**: Check conservation of important quantities
2. **Document group structures**: Keep clear records of which structures you're using
3. **Use appropriate interpolation**: Linear for cross sections, logarithmic for energy-dependent quantities
4. **Consider flux weighting**: When converting cross sections, flux weighting is usually needed
5. **Check boundary alignment**: Conversions work better when boundaries are aligned

Common Pitfalls
---------------

1. **Off-by-one errors**: Remember that n groups require n+1 boundaries
2. **Energy ordering**: Ensure boundaries are in correct order (usually descending in FISPACT)
3. **Units**: Keep track of energy units (eV, keV, MeV)
4. **Normalization**: Check if normalization is preserved after conversion
5. **Interpolation artifacts**: Fine structure may be lost in coarse conversions

Resources
---------

Standard Group Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~

- CCFE 709 groups: Standard for fusion neutronics
- CCFE 315 groups: Reduced structure for faster calculations
- VITAMIN-J 175 groups: Common in fission applications
- WIMS 69 groups: Used in reactor physics

For more information on these structures, consult the FISPACT-II documentation.
