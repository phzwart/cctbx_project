# CCTBX ADP Restraints Module

## Overview

The `cctbx.adp_restraints` module provides comprehensive functionality for handling Anisotropic Displacement Parameter (ADP) restraints in crystallographic refinement. This module is essential for maintaining physically reasonable atomic displacement parameters during structure refinement, ensuring that thermal motion parameters follow expected patterns and relationships.

The module supports multiple types of ADP restraints:
- **ADP Similarity**: Ensures similar atoms have similar displacement parameters
- **Rigid Bond**: Enforces rigid bond constraints on thermal motion
- **Isotropic ADP**: Converts anisotropic to isotropic displacement parameters
- **Fixed Ueq**: Maintains equivalent isotropic displacement parameters
- **RIGU**: Rigid bond restraints with additional constraints

## Architecture

The module follows a layered architecture with three main components:

1. **Core Classes** (`flags.py`, `energies.py`): Provide high-level management and energy calculations
2. **Restraint Types** (`__init__.py`): Define specific restraint implementations with injected methods
3. **C++ Extensions**: Low-level computational kernels for performance-critical operations

### Data Flow
```
Input: X-ray structure + restraint parameters
    ↓
Flags management (enable/disable restraint types)
    ↓
Energy calculation (compute residuals and gradients)
    ↓
Output: Refined ADP parameters + statistics
```

## Key Components

### flags Class
**Purpose**: Manages boolean flags that control which types of ADP restraints are active during refinement.

**Key Functions**:
- `__init__(adp_similarity, rigid_bond, isotropic_adp, default)`: Initialize restraint flags
- `show(f)`: Display current flag values

**Input/Output**: Boolean flags for restraint types
**Dependencies**: `libtbx.adopt_init_args`

### energies Class
**Purpose**: Computes and manages ADP restraint energies, handling multiple restraint types simultaneously.

**Key Functions**:
- `__init__(u_cart, u_iso, use_u_aniso, sites_cart, proxies...)`: Initialize energy calculation
- `adp_similarity_deviation()`: Calculate ADP similarity statistics
- `rigid_bond_deviation()`: Calculate rigid bond statistics  
- `isotropic_adp_deviation()`: Calculate isotropic ADP statistics
- `show(f, prefix)`: Display energy statistics
- `finalize_target_and_gradients()`: Apply normalization

**Input/Output**: ADP parameters → Energy values and gradients
**Dependencies**: `cctbx.array_family.flex`, `cctbx.adp_restraints`

### energies_iso Class
**Purpose**: Specialized class for computing isotropic ADP restraint energies with local sphere constraints.

**Key Functions**:
- `__init__(plain_pair_sym_table, xray_structure, parameters, ...)`: Initialize isotropic restraints

**Input/Output**: X-ray structure → Isotropic ADP energies
**Dependencies**: `scitbx.restraints.energies`, `cctbx.crystal`

### adp_aniso_restraints Class
**Purpose**: Handles anisotropic ADP restraints with support for mixed isotropic/anisotropic cases.

**Key Functions**:
- `__init__(xray_structure, restraints_manager, use_hd, selection)`: Initialize anisotropic restraints

**Input/Output**: X-ray structure → Anisotropic restraint results
**Dependencies**: `cctbx_adp_restraints_ext`

## Usage Examples

### Basic Usage
```python
# CODE_EXAMPLE_START
# Basic ADP restraints setup and energy calculation
from cctbx.adp_restraints import flags, energies
from cctbx.array_family import flex

# Initialize restraint flags
restraint_flags = flags(
    adp_similarity=True,
    rigid_bond=True,
    isotropic_adp=False,
    default=False
)

# Set up ADP parameters
u_cart = flex.sym_mat3_double([(0.1, 0.2, 0.05, 0.03, 0.02, 0.01)])
sites_cart = flex.vec3_double([(1.0, 2.0, 3.0)])

# Create energy calculator
energy_calc = energies(
    u_cart=u_cart,
    sites_cart=sites_cart,
    compute_gradients=True
)

# Display results
energy_calc.show()
# CODE_EXAMPLE_STOP
```

### Advanced Usage
```python
# CODE_EXAMPLE_START
# Advanced ADP restraints with multiple restraint types
from cctbx.adp_restraints import energies, energies_iso
from cctbx.array_family import flex
import cctbx.xray

# Create X-ray structure
xray_structure = cctbx.xray.structure.from_pdb_file("structure.pdb")

# Set up comprehensive restraint parameters
u_cart = xray_structure.scatterers().extract_u_cart(xray_structure.unit_cell())
u_iso = xray_structure.scatterers().extract_u_iso()
use_u_aniso = xray_structure.use_u_aniso()
sites_cart = xray_structure.sites_cart()

# Create proxies for different restraint types
adp_similarity_proxies = [adp_similarity_proxy(i_seqs=(0,1), weight=1.0)]
rigid_bond_proxies = [rigid_bond_proxy(i_seqs=(0,1), weight=1.0)]
isotropic_adp_proxies = [isotropic_adp_proxy(i_seqs=(0,), weight=1.0)]

# Initialize comprehensive energy calculator
energy_calc = energies(
    u_cart=u_cart,
    u_iso=u_iso,
    use_u_aniso=use_u_aniso,
    sites_cart=sites_cart,
    adp_similarity_proxies=adp_similarity_proxies,
    rigid_bond_proxies=rigid_bond_proxies,
    isotropic_adp_proxies=isotropic_adp_proxies,
    compute_gradients=True,
    normalization=True
)

# Get detailed statistics
adp_stats = energy_calc.adp_similarity_deviation()
rigid_stats = energy_calc.rigid_bond_deviation()
iso_stats = energy_calc.isotropic_adp_deviation()

print(f"ADP Similarity: min={adp_stats[0]:.6f}, max={adp_stats[1]:.6f}, avg={adp_stats[2]:.6f}")
# CODE_EXAMPLE_STOP
```

### Isotropic ADP Restraints
```python
# CODE_EXAMPLE_START
# Specialized isotropic ADP restraints with local sphere constraints
from cctbx.adp_restraints import energies_iso
from cctbx import crystal

# Create pair symmetry table
pair_sym_table = crystal.pair_sym_table()

# Set up parameters
parameters = type('Parameters', (), {
    'sphere_radius': 5.0,
    'distance_power': 1.0,
    'average_power': 1.0,
    'wilson_b_weight': 1.0,
    'wilson_b_weight_auto': True
})()

# Initialize isotropic restraints
iso_energies = energies_iso(
    plain_pair_sym_table=pair_sym_table,
    xray_structure=xray_structure,
    parameters=parameters,
    use_u_local_only=True,
    use_hd=False,
    wilson_b=20.0,
    compute_gradients=True,
    normalization=False,
    collect=False
)

print(f"Number of restraints: {iso_energies.number_of_restraints}")
print(f"Residual sum: {iso_energies.residual_sum:.6f}")
# CODE_EXAMPLE_STOP
```

## API Reference

### Functions
- `flags.__init__(adp_similarity: Optional[bool], rigid_bond: Optional[bool], isotropic_adp: Optional[bool], default: bool) -> None`: Initialize restraint flags
- `flags.show(f: Optional[TextIO]) -> None`: Display current flag values
- `energies.__init__(u_cart: flex.sym_mat3_double, u_iso: Optional[flex.double], use_u_aniso: Optional[flex.bool], sites_cart: Optional[flex.vec3_double], adp_similarity_proxies: Optional[Any], rigid_bond_proxies: Optional[Any], isotropic_adp_proxies: Optional[Any], compute_gradients: bool, gradients_aniso_cart: Optional[flex.sym_mat3_double], gradients_iso: Optional[flex.double], disable_asu_cache: bool, normalization: bool) -> None`: Initialize energy calculation
- `energies.adp_similarity_deviation() -> Optional[Tuple[float, float, float]]`: Calculate ADP similarity deviation statistics
- `energies.rigid_bond_deviation() -> Optional[Tuple[float, float, float]]`: Calculate rigid bond deviation statistics
- `energies.isotropic_adp_deviation() -> Optional[Tuple[float, float, float]]`: Calculate isotropic ADP deviation statistics
- `energies.show(f: Optional[TextIO], prefix: str) -> None`: Display energy statistics
- `energies.finalize_target_and_gradients() -> None`: Finalize target and apply normalization

### Classes
- `flags`: Manages restraint type flags
  - `__init__(adp_similarity, rigid_bond, isotropic_adp, default)`: Constructor with flag initialization
  - `show(f)`: Display current flag values

- `energies`: Main energy calculation class
  - `__init__(u_cart, u_iso, use_u_aniso, sites_cart, proxies...)`: Constructor with comprehensive parameters
  - `adp_similarity_deviation()`: Returns (min, max, average) deviation statistics
  - `rigid_bond_deviation()`: Returns rigid bond deviation statistics
  - `isotropic_adp_deviation()`: Returns isotropic ADP deviation statistics
  - `show(f, prefix)`: Display detailed energy statistics
  - `finalize_target_and_gradients()`: Apply normalization to gradients

- `energies_iso`: Isotropic ADP restraint energies
  - `__init__(plain_pair_sym_table, xray_structure, parameters, ...)`: Constructor for isotropic restraints

- `adp_aniso_restraints`: Anisotropic ADP restraints
  - `__init__(xray_structure, restraints_manager, use_hd, selection)`: Constructor for anisotropic restraints

## Configuration

### Restraint Flags
The `flags` class controls which restraint types are active:
- `adp_similarity`: Enable ADP similarity restraints
- `rigid_bond`: Enable rigid bond restraints  
- `isotropic_adp`: Enable isotropic ADP restraints
- `default`: Default value for unspecified flags

### Energy Calculation Parameters
The `energies` class accepts comprehensive parameters:
- `u_cart`: Anisotropic displacement parameters (required)
- `u_iso`: Isotropic displacement parameters (optional)
- `use_u_aniso`: Boolean array for anisotropic usage (optional)
- `sites_cart`: Atomic positions (required for rigid bond)
- `compute_gradients`: Whether to compute gradients (default: True)
- `normalization`: Whether to apply normalization (default: False)

## Data Flow

### Input Formats
- **ADP Parameters**: `flex.sym_mat3_double` for anisotropic, `flex.double` for isotropic
- **Atomic Positions**: `flex.vec3_double` for Cartesian coordinates
- **Proxies**: Lists of restraint proxy objects defining restraint relationships
- **Flags**: Boolean values controlling restraint types

### Processing Steps
1. **Initialization**: Validate input parameters and set up gradient arrays
2. **Proxy Processing**: Iterate through each restraint type's proxies
3. **Energy Calculation**: Compute residuals and gradients for each restraint
4. **Statistics**: Calculate deviation statistics for monitoring
5. **Normalization**: Apply normalization if requested
6. **Output**: Return target energy and gradients

### Output Formats
- **Target Energy**: Single float value representing total restraint energy
- **Gradients**: `flex.sym_mat3_double` for anisotropic, `flex.double` for isotropic
- **Statistics**: Tuples of (min, max, average) deviation values
- **Counts**: Number of restraints of each type

## Common Use Cases

1. **Basic Structure Refinement**: Simple ADP restraint application
```python
# CODE_EXAMPLE_START
# Basic structure refinement with ADP restraints
from cctbx.adp_restraints import flags, energies
from cctbx.array_family import flex

# Set up basic restraints
flags_obj = flags(adp_similarity=True, rigid_bond=True)
u_cart = flex.sym_mat3_double([(0.1, 0.2, 0.05, 0.03, 0.02, 0.01)])
sites_cart = flex.vec3_double([(1.0, 2.0, 3.0)])

# Calculate energies
energy_calc = energies(u_cart=u_cart, sites_cart=sites_cart)
print(f"Target energy: {energy_calc.target:.6f}")
# CODE_EXAMPLE_STOP
```

2. **Advanced Refinement with Multiple Restraint Types**: Comprehensive restraint application
```python
# CODE_EXAMPLE_START
# Advanced refinement with multiple restraint types
from cctbx.adp_restraints import energies
from cctbx.array_family import flex

# Set up comprehensive restraints
u_cart = flex.sym_mat3_double([(0.1, 0.2, 0.05, 0.03, 0.02, 0.01)])
u_iso = flex.double([0.1])
use_u_aniso = flex.bool([True])
sites_cart = flex.vec3_double([(1.0, 2.0, 3.0)])

# Create proxies for different restraint types
adp_proxies = [adp_similarity_proxy(i_seqs=(0,1), weight=1.0)]
rigid_proxies = [rigid_bond_proxy(i_seqs=(0,1), weight=1.0)]
iso_proxies = [isotropic_adp_proxy(i_seqs=(0,), weight=1.0)]

# Calculate comprehensive energies
energy_calc = energies(
    u_cart=u_cart,
    u_iso=u_iso,
    use_u_aniso=use_u_aniso,
    sites_cart=sites_cart,
    adp_similarity_proxies=adp_proxies,
    rigid_bond_proxies=rigid_proxies,
    isotropic_adp_proxies=iso_proxies,
    normalization=True
)

# Get detailed statistics
print(f"Total restraints: {energy_calc.number_of_restraints}")
print(f"Target energy: {energy_calc.target:.6f}")
# CODE_EXAMPLE_STOP
```

3. **Isotropic ADP Refinement**: Specialized isotropic restraint application
```python
# CODE_EXAMPLE_START
# Isotropic ADP refinement with local sphere constraints
from cctbx.adp_restraints import energies_iso
from cctbx import crystal

# Set up isotropic restraints
pair_sym_table = crystal.pair_sym_table()
parameters = type('Parameters', (), {
    'sphere_radius': 5.0,
    'distance_power': 1.0,
    'average_power': 1.0,
    'wilson_b_weight': 1.0,
    'wilson_b_weight_auto': True
})()

# Calculate isotropic energies
iso_energies = energies_iso(
    plain_pair_sym_table=pair_sym_table,
    xray_structure=xray_structure,
    parameters=parameters,
    use_u_local_only=True,
    use_hd=False,
    wilson_b=20.0
)

print(f"Isotropic restraints: {iso_energies.number_of_restraints}")
print(f"Isotropic energy: {iso_energies.residual_sum:.6f}")
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues

1. **Issue**: `AssertionError: sites_cart.size() == u_cart.size()`
   - **Cause**: Mismatch between number of atomic positions and ADP parameters
   - **Solution**: Ensure `sites_cart` and `u_cart` have the same number of elements
   - **Prevention**: Validate input arrays before creating energy calculator
   ```python
   # CODE_EXAMPLE_START
   # Proper validation before energy calculation
   from cctbx.adp_restraints import energies
   from cctbx.array_family import flex
   
   # Validate input sizes
   assert sites_cart.size() == u_cart.size(), "Size mismatch between sites and ADP parameters"
   if u_iso is not None:
       assert u_iso.size() == u_cart.size(), "Size mismatch with isotropic parameters"
   
   # Safe energy calculation
   energy_calc = energies(u_cart=u_cart, sites_cart=sites_cart, u_iso=u_iso)
   # CODE_EXAMPLE_STOP
   ```

2. **Issue**: `AssertionError: adp_similarity_proxies is not None`
   - **Cause**: ADP similarity proxies provided but missing required parameters
   - **Solution**: Provide both `u_iso` and `use_u_aniso` when using ADP similarity restraints
   - **Prevention**: Check proxy requirements before initialization
   ```python
   # CODE_EXAMPLE_START
   # Proper ADP similarity setup
   from cctbx.adp_restraints import energies
   
   # Ensure required parameters for ADP similarity
   if adp_similarity_proxies is not None:
       assert u_iso is not None, "u_iso required for ADP similarity restraints"
       assert use_u_aniso is not None, "use_u_aniso required for ADP similarity restraints"
   
   energy_calc = energies(
       u_cart=u_cart,
       u_iso=u_iso,
       use_u_aniso=use_u_aniso,
       adp_similarity_proxies=adp_similarity_proxies
   )
   # CODE_EXAMPLE_STOP
   ```

3. **Issue**: `ValueError: gradients_aniso_cart.size() != sites_cart.size()`
   - **Cause**: Pre-allocated gradient array has wrong size
   - **Solution**: Ensure gradient arrays match the number of atoms
   - **Prevention**: Let the system allocate gradients automatically
   ```python
   # CODE_EXAMPLE_START
   # Automatic gradient allocation (recommended)
   from cctbx.adp_restraints import energies
   
   # Let system handle gradient allocation
   energy_calc = energies(
       u_cart=u_cart,
       sites_cart=sites_cart,
       compute_gradients=True
       # Don't specify gradients_aniso_cart - let system allocate
   )
   # CODE_EXAMPLE_STOP
   ```

### Error Messages
- `AssertionError: sites_cart.size() == u_cart.size()`: Size mismatch between atomic positions and ADP parameters
- `AssertionError: u_iso.size() == u_cart.size()`: Size mismatch with isotropic parameters
- `AssertionError: use_u_aniso.size() == u_cart.size()`: Size mismatch with anisotropic usage flags
- `ValueError: gradients_aniso_cart.size() != sites_cart.size()`: Gradient array size mismatch

### Performance Tips
- **Use `compute_gradients=False`** when only energy values are needed (faster)
- **Pre-allocate gradient arrays** for repeated calculations to avoid reallocation
- **Use `normalization=True`** for consistent energy scaling across different restraint counts
- **Batch restraint calculations** rather than individual proxy processing
- **Monitor memory usage** with large structures - gradient arrays can be substantial

## Dependencies
- `cctbx.array_family.flex`: Array operations and data structures
- `cctbx.adptbx`: ADP parameter transformations
- `cctbx.crystal`: Crystal symmetry operations
- `scitbx.restraints`: Base restraint framework
- `libtbx.adopt_init_args`: Automatic argument handling
- `cctbx_adp_restraints_ext`: C++ computational kernels

## Testing
```python
# CODE_EXAMPLE_START
# Example test cases for ADP restraints
import pytest
from cctbx.adp_restraints import flags, energies
from cctbx.array_family import flex

def test_basic_flags():
    """Test basic flag initialization and display"""
    f = flags(adp_similarity=True, rigid_bond=False, isotropic_adp=True)
    assert f.adp_similarity is True
    assert f.rigid_bond is False
    assert f.isotropic_adp is True

def test_energy_calculation():
    """Test basic energy calculation"""
    u_cart = flex.sym_mat3_double([(0.1, 0.2, 0.05, 0.03, 0.02, 0.01)])
    sites_cart = flex.vec3_double([(1.0, 2.0, 3.0)])
    
    energy_calc = energies(u_cart=u_cart, sites_cart=sites_cart)
    assert energy_calc.target is not None
    assert energy_calc.number_of_restraints >= 0

def test_deviation_statistics():
    """Test deviation statistics calculation"""
    u_cart = flex.sym_mat3_double([(0.1, 0.2, 0.05, 0.03, 0.02, 0.01)])
    sites_cart = flex.vec3_double([(1.0, 2.0, 3.0)])
    
    energy_calc = energies(u_cart=u_cart, sites_cart=sites_cart)
    rigid_stats = energy_calc.rigid_bond_deviation()
    # Should return None when no rigid bond proxies are provided
    assert rigid_stats is None
# CODE_EXAMPLE_STOP
```

## Integration Notes

### Upstream Dependencies
- **X-ray Structure**: Requires `cctbx.xray.structure` objects for atomic information
- **Crystal Symmetry**: Uses `cctbx.crystal` for symmetry operations
- **Array Framework**: Depends on `cctbx.array_family.flex` for data structures

### Downstream Components
- **Refinement Engines**: Provides energy and gradient information for optimization
- **Structure Analysis**: Outputs statistics for restraint quality assessment
- **Visualization**: Supplies data for restraint visualization tools

### Shared Resources
- **Unit Cell**: Shared across all restraint types for coordinate transformations
- **Atomic Selection**: Common selection mechanisms for restraint application
- **Gradient Arrays**: Shared memory for efficient gradient accumulation

## Changelog/Version Notes

### Recent Enhancements
- **Type Hints**: Added comprehensive type annotations for all functions and methods
- **Documentation**: Enhanced docstrings with detailed parameter descriptions
- **Error Handling**: Improved validation and error messages
- **Performance**: Optimized gradient calculations for large structures

### Compatibility Notes
- **Backward Compatible**: All existing APIs remain unchanged
- **Structural Integrity**: Function signatures and parameter counts preserved
- **Type Safety**: Optional type hints enhance IDE support without breaking existing code

The ADP restraints module provides essential functionality for maintaining physically reasonable atomic displacement parameters during crystallographic refinement, with comprehensive support for multiple restraint types and detailed statistical analysis. 