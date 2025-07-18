# CCTBX ADP Toolbox (adptbx)

## Overview

The `cctbx.adptbx` module provides comprehensive functionality for handling Anisotropic Displacement Parameters (ADPs) in crystallographic refinement. This toolbox is essential for managing thermal motion parameters, coordinate transformations, and ADP-related calculations in crystallographic structure determination and refinement.

The module supports multiple ADP coordinate systems and provides tools for:
- **ADP Transformations**: Converting between different coordinate representations (U_star, U_cart, U_cif, beta)
- **Debye-Waller Factor Calculations**: Computing temperature factors for structure factors
- **Eigenvalue Analysis**: Analyzing ADP tensors for physical validity
- **Hirshfeld Analysis**: Mean square displacement calculations for rigid bond restraints
- **ADP Filtering**: Constraining ADPs to physically reasonable values

## Architecture

The module follows a layered architecture with four main components:

1. **Core C++ Extensions** (`adptbx_ext.cpp`, `hirshfeld.cpp`, `anharmonic_ext.cpp`): High-performance computational kernels
2. **Python Interface Modules** (`cctbx/adptbx.py`, `cctbx/anharmonic.py`): Python wrappers that import compiled extensions
3. **Test Suite** (`tst_adptbx.py`, `tst_hirshfeld.py`): Comprehensive validation and usage examples
4. **Header Files** (`hirshfeld.h`): Mathematical implementations for Hirshfeld analysis

### Compilation and Import Chain
```
C++ Source Files (adptbx_ext.cpp, hirshfeld.cpp, anharmonic_ext.cpp)
    ↓ (compiled via SConscript)
Shared Libraries (cctbx_adptbx_ext, cctbx_anharmonic_ext)
    ↓ (imported via boost_adaptbx.boost.python)
Python Interface Modules (cctbx/adptbx.py, cctbx/anharmonic.py)
    ↓ (imported by users)
Python Functions and Classes accessible as cctbx.adptbx.*
```

### Data Flow
```
Input: ADP parameters in various coordinate systems
    ↓
Coordinate transformations (U_star ↔ U_cart ↔ U_cif ↔ beta)
    ↓
Physical validation (eigenvalue analysis, positive definiteness)
    ↓
Output: Transformed ADPs + Debye-Waller factors + validation results
```

## Key Components

### Python Interface Modules
**Purpose**: Provide Python access to compiled C++ ADP functions and classes.

**Main Modules**:
- **`cctbx/adptbx.py`**: Primary interface importing `cctbx_adptbx_ext`
  - Imports core ADP transformation and calculation functions
  - Provides additional Python utility functions
  - Exposes C++ functions as Python functions
- **`cctbx/anharmonic.py`**: Anharmonic ADP functions importing `cctbx_anharmonic_ext`
  - Imports anharmonic ADP calculation functions
  - Provides Gram-Charlier expansion calculations

**Import Pattern**:
```python
import boost_adaptbx.boost.python as bp
ext = bp.import_ext("cctbx_adptbx_ext")
from cctbx_adptbx_ext import *
```

### ADP Transformation Functions
**Purpose**: Convert anisotropic displacement parameters between different coordinate systems used in crystallography.

**Key Functions** (from C++ compiled extensions):
- `u_as_b(u_iso)`: Convert isotropic U to B factor
- `b_as_u(b_iso)`: Convert B factor to isotropic U
- `u_cif_as_u_star(unit_cell, u_cif)`: Convert U_cif to U_star coordinates
- `u_star_as_u_cif(unit_cell, u_star)`: Convert U_star to U_cif coordinates
- `u_cart_as_u_star(unit_cell, u_cart)`: Convert U_cart to U_star coordinates
- `u_star_as_u_cart(unit_cell, u_star)`: Convert U_star to U_cart coordinates
- `u_star_as_beta(u_star)`: Convert U_star to beta parameters
- `beta_as_u_star(beta)`: Convert beta to U_star parameters

**Input/Output**: Symmetric 3x3 matrices representing ADP tensors
**Dependencies**: `cctbx.uctbx` for unit cell operations

### Debye-Waller Factor Calculations
**Purpose**: Compute temperature factors for structure factor calculations.

**Key Functions**:
- `debye_waller_factor_b_iso(stol_sq, b_iso)`: Isotropic B-factor Debye-Waller factor
- `debye_waller_factor_u_iso(stol_sq, u_iso)`: Isotropic U-factor Debye-Waller factor
- `debye_waller_factor_u_star(h, u_star)`: Anisotropic U_star Debye-Waller factor
- `debye_waller_factor_u_cart(unit_cell, h, u_cart)`: Anisotropic U_cart Debye-Waller factor

**Input/Output**: Miller indices and ADP parameters → Debye-Waller factors
**Dependencies**: `scitbx.constants` for mathematical constants

### Eigenvalue Analysis Functions
**Purpose**: Analyze ADP tensors for physical validity and constraints.

**Key Functions**:
- `eigenvalues(u)`: Compute eigenvalues of ADP tensor
- `eigensystem(u)`: Compute eigenvalues and eigenvectors
- `is_positive_definite(eigenvalues, tolerance)`: Check physical validity
- `eigenvalue_filtering(u_cart, u_min, u_max)`: Constrain eigenvalues to bounds

**Input/Output**: ADP tensors → Eigenvalues and validation results
**Dependencies**: `scitbx.linalg.eigensystem` for eigenvalue calculations

### Hirshfeld Analysis Functions
**Purpose**: Compute mean square displacements for rigid bond restraints and validation.

**Key Functions** (from C++ compiled extensions):
- `mean_square_displacement(unit_cell, z)`: Compute mean square displacement along direction z
- `relative_hirshfeld_difference(unit_cell, x1, u1, x2, u2, op)`: Compute relative differences

**Input/Output**: Unit cell, atomic positions, and ADPs → Displacement calculations
**Dependencies**: `scitbx.matrix`, `cctbx.sgtbx` for symmetry operations

### Additional Python Utility Functions
**Purpose**: Provide Python-specific utilities and convenience functions.

**Key Functions** (from `cctbx/adptbx.py`):
- `random_rotate_ellipsoid(u_cart, r_min, r_max)`: Randomly rotate ADP ellipsoid
- `random_u_cart(u_scale, u_min)`: Generate random U_cart parameters
- `debye_waller_factor_u_star_gradients(h, u_star)`: Calculate Debye-Waller gradients
- `debye_waller_factor_u_star_curvatures(h, u_star)`: Calculate Debye-Waller curvatures
- `random_traceless_symmetry_constrained_b_cart(crystal_symmetry, u_scale, u_min)`: Generate symmetry-constrained B_cart
- `intersection(u_1, u_2, site_1, site_2, unit_cell)`: Calculate scatterer intersection

## Usage Examples

### Basic Usage
```python
# CODE_EXAMPLE_START
# Basic ADP transformations and Debye-Waller factor calculations
from cctbx import adptbx, uctbx
from cctbx.array_family import flex

# Set up unit cell and ADP parameters
unit_cell = uctbx.unit_cell((5, 4, 7, 80, 110, 100))
u_cart = (0.1, 0.2, 0.05, 0.03, 0.02, 0.01)  # U_cart parameters

# Transform between coordinate systems
u_star = adptbx.u_cart_as_u_star(unit_cell, u_cart)
u_cif = adptbx.u_cart_as_u_cif(unit_cell, u_cart)
beta = adptbx.u_star_as_beta(u_star)

# Verify transformations are reversible
u_cart_back = adptbx.u_star_as_u_cart(unit_cell, u_star)
assert flex.double(u_cart) == flex.double(u_cart_back)

# Calculate Debye-Waller factors
h = (1, 2, 3)  # Miller index
dw_star = adptbx.debye_waller_factor_u_star(h, u_star)
dw_cart = adptbx.debye_waller_factor_u_cart(unit_cell, h, u_cart)
print(f"Debye-Waller factors: U_star={dw_star:.6f}, U_cart={dw_cart:.6f}")
# CODE_EXAMPLE_STOP
```

### Advanced Usage
```python
# CODE_EXAMPLE_START
# Advanced ADP analysis with eigenvalue filtering and validation
from cctbx import adptbx, uctbx
from cctbx.array_family import flex
import scitbx.linalg.eigensystem

# Set up unit cell and potentially problematic ADP
unit_cell = uctbx.unit_cell((12.3, 16.0, 20.9, 83.0, 109.0, 129.0))
u_cart = (0.1, 0.2, -0.05, 0.03, 0.02, 0.01)  # May have negative eigenvalues

# Analyze eigenvalues
eigenvals = adptbx.eigenvalues(u_cart)
print(f"Eigenvalues: {eigenvals}")

# Check physical validity
is_valid = adptbx.is_positive_definite(eigenvals, tolerance=0.0)
print(f"Physically valid: {is_valid}")

# Apply eigenvalue filtering to ensure physical constraints
u_filtered = adptbx.eigenvalue_filtering(
    u_cart=u_cart, 
    u_min=0.01,  # Minimum eigenvalue
    u_max=0.5    # Maximum eigenvalue
)

# Verify filtered result is physically valid
eigenvals_filtered = adptbx.eigenvalues(u_filtered)
is_valid_filtered = adptbx.is_positive_definite(eigenvals_filtered, tolerance=0.0)
print(f"Filtered eigenvalues: {eigenvals_filtered}")
print(f"Filtered physically valid: {is_valid_filtered}")

# Factor U_cart into isotropic and anisotropic components
fc = adptbx.factor_u_cart_u_iso(u_cart=u_filtered)
print(f"U_iso: {fc.u_iso:.6f}")
print(f"U_cart minus U_iso: {fc.u_cart_minus_u_iso}")
# CODE_EXAMPLE_STOP
```

### Hirshfeld Analysis for Rigid Bond Restraints
```python
# CODE_EXAMPLE_START
# Hirshfeld analysis for rigid bond restraint validation
from cctbx import adptbx, uctbx, sgtbx
from scitbx import matrix
from cctbx.array_family import flex

# Set up unit cell and atomic positions
unit_cell = uctbx.unit_cell((10, 12, 15, 90, 90, 90))
x1 = matrix.col((1.0, 2.0, 3.0))  # First atom position
x2 = matrix.col((1.5, 2.0, 3.0))  # Second atom position

# Set up ADP tensors for the two atoms
u1 = matrix.sym((0.1, 0.2, 0.05, 0.03, 0.02, 0.01))
u2 = matrix.sym((0.12, 0.18, 0.06, 0.025, 0.015, 0.008))

# Compute mean square displacement along the bond direction
z = x1 - x2  # Bond direction vector
hirshfeld = adptbx.mean_square_displacement(unit_cell, z)

# Calculate mean square displacements for both atoms
h1 = hirshfeld(u1).value
h2 = hirshfeld(u2).value

print(f"Mean square displacement atom 1: {h1:.6f}")
print(f"Mean square displacement atom 2: {h2:.6f}")
print(f"Rigid bond difference: {abs(h1 - h2):.6f}")

# Compute relative Hirshfeld difference with symmetry operation
op = sgtbx.rt_mx()  # Identity operation
r = adptbx.relative_hirshfeld_difference(unit_cell, x1, u1, x2, u2, op)
print(f"Relative Hirshfeld difference: {r.value:.6f}")
# CODE_EXAMPLE_STOP
```

## API Reference

### Core Transformation Functions
- `u_as_b(u_iso: float) -> float`: Convert isotropic U to B factor
- `b_as_u(b_iso: float) -> float`: Convert B factor to isotropic U
- `u_cif_as_u_star(unit_cell, u_cif: sym_mat3) -> sym_mat3`: U_cif to U_star
- `u_star_as_u_cif(unit_cell, u_star: sym_mat3) -> sym_mat3`: U_star to U_cif
- `u_cart_as_u_star(unit_cell, u_cart: sym_mat3) -> sym_mat3`: U_cart to U_star
- `u_star_as_u_cart(unit_cell, u_star: sym_mat3) -> sym_mat3`: U_star to U_cart
- `u_star_as_beta(u_star: sym_mat3) -> sym_mat3`: U_star to beta
- `beta_as_u_star(beta: sym_mat3) -> sym_mat3`: Beta to U_star

### Debye-Waller Factor Functions
- `debye_waller_factor_b_iso(stol_sq: float, b_iso: float) -> float`: Isotropic B-factor
- `debye_waller_factor_u_iso(stol_sq: float, u_iso: float) -> float`: Isotropic U-factor
- `debye_waller_factor_u_star(h: miller.index, u_star: sym_mat3) -> float`: Anisotropic U_star
- `debye_waller_factor_u_cart(unit_cell, h: miller.index, u_cart: sym_mat3) -> float`: Anisotropic U_cart

### Eigenvalue Analysis Functions
- `eigenvalues(u: sym_mat3) -> vec3`: Compute eigenvalues
- `eigensystem(u: sym_mat3) -> eigensystem`: Compute eigenvalues and eigenvectors
- `is_positive_definite(eigenvalues: vec3, tolerance: float = 0.0) -> bool`: Check validity
- `eigenvalue_filtering(u_cart: sym_mat3, u_min: float = 0, u_max: float = 0) -> sym_mat3`: Constrain eigenvalues

### Factorization Functions
- `factor_u_cart_u_iso(u_cart: sym_mat3) -> factor_result`: Factor U_cart into isotropic and anisotropic components
- `factor_u_star_u_iso(unit_cell, u_star: sym_mat3) -> factor_result`: Factor U_star into isotropic and anisotropic components

### Hirshfeld Analysis Functions
- `mean_square_displacement(unit_cell, z: vec3) -> mean_square_displacement`: Compute mean square displacement
- `relative_hirshfeld_difference(unit_cell, x1: vec3, u1: sym_mat3, x2: vec3, u2: sym_mat3, op: rt_mx) -> relative_hirshfeld_difference`: Compute relative differences

## Configuration

### Unit Cell Requirements
All coordinate transformations require a valid unit cell object from `cctbx.uctbx`:
- **U_cart ↔ U_star**: Requires unit cell for fractionalization/orthogonalization matrices
- **U_cif ↔ U_star**: Requires unit cell for reciprocal parameters
- **Debye-Waller factors**: Require unit cell for d* calculations

### ADP Parameter Formats
ADP parameters are represented as symmetric 3x3 matrices with 6 components:
- **U_cart**: Cartesian coordinates (Å²)
- **U_star**: Reciprocal space coordinates (Å²)
- **U_cif**: CIF format coordinates (Å²)
- **Beta**: Beta parameters (Å²)

### Tolerance Parameters
- **Positive definiteness**: Default tolerance of 0.0 for strict physical validity
- **Eigenvalue filtering**: User-defined minimum and maximum bounds
- **Coordinate transformations**: Numerical precision tolerance for reversibility checks

## Data Flow

### Input Formats
- **ADP Parameters**: `sym_mat3` objects or 6-element tuples/lists
- **Unit Cell**: `uctbx.unit_cell` objects with lattice parameters
- **Miller Indices**: `miller.index` objects or 3-element tuples
- **Atomic Positions**: `vec3` objects or 3-element tuples/lists

### Processing Steps
1. **Input Validation**: Check unit cell validity and ADP parameter formats
2. **Coordinate Transformation**: Apply appropriate transformation matrices
3. **Physical Validation**: Check positive definiteness and eigenvalue bounds
4. **Debye-Waller Calculation**: Compute temperature factors for structure factors
5. **Output**: Return transformed parameters and validation results

### Output Formats
- **Transformed ADPs**: `sym_mat3` objects in target coordinate system
- **Debye-Waller Factors**: Float values for structure factor calculations
- **Eigenvalues**: `vec3` objects with sorted eigenvalues
- **Validation Results**: Boolean flags and constraint satisfaction indicators

## Common Use Cases

1. **Structure Refinement**: Coordinate transformations during refinement
```python
# CODE_EXAMPLE_START
# Structure refinement with ADP coordinate transformations
from cctbx import adptbx, uctbx
from cctbx.array_family import flex

# During refinement, convert between coordinate systems
unit_cell = uctbx.unit_cell((10, 12, 15, 90, 90, 90))
u_cart_refined = (0.15, 0.25, 0.08, 0.04, 0.03, 0.02)

# Convert to U_star for structure factor calculations
u_star = adptbx.u_cart_as_u_star(unit_cell, u_cart_refined)

# Convert to U_cif for output files
u_cif = adptbx.u_cart_as_u_cif(unit_cell, u_cart_refined)

# Validate physical reasonableness
eigenvals = adptbx.eigenvalues(u_cart_refined)
is_valid = adptbx.is_positive_definite(eigenvals)
print(f"Refined ADP physically valid: {is_valid}")
# CODE_EXAMPLE_STOP
```

2. **Structure Factor Calculations**: Debye-Waller factor computation
```python
# CODE_EXAMPLE_START
# Structure factor calculations with Debye-Waller factors
from cctbx import adptbx, uctbx, miller

# Set up reflection data
unit_cell = uctbx.unit_cell((8, 9, 10, 90, 90, 90))
hkl = miller.index((2, 3, 1))
u_star = (0.1, 0.15, 0.08, 0.02, 0.01, 0.005)

# Calculate Debye-Waller factor for this reflection
dw_factor = adptbx.debye_waller_factor_u_star(hkl, u_star)
print(f"Debye-Waller factor for {hkl}: {dw_factor:.6f}")

# For multiple reflections
hkl_list = [miller.index((1,0,0)), miller.index((0,1,0)), miller.index((0,0,1))]
dw_factors = [adptbx.debye_waller_factor_u_star(h, u_star) for h in hkl_list]
print(f"Debye-Waller factors: {[f'{dw:.6f}' for dw in dw_factors]}")
# CODE_EXAMPLE_STOP
```

3. **Rigid Bond Restraint Validation**: Hirshfeld analysis
```python
# CODE_EXAMPLE_START
# Rigid bond restraint validation using Hirshfeld analysis
from cctbx import adptbx, uctbx, sgtbx
from scitbx import matrix

# Set up bonded atom pair
unit_cell = uctbx.unit_cell((10, 10, 10, 90, 90, 90))
x1 = matrix.col((1.0, 1.0, 1.0))  # Carbon atom
x2 = matrix.col((1.54, 1.0, 1.0))  # Bonded carbon atom (C-C bond)

# ADP tensors for the two atoms
u1 = matrix.sym((0.08, 0.12, 0.06, 0.02, 0.01, 0.005))  # First atom
u2 = matrix.sym((0.09, 0.11, 0.07, 0.025, 0.015, 0.008))  # Second atom

# Compute rigid bond restraint
z = x2 - x1  # Bond direction
hirshfeld = adptbx.mean_square_displacement(unit_cell, z)

h1 = hirshfeld(u1).value
h2 = hirshfeld(u2).value
delta_z = abs(h1 - h2)

print(f"Rigid bond restraint: {delta_z:.6f} Å²")
print(f"Acceptable range: < 0.01 Å²")

# Check if restraint is satisfied
restraint_satisfied = delta_z < 0.01
print(f"Rigid bond satisfied: {restraint_satisfied}")
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues

1. **Issue**: "anisotropic displacement tensor is not positive definite"
   - **Cause**: ADP parameters result in negative eigenvalues, indicating unphysical thermal motion
   - **Solution**: Apply eigenvalue filtering to constrain to positive values
   - **Prevention**: Validate ADPs during refinement with `is_positive_definite()`
   ```python
   # CODE_EXAMPLE_START
   # Fix non-positive definite ADP
   from cctbx import adptbx
   
   # Problematic ADP with negative eigenvalues
   u_cart = (0.1, 0.2, -0.05, 0.03, 0.02, 0.01)
   
   # Check if physically valid
   eigenvals = adptbx.eigenvalues(u_cart)
   is_valid = adptbx.is_positive_definite(eigenvals)
   print(f"Original valid: {is_valid}")
   
   # Apply filtering to ensure physical constraints
   u_filtered = adptbx.eigenvalue_filtering(u_cart=u_cart, u_min=0.01)
   eigenvals_filtered = adptbx.eigenvalues(u_filtered)
   is_valid_filtered = adptbx.is_positive_definite(eigenvals_filtered)
   print(f"Filtered valid: {is_valid_filtered}")
   # CODE_EXAMPLE_STOP
   ```

2. **Issue**: Coordinate transformation not reversible
   - **Cause**: Numerical precision issues or invalid unit cell parameters
   - **Solution**: Check unit cell validity and use appropriate tolerance
   - **Prevention**: Validate unit cell parameters before transformations
   ```python
   # CODE_EXAMPLE_START
   # Ensure reversible coordinate transformations
   from cctbx import adptbx, uctbx
   from cctbx.array_family import flex
   
   # Valid unit cell
   unit_cell = uctbx.unit_cell((10, 12, 15, 90, 90, 90))
   u_cart = (0.1, 0.2, 0.05, 0.03, 0.02, 0.01)
   
   # Forward transformation
   u_star = adptbx.u_cart_as_u_star(unit_cell, u_cart)
   
   # Reverse transformation
   u_cart_back = adptbx.u_star_as_u_cart(unit_cell, u_star)
   
   # Check reversibility with tolerance
   tolerance = 1e-10
   is_reversible = all(abs(a - b) < tolerance 
                       for a, b in zip(u_cart, u_cart_back))
   print(f"Transformation reversible: {is_reversible}")
   # CODE_EXAMPLE_STOP
   ```

3. **Issue**: Debye-Waller factor calculation errors
   - **Cause**: Invalid Miller indices or ADP parameters
   - **Solution**: Validate input parameters and check for zero values
   - **Prevention**: Use appropriate parameter ranges and validation
   ```python
   # CODE_EXAMPLE_START
   # Safe Debye-Waller factor calculation
   from cctbx import adptbx, uctbx, miller
   
   # Valid parameters
   unit_cell = uctbx.unit_cell((8, 9, 10, 90, 90, 90))
   hkl = miller.index((1, 1, 1))  # Valid Miller index
   u_star = (0.1, 0.15, 0.08, 0.02, 0.01, 0.005)  # Valid ADP
   
   try:
       dw_factor = adptbx.debye_waller_factor_u_star(hkl, u_star)
       print(f"Debye-Waller factor: {dw_factor:.6f}")
   except Exception as e:
       print(f"Error calculating Debye-Waller factor: {e}")
       # Check parameters and try with different values
   # CODE_EXAMPLE_STOP
   ```

### Error Messages
- `"anisotropic displacement tensor is not positive definite"`: ADP has negative eigenvalues
- `"unit cell parameters are invalid"`: Unit cell parameters are unphysical
- `"Miller index out of range"`: Invalid reflection indices
- `"ADP parameters have wrong format"`: Incorrect parameter array length or type

### Performance Tips
- **Batch Operations**: Use array operations for multiple ADPs when possible
- **Caching**: Cache unit cell matrices for repeated transformations
- **Memory Management**: Use `flex` arrays for large datasets
- **Numerical Precision**: Use appropriate tolerances for floating-point comparisons

## Dependencies

### Core Dependencies
- `cctbx.uctbx`: Unit cell operations and coordinate transformations
- `scitbx.matrix`: Matrix operations and eigenvalue calculations
- `scitbx.constants`: Mathematical constants (π, etc.)
- `cctbx.array_family.flex`: Array operations for batch processing
- `cctbx.sgtbx`: Symmetry operations for Hirshfeld analysis

### Compilation Dependencies
- **Boost.Python**: C++ to Python binding framework
- **SCons**: Build system for compiling C++ extensions
- **C++ Compiler**: Required for building shared libraries

### Extension Dependencies
- **`cctbx_adptbx_ext`**: Main ADP functions and classes
- **`cctbx_anharmonic_ext`**: Anharmonic ADP calculations
- **`boost_adaptbx.boost.python`**: Python import mechanism for compiled extensions

## Testing
The module includes comprehensive test suites that validate all functionality:

```python
# CODE_EXAMPLE_START
# Run the test suites
import sys
sys.path.append('cctbx/adptbx/boost_python')

# Test basic ADP functionality
from tst_adptbx import run as test_adptbx
test_adptbx()

# Test Hirshfeld analysis
from tst_hirshfeld import run as test_hirshfeld
test_hirshfeld()
# CODE_EXAMPLE_STOP
```

### Test Coverage
- **Coordinate Transformations**: Verify all transformation pairs are reversible
- **Debye-Waller Factors**: Validate against analytical solutions
- **Eigenvalue Analysis**: Test positive definiteness and filtering
- **Hirshfeld Analysis**: Compare with rigid bond restraint calculations
- **Edge Cases**: Test with extreme parameter values and boundary conditions

## Integration Notes

### Upstream Dependencies
- **Unit Cell**: Requires valid unit cell parameters from crystallographic data
- **Atomic Positions**: Requires fractional or Cartesian coordinates
- **Symmetry Operations**: Requires space group symmetry for Hirshfeld analysis

### Downstream Components
- **Structure Factor Calculations**: Provides Debye-Waller factors for F_calc
- **Refinement Programs**: Supplies coordinate transformations and validation
- **Restraint Systems**: Provides Hirshfeld analysis for rigid bond restraints
- **Output Formats**: Converts between coordinate systems for different file formats

### Shared Resources
- **Unit Cell Objects**: Shared across transformation functions
- **Symmetry Operations**: Used in Hirshfeld analysis
- **Mathematical Constants**: Used in Debye-Waller calculations

### Module Import Structure
```
cctbx.adptbx (Python module)
    ↓ imports
cctbx_adptbx_ext (compiled C++ extension)
    ↓ contains
C++ functions: u_as_b, b_as_u, u_cart_as_u_star, etc.
C++ classes: mean_square_displacement, relative_hirshfeld_difference

cctbx.anharmonic (Python module)
    ↓ imports
cctbx_anharmonic_ext (compiled C++ extension)
    ↓ contains
C++ classes: gram_charlier (Gram-Charlier expansion)
```

## Changelog/Version Notes

### Recent Enhancements
- **Type Hints**: Added comprehensive type annotations to test files
- **Documentation**: Enhanced docstrings with Google/NumPy style
- **Validation**: Improved physical constraint checking
- **Performance**: Optimized coordinate transformation algorithms

### Compatibility
- **Python 2/3**: Maintains compatibility with both Python versions
- **C++ Extensions**: Uses Boost.Python for high-performance operations
- **Array Formats**: Supports both `flex` arrays and native Python types
- **Unit Cell Formats**: Compatible with all CCTBX unit cell representations

### Future Development
- **GPU Acceleration**: Planned GPU support for large-scale ADP operations
- **Advanced Filtering**: Enhanced eigenvalue filtering algorithms
- **Machine Learning**: Integration with ML-based ADP prediction
- **Real-time Validation**: Continuous physical constraint checking during refinement
- **Enhanced C++ Extensions**: Additional high-performance computational kernels
- **Improved Python Interface**: More comprehensive Python utility functions 