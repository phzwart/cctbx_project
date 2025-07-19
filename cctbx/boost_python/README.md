# CCTBX Boost.Python Extensions

## Overview

The `cctbx/boost_python` directory contains C++ Boost.Python extension modules that provide high-performance implementations of crystallographic algorithms. These extensions are compiled into shared libraries and imported by Python wrapper modules to expose C++ functionality to Python code.

This directory serves as the bridge between the high-performance C++ core of CCTBX and the Python interface, enabling fast execution of computationally intensive crystallographic operations while maintaining the flexibility and ease of use of Python.

## Architecture

The directory follows a consistent pattern where each C++ extension file (`*_ext.cpp`) corresponds to a specific domain of crystallographic functionality:

- **`french_wilson_ext.cpp`**: French-Wilson scaling algorithms for intensity correction
- **`orientation_ext.cpp`**: Crystal orientation matrix operations and transformations  
- **`statistics_ext.cpp`**: Statistical analysis tools for crystallographic data
- **`emma_ext.cpp`**: Euclidean model matching for structure superposition

Each extension is compiled into a shared library (e.g., `libcctbx_french_wilson_ext.so`) and imported by corresponding Python modules that provide additional functionality and type hints.

## Key Components

### French-Wilson Scaling (`french_wilson_ext.cpp`)

**Purpose**: Provides high-performance implementations of French-Wilson scaling algorithms for correcting intensity data.

**Key Functions**:
- `expectEFW(eosq, sigesq, centric)`: Calculate expected E values for French-Wilson scaling
- `expectEsqFW(eosq, sigesq, centric)`: Calculate expected E² values for French-Wilson scaling  
- `is_FrenchWilson(F, SIGF, is_centric, eps)`: Determine if data follows French-Wilson statistics

**Input/Output**: Takes intensity data and returns corrected intensities and amplitudes
**Dependencies**: CCTBX core libraries, Boost.Python

**Python Interface**: `cctbx/french_wilson.py` provides the main Python API with type hints and docstrings.

### Crystal Orientation (`orientation_ext.cpp`)

**Purpose**: Handles crystal orientation matrices and their transformations in both direct and reciprocal space.

**Key Functions**:
- `crystal_orientation` class: Core orientation matrix class with methods for:
  - `unit_cell()`: Get direct space unit cell
  - `unit_cell_inverse()`: Get reciprocal space unit cell  
  - `direct_matrix()`: Get direct space orientation matrix
  - `reciprocal_matrix()`: Get reciprocal space orientation matrix
  - `change_basis()`: Transform orientation by change of basis operator
  - `rotate_thru()`: Apply rotation to orientation matrix
  - `best_similarity_transformation()`: Find optimal transformation between orientations

**Input/Output**: Takes orientation matrices and returns transformed orientations
**Dependencies**: CCTBX crystal symmetry, Boost.Python

**Python Interface**: `cctbx/crystal_orientation.py` extends the C++ class with additional Python methods and type hints.

### Statistical Analysis (`statistics_ext.cpp`)

**Purpose**: Provides fast implementations of crystallographic statistical analysis tools.

**Key Functions**:
- `cumulative_intensity_core` class: Core implementation of cumulative intensity distribution
  - `x()`: Get x-coordinates for plotting
  - `y()`: Get y-coordinates for plotting

**Input/Output**: Takes intensity data and returns statistical distributions
**Dependencies**: CCTBX miller arrays, Boost.Python

**Python Interface**: `cctbx/statistics.py` provides classes like `wilson_plot`, `cumulative_intensity_distribution`, and `sys_absent_intensity_distribution` with type hints and docstrings.

### Euclidean Model Matching (`emma_ext.cpp`)

**Purpose**: Implements algorithms for matching and superposing crystal structures using Euclidean transformations.

**Key Functions**:
- `add_pair` class: Core class for finding pairs of matching sites between structures
  - `next_pivot()`: Find next pivot point for matching
  - `next_pair()`: Find next pair of matching sites
  - `new_pair_1()`: Get first site of current pair
  - `new_pair_2()`: Get second site of current pair

**Input/Output**: Takes atomic positions and returns matching pairs and transformations
**Dependencies**: CCTBX symmetry, Boost.Python

**Python Interface**: `cctbx/euclidean_model_matching.py` provides the main API with classes like `position`, `model`, and functions like `sgtbx_rt_mx_as_matrix_rt`.

## Usage Examples

### Basic Usage

```python
# CODE_EXAMPLE_START
# French-Wilson scaling example
from cctbx import french_wilson
from cctbx.array_family import flex

# Create miller array with intensity data
miller_array = miller.array(miller_set, data=intensities, sigmas=sigmas)

# Perform French-Wilson scaling
scaled_array = french_wilson.french_wilson_scale(
    miller_array=miller_array,
    sigma_iobs_rejection_criterion=-4.0,
    max_bins=60,
    min_bin_size=40
)
# CODE_EXAMPLE_STOP
```

### Advanced Usage

```python
# CODE_EXAMPLE_START
# Crystal orientation manipulation
from cctbx import crystal_orientation
from scitbx import matrix

# Create orientation from reciprocal matrix
recip_matrix = matrix.sqr((1, 0, 0, 0, 1, 0, 0, 0, 1))
orientation = crystal_orientation.crystal_orientation(
    recip_matrix, crystal_orientation.basis_type.reciprocal)

# Apply rotation
rotated = orientation.rotate_thru(
    unit_axis=(0, 0, 1), 
    angle=math.pi/2
)

# Get crystal rotation matrix
U_matrix = orientation.crystal_rotation_matrix()
# CODE_EXAMPLE_STOP
```

### Statistical Analysis

```python
# CODE_EXAMPLE_START
# Wilson plot analysis
from cctbx import statistics

# Create Wilson plot
asu_contents = {"C": 100, "N": 20, "O": 30}
wilson = statistics.wilson_plot(
    f_obs=f_obs_array,
    asu_contents=asu_contents,
    e_statistics=True
)

# Get plot information
plot_info = wilson.xy_plot_info()
print(f"Wilson B-factor: {wilson.wilson_b}")
print(f"Scale factor: {wilson.wilson_k}")
# CODE_EXAMPLE_STOP
```

### Model Matching

```python
# CODE_EXAMPLE_START
# Euclidean model matching
from cctbx import euclidean_model_matching as emma

# Create models from structures
model1 = structure1.as_emma_model()
model2 = structure2.as_emma_model()

# Find matches
matches = emma.model_matches(
    model1=model1,
    model2=model2,
    tolerance=1.5,
    models_are_diffraction_index_equivalent=True
)

# Process results
for match in matches.refined_matches:
    print(f"RMSD: {match.rmsd()}")
    print(f"Pairs: {len(match.pairs)}")
# CODE_EXAMPLE_STOP
```

## API Reference

### Functions

- `french_wilson.fw_acentric(I: float, sigma_I: float, mean_intensity: float, sigma_iobs_rejection_criterion: float) -> Tuple[float, float, float, float]`: French-Wilson scaling for acentric reflections
- `french_wilson.fw_centric(I: float, sigma_I: float, mean_intensity: float, sigma_iobs_rejection_criterion: float) -> Tuple[float, float, float, float]`: French-Wilson scaling for centric reflections
- `french_wilson.f_w_binning(miller_array: Any, max_bins: int = 60, min_bin_size: int = 40, log: Optional[Any] = None) -> bool`: Set up binning for French-Wilson scaling
- `crystal_orientation.crystal_orientation(matrix: Any, basis_type_flag: bool)`: Create crystal orientation object
- `statistics.wilson_plot(f_obs: Any, asu_contents: Dict[str, int], scattering_table: str = "wk1995", e_statistics: bool = False)`: Perform Wilson plot analysis
- `euclidean_model_matching.model_matches(model1: Any, model2: Any, tolerance: float = 1.5, models_are_diffraction_index_equivalent: bool = True)`: Find matches between crystal structures

### Classes

- `crystal_orientation.crystal_orientation`: Crystal orientation matrix class
  - `unit_cell()`: Get direct space unit cell
  - `reciprocal_matrix()`: Get reciprocal space matrix
  - `change_basis(cb_op)`: Apply change of basis transformation
  - `rotate_thru(unit_axis, angle)`: Apply rotation
  - `crystal_rotation_matrix()`: Get U matrix

- `statistics.wilson_plot`: Wilson plot analysis class
  - `wilson_b`: Wilson B-factor
  - `wilson_k`: Scale factor
  - `xy_plot_info()`: Get plotting data

- `euclidean_model_matching.model`: Crystal structure model class
  - `add_position(pos)`: Add atomic position
  - `change_basis(cb_op)`: Apply change of basis
  - `expand_to_p1()`: Expand to P1 symmetry

## Configuration

The extensions are built using the SCons build system with configuration in `SConscript`:

```python
# Build configuration
env.SharedLibrary(target="#lib/cctbx_statistics_ext", source=["statistics_ext.cpp"])
env.SharedLibrary(target="#lib/cctbx_emma_ext", source=["emma_ext.cpp"])
env.SharedLibrary(target="#lib/cctbx_orientation_ext", source=["orientation_ext.cpp"])
env.SharedLibrary(target="#lib/cctbx_french_wilson_ext", source=["french_wilson_ext.cpp"])
```

## Data Flow

### Input Formats
- **Miller Arrays**: Reflection data with indices, intensities, and sigmas
- **Crystal Symmetry**: Unit cell parameters and space group information
- **Atomic Positions**: Cartesian or fractional coordinates with labels
- **Orientation Matrices**: 3x3 transformation matrices in direct or reciprocal space

### Processing Steps
1. **Data Validation**: Check input data types and ranges
2. **Symmetry Operations**: Apply space group symmetry and special positions
3. **Algorithm Execution**: Run C++ implementations for performance
4. **Result Formatting**: Convert C++ results to Python objects

### Output Formats
- **Scaled Data**: Corrected intensities and amplitudes with uncertainties
- **Transformation Matrices**: Rotation and translation operators
- **Statistical Measures**: B-factors, scale factors, correlation coefficients
- **Matching Results**: Pairs of matched sites with RMSD values

## Common Use Cases

1. **Intensity Scaling**: Correct observed intensities using French-Wilson method
```python
# CODE_EXAMPLE_START
# Scale intensities from integration results
from cctbx import french_wilson

# Load integrated data
miller_array = load_integration_data()

# Apply French-Wilson scaling
scaled_array = french_wilson.french_wilson_scale(
    miller_array=miller_array,
    sigma_iobs_rejection_criterion=-4.0
)

# Save scaled data
scaled_array.as_mtz_dataset("scaled.mtz")
# CODE_EXAMPLE_STOP
```

2. **Crystal Orientation Analysis**: Manipulate and analyze crystal orientations
```python
# CODE_EXAMPLE_START
# Analyze crystal orientation from diffraction data
from cctbx import crystal_orientation

# Create orientation from unit cell
uc = unit_cell((50, 60, 70, 90, 90, 90))
orientation = crystal_orientation.crystal_orientation(
    uc.orthogonalization_matrix(), 
    crystal_orientation.basis_type.direct
)

# Apply rotation and get U matrix
rotated = orientation.rotate_thru((0, 0, 1), math.pi/4)
U_matrix = rotated.crystal_rotation_matrix()

# Compare orientations
diff = orientation.direct_mean_square_difference(other_orientation)
# CODE_EXAMPLE_STOP
```

3. **Statistical Quality Assessment**: Analyze data quality using Wilson plots
```python
# CODE_EXAMPLE_START
# Assess data quality with Wilson plot
from cctbx import statistics

# Create Wilson plot
asu_contents = {"C": 150, "N": 30, "O": 40, "S": 2}
wilson = statistics.wilson_plot(
    f_obs=f_obs_array,
    asu_contents=asu_contents,
    e_statistics=True
)

# Check data quality
if wilson.wilson_b > 50:
    print("Warning: High B-factor suggests poor data quality")
if wilson.fit_correlation < 0.8:
    print("Warning: Poor Wilson plot correlation")
# CODE_EXAMPLE_STOP
```

4. **Structure Superposition**: Match and superpose crystal structures
```python
# CODE_EXAMPLE_START
# Superpose two crystal structures
from cctbx import euclidean_model_matching as emma

# Convert structures to models
model1 = structure1.as_emma_model()
model2 = structure2.as_emma_model()

# Find best superposition
matches = emma.model_matches(
    model1=model1,
    model2=model2,
    tolerance=1.0
)

# Apply transformation
if matches.refined_matches:
    best_match = matches.refined_matches[0]
    transformed_model = best_match.get_transformed_model2(template=model2)
    print(f"RMSD: {best_match.rmsd():.3f} Å")
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues

1. **Issue**: Import error for C++ extensions
   - **Cause**: Extensions not compiled or wrong Python version
   - **Solution**: Rebuild extensions with `libtbx.scons`
   - **Prevention**: Ensure consistent Python environment

2. **Issue**: Memory errors with large datasets
   - **Cause**: Insufficient memory for C++ operations
   - **Solution**: Process data in smaller chunks or increase system memory
   - **Code Example**: 
   ```python
   # CODE_EXAMPLE_START
   # Process large datasets in chunks
   from cctbx import french_wilson
   
   # Split large miller array
   chunk_size = 10000
   for i in range(0, len(miller_array), chunk_size):
       chunk = miller_array[i:i+chunk_size]
       scaled_chunk = french_wilson.french_wilson_scale(chunk)
       # Process scaled_chunk
   # CODE_EXAMPLE_STOP
   ```

3. **Issue**: Incorrect crystal orientation results
   - **Cause**: Wrong basis type (direct vs reciprocal) or matrix format
   - **Solution**: Verify matrix format and basis type flags
   - **Prevention**: Use consistent coordinate system conventions

4. **Issue**: Poor Wilson plot fit
   - **Cause**: Data quality issues or incorrect ASU contents
   - **Solution**: Check data quality and verify chemical composition
   - **Code Example**:
   ```python
   # CODE_EXAMPLE_START
   # Debug Wilson plot issues
   from cctbx import statistics
   
   # Check data quality first
   f_obs_positive = f_obs.select(f_obs.data() > 0)
   if len(f_obs_positive) < len(f_obs) * 0.8:
       print("Warning: Many negative intensities")
   
   # Try different scattering tables
   for table in ["wk1995", "it1992", "n_gaussian"]:
       try:
           wilson = statistics.wilson_plot(f_obs, asu_contents, table)
           if wilson.fit_correlation > 0.8:
               break
       except:
           continue
   # CODE_EXAMPLE_STOP
   ```

### Error Messages

- `ImportError: No module named 'cctbx_french_wilson_ext'`: C++ extension not compiled
- `RuntimeError: Too few reflections for accurate binning`: Insufficient data for French-Wilson scaling
- `AssertionError: Invalid crystal orientation matrix`: Matrix format or basis type error
- `ValueError: Wilson plot error: empty bins`: Poor data distribution in resolution shells

### Performance Tips

- **Use C++ Extensions**: Always use the C++ implementations for large datasets
- **Batch Processing**: Process multiple datasets together when possible
- **Memory Management**: Release large arrays when no longer needed
- **Parallel Processing**: Use multiprocessing for independent operations

## Dependencies

List all external dependencies and their purposes:
- `boost.python`: C++ to Python interface library
- `cctbx`: Core crystallographic algorithms and data structures
- `scitbx`: Scientific computing utilities
- `libtbx`: Build system and utilities

## Testing

How to test the functionality:
```python
# CODE_EXAMPLE_START
# Example test cases
import pytest
from cctbx import french_wilson, crystal_orientation, statistics

def test_french_wilson_scaling():
    # Create test miller array
    miller_array = create_test_miller_array()
    
    # Test French-Wilson scaling
    scaled = french_wilson.french_wilson_scale(miller_array)
    assert scaled is not None
    assert len(scaled.data()) > 0

def test_crystal_orientation():
    # Test orientation creation and manipulation
    matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    orientation = crystal_orientation.crystal_orientation(
        matrix, crystal_orientation.basis_type.reciprocal)
    
    # Test basic operations
    uc = orientation.unit_cell()
    assert uc is not None
    
    # Test rotation
    rotated = orientation.rotate_thru((0, 0, 1), 3.14159/2)
    assert rotated is not None

def test_wilson_plot():
    # Test Wilson plot analysis
    f_obs = create_test_f_obs()
    asu_contents = {"C": 100, "N": 20}
    
    wilson = statistics.wilson_plot(f_obs, asu_contents)
    assert wilson.wilson_b is not None
    assert wilson.wilson_k > 0
# CODE_EXAMPLE_STOP
```

## Integration Notes

### Upstream Components
- **Miller Arrays**: Reflection data from integration or merging
- **Crystal Symmetry**: Unit cell and space group information
- **Atomic Structures**: Coordinates and scattering information

### Downstream Components
- **Refinement Programs**: Use scaled intensities and orientations
- **Structure Solution**: Use matched models and transformations
- **Data Analysis**: Use statistical measures for quality assessment

### Shared Resources
- **Memory**: Large arrays shared between C++ and Python
- **File I/O**: MTZ and CIF file formats
- **Symmetry**: Space group and special position information

## Changelog/Version Notes

- **Version 1.0**: Initial implementation of core extensions
- **Version 1.1**: Added type hints and comprehensive docstrings to Python interfaces
- **Version 1.2**: Performance optimizations for large datasets
- **Version 1.3**: Enhanced error handling and validation

## External File Dependencies

This directory's C++ extensions interface with Python files outside this directory:

### `cctbx/french_wilson.py`
- **Purpose**: Main Python interface for French-Wilson scaling
- **Relationship**: Imports `cctbx_french_wilson_ext` and provides high-level functions
- **Key Functions**: `french_wilson_scale()`, `fw_acentric()`, `fw_centric()`
- **Usage**: Primary API for intensity scaling operations

### `cctbx/crystal_orientation.py` 
- **Purpose**: Python wrapper for crystal orientation operations
- **Relationship**: Extends `cctbx_orientation_ext.crystal_orientation` class
- **Key Methods**: `crystal_rotation_matrix()`, `make_positive()`, `reduced_cell()`
- **Usage**: Crystal orientation manipulation and analysis

### `cctbx/statistics.py`
- **Purpose**: Statistical analysis tools for crystallographic data
- **Relationship**: Uses `cctbx_statistics_ext.cumulative_intensity_core`
- **Key Classes**: `wilson_plot`, `cumulative_intensity_distribution`, `sys_absent_intensity_distribution`
- **Usage**: Data quality assessment and statistical analysis

### `cctbx/euclidean_model_matching.py`
- **Purpose**: Structure superposition and matching algorithms
- **Relationship**: Uses `cctbx_emma_ext.add_pair` class
- **Key Classes**: `position`, `model`, `sgtbx_rt_mx_as_matrix_rt`
- **Usage**: Structure comparison and superposition

### `cctbx/command_line/` scripts
- **Purpose**: Command-line interfaces for the extensions
- **Files**: `euclidean_model_matching.py`, `french_wilson.py`
- **Relationship**: Provide user-friendly command-line access to extension functionality
- **Usage**: Direct command-line operation of the algorithms

This architecture allows the C++ extensions to provide high-performance implementations while the Python files offer convenient interfaces, type hints, docstrings, and additional functionality that would be cumbersome to implement in C++. 