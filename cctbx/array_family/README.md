# CCTBX Array Family

## Overview

The `cctbx/array_family` module provides specialized array types for crystallographic data processing within the CCTBX (Computational Crystallography Toolbox) framework. This module extends the base `scitbx.array_family.flex` functionality with crystallography-specific array types and operations.

## Architecture

The module consists of:
- **Python Interface**: `flex.py` - Main import/export wrapper with docstring injection
- **Type Hints**: `flex.pyi` - Stub file providing type annotations for IDE support
- **C++ Extensions**: `boost_python/` - Core functionality implemented in C++ and exposed via Boost.Python
- **Test Suite**: `boost_python/tst_flex.py` - Comprehensive test coverage

The architecture follows a hybrid approach where:
1. Core functionality is implemented in C++ for performance
2. Python bindings are created via Boost.Python
3. Type hints and docstrings are added post-import for developer experience

## Key Components

### flex.py
**Purpose**: Main entry point that imports C++ extensions and adds documentation
**Key Functions**:
- `_add_docstrings()`: Runtime docstring injection for Boost.Python exposed functions
- Module-level imports and exports

**Input/Output**: Imports C++ extensions and exports them with enhanced documentation
**Dependencies**: `boost_adaptbx.boost.python`, `scitbx.array_family.flex`

### flex.pyi (Type Stub File)
**Purpose**: Provides type hints for IDE support and static analysis
**Key Features**:
- Type aliases for common flex types (`FlexDouble`, `FlexInt`, etc.)
- Complete type annotations for all exposed functions
- Support for complex types (`Optional`, `Union`, `Tuple`)

**Dependencies**: `typing` module, `scitbx.array_family.flex`

### C++ Extensions (boost_python/)

#### flex_hendrickson_lattman.cpp
**Purpose**: Implements Hendrickson-Lattman coefficient arrays for phase refinement
**Key Functions**:
- `from_a_b()`: Constructor from A, B parameters
- `from_a_b_c_d()`: Constructor from A, B, C, D parameters
- `slice()`: Extract parameter slices
- `conj()`: Complex conjugate operations
- `as_abcd()`: Extract A, B, C, D as separate arrays

#### flex_miller_index.cpp
**Purpose**: Implements Miller index arrays for crystallographic calculations
**Key Functions**:
- `join()`: Combine h, k, l arrays into Miller indices
- `as_vec3_double()`: Convert to 3D vector format
- `fourier_transform_real_part_at_x()`: Calculate Fourier transform values
- `first_index()`: Find first occurrence of a Miller index

#### flex_xray_scatterer.cpp
**Purpose**: Implements X-ray scatterer arrays for structural refinement
**Key Functions**:
- `extract_labels()`: Get scatterer labels
- `extract_sites()`: Get atomic positions
- `set_sites()`: Update atomic positions
- `extract_occupancies()`: Get occupancy values
- `set_occupancies()`: Update occupancy values
- `extract_u_iso()`: Get isotropic B-factors
- `set_u_iso()`: Update isotropic B-factors
- `extract_u_star()`: Get anisotropic B-factors
- `set_u_star()`: Update anisotropic B-factors
- `count_anisotropic()`: Count anisotropic scatterers
- `convert_to_isotropic()`: Convert anisotropic to isotropic
- `convert_to_anisotropic()`: Convert isotropic to anisotropic

## Usage Examples

### Basic Usage
```python
# CODE_EXAMPLE_START
# Import the array family module
from cctbx.array_family import flex

# Create Hendrickson-Lattman coefficients
a_params = flex.double([1.0, 2.0, 3.0])
b_params = flex.double([4.0, 5.0, 6.0])
hl_array = flex.hendrickson_lattman(a=a_params, b=b_params)

# Extract parameter slices
a_slice = hl_array.slice(0)  # Get A parameters
b_slice = hl_array.slice(1)  # Get B parameters

# Get complex conjugate
hl_conj = hl_array.conj()

# Extract all parameters
a, b, c, d = hl_array.as_abcd()
# CODE_EXAMPLE_STOP
```

### Miller Index Operations
```python
# CODE_EXAMPLE_START
# Create Miller indices
h_indices = flex.int([1, 2, 3])
k_indices = flex.int([0, 1, 2])
l_indices = flex.int([1, 1, 1])

miller_indices = flex.miller_index(h=h_indices, k=k_indices, l=l_indices)

# Convert to 3D vectors
vec3_array = miller_indices.as_vec3_double()

# Calculate Fourier transform
fourier_coeffs = flex.complex_double([1.0+0.5j, 0.5+1.0j, 0.3+0.7j])
position = (0.1, 0.2, 0.3)
real_part = miller_indices.fourier_transform_real_part_at_x(
    fourier_coeffs=fourier_coeffs, x=position)

# Find specific Miller index
target_index = (1, 0, 1)
first_occurrence = miller_indices.first_index(miller_index=target_index)
# CODE_EXAMPLE_STOP
```

### X-ray Scatterer Management
```python
# CODE_EXAMPLE_START
from cctbx import xray, uctbx

# Create scatterers
scatterer1 = xray.scatterer("Si1", (0.1, 0.2, 0.3))
scatterer2 = xray.scatterer("O1", (0.2, 0.3, 0.4), occupancy=0.9)
scatterer3 = xray.scatterer("K1", (0.3, 0.4, 0.5), fp=5, fdp=7)

# Create scatterer array
scatterers = flex.xray_scatterer((scatterer1, scatterer2, scatterer3))

# Extract information
labels = scatterers.extract_labels()
sites = scatterers.extract_sites()
occupancies = scatterers.extract_occupancies()

# Update scatterer properties
new_sites = flex.vec3_double([(0.5, 0.6, 0.7), (0.8, 0.9, 1.0), (1.1, 1.2, 1.3)])
scatterers.set_sites(sites=new_sites)

new_occupancies = flex.double([0.8, 0.9, 0.7])
scatterers.set_occupancies(occupancies=new_occupancies)

# B-factor operations
u_iso_values = scatterers.extract_u_iso()
scatterers.set_u_iso(u_iso=flex.double([0.1, 0.2, 0.3]), 
                     selection=flex.bool(scatterers.size(), True))

# Convert between isotropic and anisotropic
scatterers.convert_to_anisotropic(unit_cell=uctbx.unit_cell((10, 10, 10)))
anisotropic_count = scatterers.count_anisotropic()
# CODE_EXAMPLE_STOP
```

### Advanced Usage
```python
# CODE_EXAMPLE_START
# Complex Hendrickson-Lattman operations
centric_flags = flex.bool([False, True, False])
phase_integrals = flex.complex_double([
    complex(0.5, -0.7), 
    complex(-0.3, 0.4),
    complex(0.1, 0.2)
])

hl_from_phases = flex.hendrickson_lattman(
    centric_flags=centric_flags,
    phase_integrals=phase_integrals,
    max_figure_of_merit=0.999999
)

# Mathematical operations
hl_sum = hl_array + hl_from_phases
hl_scaled = hl_array * 2.0

# Comparison operations
is_equal = hl_array == (1.0, 4.0, 0.0, 0.0)
is_not_equal = hl_array != (0.0, 0.0, 0.0, 0.0)

# X-ray scatterer with anisotropic B-factors
unit_cell = uctbx.unit_cell((10, 11, 12))
u_star_values = flex.sym_mat3_double([
    (1, 2, 3, -0.6, 0.2, -0.3),
    (3, 1, 2, -0.2, 0.5, -0.1),
    (2, 3, 1, -0.4, 0.3, -0.2)
])

scatterers.set_u_star(u_star=u_star_values)
u_cart_values = scatterers.extract_u_cart(unit_cell=unit_cell)

# Scale atomic displacement parameters
scatterers.scale_adps(scale_factor=1.5)
# CODE_EXAMPLE_STOP
```

## API Reference

### Hendrickson-Lattman Functions
- `hendrickson_lattman(a: flex.double, b: flex.double, c: Optional[flex.double] = None, d: Optional[flex.double] = None)`: Initialize HL coefficients
- `slice(i_param: int) -> flex.double`: Extract parameter slice
- `conj() -> hendrickson_lattman`: Return complex conjugate
- `as_abcd() -> Tuple[flex.double, flex.double, flex.double, flex.double]`: Extract A, B, C, D parameters
- `count(value: Tuple[float, float, float, float]) -> int`: Count occurrences
- `all_eq(value: Tuple[float, float, float, float]) -> flex.bool`: Check if all elements equal
- `__add__(other: hendrickson_lattman) -> hendrickson_lattman`: Array addition
- `__mul__(scalar: float) -> hendrickson_lattman`: Scalar multiplication

### Miller Index Functions
- `miller_index(h: flex.int, k: flex.int, l: flex.int)`: Initialize Miller indices
- `as_vec3_double() -> flex.vec3_double`: Convert to 3D vectors
- `fourier_transform_real_part_at_x(fourier_coeffs: flex.complex_double, x: Tuple[float, float, float]) -> float`: Calculate Fourier transform
- `first_index(miller_index: Tuple[float, float, float]) -> Optional[int]`: Find first occurrence
- `__neg__() -> miller_index`: Negate indices

### X-ray Scatterer Functions
- `xray_scatterer(scatterers: Tuple[xray.scatterer, ...])`: Initialize scatterer array
- `extract_labels() -> flex.std_string`: Get scatterer labels
- `extract_scattering_types() -> flex.std_string`: Get scattering types
- `extract_sites() -> flex.vec3_double`: Get atomic positions
- `set_sites(sites: flex.vec3_double) -> None`: Update positions
- `extract_occupancies() -> flex.double`: Get occupancy values
- `set_occupancies(occupancies: flex.double) -> None`: Update occupancies
- `extract_fps() -> flex.double`: Get f' values
- `set_fps(fps: flex.double) -> None`: Update f' values
- `extract_fdps() -> flex.double`: Get f'' values
- `set_fdps(fdps: flex.double) -> None`: Update f'' values
- `extract_u_iso() -> flex.double`: Get isotropic B-factors
- `set_u_iso(u_iso: flex.double, selection: flex.bool, unit_cell: Any) -> None`: Update isotropic B-factors
- `extract_u_star() -> flex.sym_mat3_double`: Get anisotropic B-factors
- `set_u_star(u_star: flex.sym_mat3_double) -> None`: Update anisotropic B-factors
- `extract_u_cart(unit_cell: Any) -> flex.sym_mat3_double`: Get Cartesian B-factors
- `set_u_cart(unit_cell: Any, u_cart: flex.sym_mat3_double) -> None`: Update Cartesian B-factors
- `count_anisotropic() -> int`: Count anisotropic scatterers
- `count_anomalous() -> int`: Count anomalous scatterers
- `convert_to_isotropic(unit_cell: Any) -> None`: Convert to isotropic
- `convert_to_anisotropic(unit_cell: Any) -> None`: Convert to anisotropic
- `scale_adps(scale_factor: float) -> None`: Scale atomic displacement parameters
- `sites_mod_positive() -> xray_scatterer`: Get positive site modifications
- `sites_mod_short() -> xray_scatterer`: Get short site modifications
- `n_grad_u_iso() -> int`: Count gradient U_iso parameters
- `n_grad_u_aniso() -> int`: Count gradient U_aniso parameters
- `extract_grad_u_iso() -> flex.bool`: Extract gradient U_iso flags

## Configuration

The module requires:
- **C++ Compilation**: The C++ extensions must be compiled with SCons
- **Boost.Python**: For Python-C++ bindings
- **CCTBX Dependencies**: `scitbx.array_family.flex`, `cctbx.uctbx`, `cctbx.xray`

## Data Flow

### Input Formats
- **Hendrickson-Lattman**: A, B, C, D parameters as `flex.double` arrays
- **Miller Indices**: h, k, l indices as `flex.int` arrays
- **X-ray Scatterers**: `xray.scatterer` objects with atomic properties

### Processing Steps
1. **Array Creation**: Initialize specialized arrays from input data
2. **Mathematical Operations**: Perform crystallographic calculations
3. **Data Extraction**: Extract specific properties or transformed data
4. **Data Modification**: Update array contents with new values

### Output Formats
- **Hendrickson-Lattman**: 4-parameter coefficient arrays
- **Miller Indices**: 3D vector arrays or Fourier transform values
- **X-ray Scatterers**: Atomic properties in various coordinate systems

## Common Use Cases

### 1. Phase Refinement with Hendrickson-Lattman Coefficients
```python
# CODE_EXAMPLE_START
# Use case: Phase refinement in crystallography
from cctbx.array_family import flex

# Initialize HL coefficients from experimental data
a_coeffs = flex.double([1.2, 0.8, 1.5])
b_coeffs = flex.double([0.3, 0.7, 0.2])
hl_coeffs = flex.hendrickson_lattman(a=a_coeffs, b=b_coeffs)

# Extract individual parameters for analysis
a_params = hl_coeffs.slice(0)
b_params = hl_coeffs.slice(1)

# Perform mathematical operations
hl_scaled = hl_coeffs * 1.5
hl_conj = hl_coeffs.conj()

# Extract all parameters for output
a, b, c, d = hl_coeffs.as_abcd()
# CODE_EXAMPLE_STOP
```

### 2. Fourier Transform Calculations with Miller Indices
```python
# CODE_EXAMPLE_START
# Use case: Calculate electron density from structure factors
from cctbx.array_family import flex

# Create Miller indices for reflections
h = flex.int([1, 2, 3, 4, 5])
k = flex.int([0, 1, 2, 3, 4])
l = flex.int([1, 1, 1, 1, 1])
miller_indices = flex.miller_index(h=h, k=k, l=l)

# Structure factors (complex numbers)
structure_factors = flex.complex_double([
    1.0+0.5j, 0.8+0.3j, 0.6+0.2j, 0.4+0.1j, 0.2+0.05j
])

# Calculate electron density at specific point
point = (0.1, 0.2, 0.3)
density_value = miller_indices.fourier_transform_real_part_at_x(
    fourier_coeffs=structure_factors, x=point)

# Convert to 3D vectors for visualization
vectors = miller_indices.as_vec3_double()
# CODE_EXAMPLE_STOP
```

### 3. Structural Refinement with X-ray Scatterers
```python
# CODE_EXAMPLE_START
# Use case: Refine atomic parameters in crystal structure
from cctbx.array_family import flex
from cctbx import xray, uctbx

# Create scatterers for different atom types
si_atom = xray.scatterer("Si1", (0.1, 0.2, 0.3), occupancy=1.0)
o_atom = xray.scatterer("O1", (0.2, 0.3, 0.4), occupancy=0.9, u_iso=0.02)
k_atom = xray.scatterer("K1", (0.3, 0.4, 0.5), fp=5, fdp=7)

# Create scatterer array
scatterers = flex.xray_scatterer((si_atom, o_atom, k_atom))

# Extract current parameters
current_sites = scatterers.extract_sites()
current_occupancies = scatterers.extract_occupancies()

# Update with refined parameters
new_sites = flex.vec3_double([
    (0.105, 0.195, 0.305),  # Refined Si position
    (0.195, 0.305, 0.395),  # Refined O position
    (0.295, 0.395, 0.495)   # Refined K position
])
scatterers.set_sites(sites=new_sites)

# Update B-factors
new_u_iso = flex.double([0.01, 0.025, 0.03])
scatterers.set_u_iso(u_iso=new_u_iso, 
                     selection=flex.bool(scatterers.size(), True))

# Convert to anisotropic for detailed refinement
unit_cell = uctbx.unit_cell((10, 11, 12))
scatterers.convert_to_anisotropic(unit_cell=unit_cell)

# Scale atomic displacement parameters
scatterers.scale_adps(scale_factor=1.1)
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues

1. **Issue**: ImportError for C++ extensions
   - **Cause**: C++ extensions not compiled or Boost.Python not available
   - **Solution**: Ensure CCTBX is properly built with `libtbx.configure`
   - **Prevention**: Check build environment and dependencies

2. **Issue**: Type hints not working in IDE
   - **Cause**: Stub file not recognized or typing imports missing
   - **Solution**: Ensure `flex.pyi` is in the same directory as `flex.py`
   - **Code Example**: 
   ```python
   # CODE_EXAMPLE_START
   # Verify type hints are working
   from cctbx.array_family import flex
   
   # IDE should show type hints for these
   hl = flex.hendrickson_lattman(a=flex.double([1,2,3]), b=flex.double([4,5,6]))
   sites = hl.slice(0)  # Should show return type as flex.double
   # CODE_EXAMPLE_STOP
   ```

3. **Issue**: Array size mismatches
   - **Cause**: Input arrays have different sizes
   - **Solution**: Ensure all input arrays have the same size
   - **Prevention**: Check array sizes before operations

4. **Issue**: Unit cell required for certain operations
   - **Cause**: Some operations require unit cell information
   - **Solution**: Provide unit cell parameter
   - **Code Example**:
   ```python
   # CODE_EXAMPLE_START
   # Correct usage with unit cell
   from cctbx import uctbx
   from cctbx.array_family import flex
   
   unit_cell = uctbx.unit_cell((10, 11, 12))
   scatterers = flex.xray_scatterer(...)
   
   # Now this will work
   scatterers.convert_to_anisotropic(unit_cell=unit_cell)
   # CODE_EXAMPLE_STOP
   ```

### Error Messages
- `CCTBX_ASSERT(a.size() == b.size())`: Array size mismatch - ensure all input arrays have same size
- `ImportError: No module named 'cctbx_array_family_flex_ext'`: C++ extensions not compiled
- `TypeError: argument 1 must be flex.double, not list`: Use proper flex array types instead of Python lists

### Performance Tips
- **Use flex arrays**: Convert Python lists to flex arrays for better performance
- **Batch operations**: Use array operations instead of loops when possible
- **Memory management**: Large arrays benefit from explicit memory management
- **Type consistency**: Use consistent data types to avoid conversions

## Dependencies
- `scitbx.array_family.flex`: Base array functionality
- `boost_adaptbx.boost.python`: Python-C++ bindings
- `cctbx.uctbx`: Unit cell operations
- `cctbx.xray`: X-ray scatterer definitions
- `typing`: Type hint support (for stub file)

## Testing
```python
# CODE_EXAMPLE_START
# Example test cases
import pytest
from cctbx.array_family import flex

def test_hendrickson_lattman_basic():
    a = flex.double([1, 2, 3])
    b = flex.double([4, 5, 6])
    hl = flex.hendrickson_lattman(a=a, b=b)
    assert hl.size() == 3
    assert hl.slice(0).all_eq(a)
    assert hl.slice(1).all_eq(b)

def test_miller_index_operations():
    h = flex.int([1, 2, 3])
    k = flex.int([0, 1, 2])
    l = flex.int([1, 1, 1])
    mi = flex.miller_index(h=h, k=k, l=l)
    assert mi.size() == 3
    vec3 = mi.as_vec3_double()
    assert vec3.size() == 3

def test_xray_scatterer_operations():
    from cctbx import xray
    scatterer = xray.scatterer("Si1", (0.1, 0.2, 0.3))
    scatterers = flex.xray_scatterer((scatterer,))
    assert scatterers.size() == 1
    labels = scatterers.extract_labels()
    assert list(labels) == ["Si1"]
# CODE_EXAMPLE_STOP
```

## Integration Notes

### Upstream Dependencies
- **scitbx.array_family.flex**: Provides base array functionality
- **cctbx.uctbx**: Unit cell operations for crystallographic calculations
- **cctbx.xray**: X-ray scatterer definitions and operations

### Downstream Components
- **cctbx.refinement**: Uses scatterer arrays for structural refinement
- **cctbx.miller**: Uses Miller index arrays for reflection data
- **cctbx.maptbx**: Uses arrays for electron density calculations

### Shared Resources
- **Memory Management**: Arrays share memory management with scitbx.array_family
- **Type System**: Consistent type system across CCTBX modules
- **Serialization**: Pickle support for all array types

## Changelog/Version Notes

### Recent Changes
- **Added Type Hints**: Comprehensive type annotations via `flex.pyi` stub file
- **Enhanced Documentation**: Runtime docstring injection for all exposed functions
- **Improved IDE Support**: Better autocomplete and IntelliSense support

### Compatibility
- **Python 2/3**: Compatible with both Python 2.7 and Python 3.x
- **CCTBX Versions**: Compatible with CCTBX 2023.1 and later
- **Boost.Python**: Requires Boost.Python 1.65 or later

### Performance Notes
- **C++ Implementation**: Core functionality implemented in C++ for optimal performance
- **Memory Efficiency**: Uses scitbx.array_family for efficient memory management
- **Vectorization**: Array operations are vectorized where possible 