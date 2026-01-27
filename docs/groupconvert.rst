Group Conversion
================

Pypact provides utilities for converting flux data between different neutron energy group structures. 
This is essential when you need to process flux spectra in different formats.

Overview
--------

FISPACT-II uses multi-group neutron cross section libraries with different energy group structures. 
Pypact includes predefined structures in the ``ALL_GROUPS`` dictionary:

- **709 groups**: CCFE 709 group structure (default for fusion applications)
- **315 groups**: CCFE 315 group structure
- **175 groups**: VITAMIN-J 175 group structure
- **172 groups**: VITAMIN-J 172 group structure
- **69 groups**: WIMS 69 group structure
- **66 groups**: WIMS 66 group structure

The group conversion utilities help convert flux data between these different structures.

**Note**: Group boundaries in pypact are stored in **descending energy order** (highest energy first), 
as per FISPACT-II convention.

Basic Usage
-----------

Accessing Group Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pypact as pp

   # Get predefined group structures
   groups_709 = pp.ALL_GROUPS[709]  # 709 group boundaries (descending)
   groups_315 = pp.ALL_GROUPS[315]  # 315 group boundaries
   groups_175 = pp.ALL_GROUPS[175]  # 175 group boundaries
   
   # Note: boundaries are in descending order (highest energy first)
   print(f"709 groups: {len(groups_709)} boundaries (710 values)")
   print(f"Highest energy: {groups_709[0]} eV")
   print(f"Lowest energy: {groups_709[-1]} eV")
   
   # To get ascending order, reverse the list
   groups_709_ascending = list(reversed(groups_709))

Conversion Methods
~~~~~~~~~~~~~~~~~~

Pypact provides two conversion methods via ``pypact.groupconvert``:

1. **by_energy**: Converts using energy weighting (width of energy bins)
2. **by_lethargy**: Converts using lethargy weighting (logarithmic energy bins)

.. code-block:: python

   import pypact as pp

   # Input flux data (66 groups)
   input_boundaries = pp.ALL_GROUPS[66]  # Descending order
   input_values = [...]  # 66 flux values
   
   # Output structure (709 groups)
   output_boundaries = pp.ALL_GROUPS[709]  # Descending order
   
   # Convert using energy weighting
   output_values_energy = pp.groupconvert.by_energy(
       input_boundaries, 
       input_values, 
       output_boundaries
   )
   
   # Convert using lethargy weighting
   output_values_lethargy = pp.groupconvert.by_lethargy(
       input_boundaries,
       input_values,
       output_boundaries
   )

Working with Flux Files
-----------------------

Converting Flux Spectra
~~~~~~~~~~~~~~~~~~~~~~~~

The most common use case is converting flux spectra between group structures:

.. code-block:: python

   import pypact as pp

   # Read an arbitrary flux file (e.g., 66 groups)
   input_flux = pp.ArbFluxesFile()
   pp.from_file(input_flux, 'fluxes66.in')
   
   # Convert to 709 groups using lethargy weighting
   output_group = 709
   output_boundaries = list(reversed(pp.ALL_GROUPS[output_group]))
   
   output_values = pp.groupconvert.by_lethargy(
       input_flux.boundaries,
       input_flux.values,
       output_boundaries
   )
   
   # Create output flux file
   output_flux = pp.FluxesFile()
   output_flux.setGroup(output_group)
   output_flux.values = output_values

Energy vs Lethargy Weighting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The choice between energy and lethargy weighting depends on your application:

- **by_energy**: Uses linear energy bin widths for weighting
  
  .. math::
     
     w = \Delta E = E_{upper} - E_{lower}

- **by_lethargy**: Uses logarithmic (lethargy) bin widths for weighting
  
  .. math::
     
     w = \Delta u = \ln(E_{upper}/E_{lower})

For most nuclear applications, **lethargy weighting** is preferred as it better represents 
the logarithmic nature of neutron energy distributions.

.. code-block:: python

   import pypact as pp

   # Example: Compare both methods
   input_boundaries = pp.ALL_GROUPS[66]
   input_values = [1.0] * 66  # Flat spectrum
   output_boundaries = list(reversed(pp.ALL_GROUPS[709]))
   
   # Energy weighting
   values_energy = pp.groupconvert.by_energy(
       input_boundaries, input_values, output_boundaries
   )
   
   # Lethargy weighting (recommended)
   values_lethargy = pp.groupconvert.by_lethargy(
       input_boundaries, input_values, output_boundaries
   )

Practical Examples
------------------

Example 1: Converting 66 to 709 Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complete example showing how to convert flux from 66 to 709 groups:

.. code-block:: python

   import pypact as pp

   # Read input flux file (66 groups)
   input_flux = pp.ArbFluxesFile()
   pp.from_file(input_flux, 'fluxes66.in')
   
   # Setup output group structure
   output_group = 709
   output_boundaries = list(reversed(pp.ALL_GROUPS[output_group]))
   
   # Convert using lethargy (recommended for neutron spectra)
   output_values = pp.groupconvert.by_lethargy(
       input_flux.boundaries,
       input_flux.values,
       output_boundaries
   )
   
   # Create and save output flux file
   output_flux = pp.FluxesFile()
   output_flux.setGroup(output_group)
   output_flux.values = output_values
   pp.to_file(output_flux, 'fluxes709.in')
   
   print(f"Converted {len(input_flux.values)} groups to {len(output_values)} groups")

Example 2: Comparing Conversion Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare energy vs lethargy weighting visually:

.. code-block:: python

   import pypact as pp
   import matplotlib.pyplot as plt

   # Load input flux
   input_flux = pp.ArbFluxesFile()
   pp.from_file(input_flux, 'fluxes66.in')
   
   # Convert using both methods
   output_boundaries = list(reversed(pp.ALL_GROUPS[709]))
   
   values_energy = pp.groupconvert.by_energy(
       input_flux.boundaries, input_flux.values, output_boundaries
   )
   
   values_lethargy = pp.groupconvert.by_lethargy(
       input_flux.boundaries, input_flux.values, output_boundaries
   )
   
   # Plot comparison
   plt.figure(figsize=(10, 6))
   plt.loglog(output_boundaries[:-1], values_energy, 'r-', label='Energy weighting')
   plt.loglog(output_boundaries[:-1], values_lethargy, 'b-', label='Lethargy weighting')
   plt.xlabel('Energy (eV)')
   plt.ylabel('Flux (normalized)')
   plt.legend()
   plt.grid(True)
   plt.show()

Example 3: Creating Helper Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create reusable conversion functions:

.. code-block:: python

   import pypact as pp

   def convert_flux_to_group(input_flux, target_group, use_lethargy=True):
       """
       Convert a flux file to a target group structure.
       
       Parameters
       ----------
       input_flux : ArbFluxesFile or FluxesFile
           Input flux with boundaries and values
       target_group : int
           Target group structure (e.g., 709, 315, 175)
       use_lethargy : bool, optional
           Use lethargy weighting if True, energy if False
       
       Returns
       -------
       FluxesFile
           Converted flux file
       """
       # Get target boundaries in ascending order
       output_boundaries = list(reversed(pp.ALL_GROUPS[target_group]))
       
       # Choose conversion method
       convert_func = pp.groupconvert.by_lethargy if use_lethargy else pp.groupconvert.by_energy
       
       # Convert
       output_values = convert_func(
           input_flux.boundaries,
           input_flux.values,
           output_boundaries
       )
       
       # Create output flux file
       output_flux = pp.FluxesFile()
       output_flux.setGroup(target_group)
       output_flux.values = output_values
       
       return output_flux

   # Usage
   input_flux = pp.ArbFluxesFile()
   pp.from_file(input_flux, 'myflux.in')
   
   flux_709 = convert_flux_to_group(input_flux, 709)
   flux_315 = convert_flux_to_group(input_flux, 315)

Validation and Checks
---------------------

Checking Conservation
~~~~~~~~~~~~~~~~~~~~~

After conversion, verify that flux is conserved:

.. code-block:: python

   import pypact as pp
   import numpy as np

   # Perform conversion
   output_values = pp.groupconvert.by_lethargy(
       input_boundaries, input_values, output_boundaries
   )
   
   # Check total flux conservation
   input_total = sum(input_values)
   output_total = sum(output_values)
   
   relative_error = abs(output_total - input_total) / input_total
   print(f"Relative error: {relative_error:.2e}")
   
   if relative_error > 1e-6:
       print("WARNING: Flux not well conserved!")

Understanding Group Boundaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remember that group boundaries are in descending order:

.. code-block:: python

   import pypact as pp

   # Get group structure
   groups_709 = pp.ALL_GROUPS[709]
   
   print(f"Number of boundaries: {len(groups_709)}")
   print(f"Number of groups: {len(groups_709) - 1}")
   print(f"Highest energy: {groups_709[0]} eV ({groups_709[0]/1e6:.2f} MeV)")
   print(f"Lowest energy: {groups_709[-1]} eV ({groups_709[-1]:.2e} eV)")
   
   # Verify descending order
   assert all(groups_709[i] > groups_709[i+1] for i in range(len(groups_709)-1))
   print("✓ Boundaries in descending order")

Available Group Structures
--------------------------

Standard Group Structures
~~~~~~~~~~~~~~~~~~~~~~~~~

Pypact includes these predefined group structures in ``ALL_GROUPS``:

.. code-block:: python

   import pypact as pp

   # List all available group structures
   available_groups = list(pp.ALL_GROUPS.keys())
   print(f"Available group structures: {available_groups}")
   
   # Access specific group structures
   groups_709 = pp.ALL_GROUPS[709]  # CCFE 709 (fusion)
   groups_315 = pp.ALL_GROUPS[315]  # CCFE 315 (fusion)
   groups_175 = pp.ALL_GROUPS[175]  # VITAMIN-J 175 (fission)
   groups_172 = pp.ALL_GROUPS[172]  # VITAMIN-J 172 (fission)
   groups_69 = pp.ALL_GROUPS[69]    # WIMS 69 (reactor)
   groups_66 = pp.ALL_GROUPS[66]    # WIMS 66 (reactor)

Each group structure list has n+1 boundaries for n groups, representing the energy bounds 
for each bin.

Common Applications
~~~~~~~~~~~~~~~~~~~

- **CCFE 709/315 groups**: Standard for fusion neutronics calculations
- **VITAMIN-J 175/172 groups**: Common in fission reactor applications
- **WIMS 69/66 groups**: Used in reactor physics and fuel cycle calculations

Best Practices
--------------

1. **Use lethargy weighting**: For neutron flux spectra, lethargy weighting (``by_lethargy``) 
   is generally more appropriate than energy weighting.

2. **Check energy ordering**: Remember that pypact uses descending energy order (highest first). 
   Reverse with ``list(reversed(boundaries))`` if you need ascending order.

3. **Validate conversions**: Always check that total flux is conserved after conversion.

4. **Group compatibility**: When converting between very different group structures 
   (e.g., 66 to 709), expect some interpolation artifacts in regions with rapid flux changes.

5. **Document conversions**: Keep clear records of which conversion method (energy vs lethargy) 
   you used for reproducibility.

Common Pitfalls
---------------

1. **Wrong energy order**: Not reversing boundaries when needed
2. **Off-by-one errors**: Forgetting that n groups require n+1 boundaries
3. **Wrong weighting**: Using energy weighting when lethargy is more appropriate
4. **Units**: Mixing energy units (eV vs MeV) - pypact uses eV

Algorithm Details
-----------------

The conversion algorithms work by calculating the overlap between input and output 
energy bins and distributing the flux proportionally.

Energy Weighting
~~~~~~~~~~~~~~~~

For each output bin, the contribution from each overlapping input bin is weighted 
by the fractional overlap in energy:

.. code-block:: python

   overlap_contribution = (overlap_width / input_bin_width) * input_value

Lethargy Weighting
~~~~~~~~~~~~~~~~~~

For lethargy weighting, the overlap is weighted by the logarithmic ratio:

.. code-block:: python

   overlap_contribution = (overlap_lethargy / input_bin_lethargy) * input_value
   # where lethargy = log(E_upper / E_lower)

This better preserves the flux shape for logarithmically-spaced energy bins, 
which is typical in neutron physics.

References
----------

For more information on group structures and their applications:

- FISPACT-II Manual: Documentation on supported group structures
- VITAMIN-J: Cross section library documentation
- WIMS: Reactor physics code documentation

See also the example at: ``examples/groupconvert/66_to_709_compare.py`` in the pypact repository.

