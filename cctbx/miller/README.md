# CCTBX Miller Index Package

## Overview

The `cctbx.miller` package provides comprehensive functionality for handling Miller indices and diffraction data in crystallography. It serves as the core component for managing reciprocal space data, including structure factors, intensities, and phases. The package supports both symmetric and asymmetric data handling, with extensive capabilities for data manipulation, analysis, and visualization.

## Architecture

The package is organized around several key components:

- **Core Data Structures**: `set` and `array` classes for managing Miller indices and associated data
- **Binning System**: Resolution-based data organization and analysis
- **Symmetry Operations**: Handling of space group symmetry and asymmetric units
- **Data Processing**: Merging, scaling, and statistical analysis
- **Visualization**: 2D and 3D display capabilities
- **File I/O**: Support for multiple crystallographic data formats

### Code Organization Note

This package exhibits what is known as the "God-like anti-pattern," where core classes (particularly `set` and `array`) have grown to contain hundreds of methods over 20+ years of organic scientific code development. While a redesign with better separation of concerns would be beneficial, the current implementation prioritizes functionality and backward compatibility over architectural purity. The extensive method collections reflect the real-world needs of crystallographic research rather than theoretical software design principles.

## Key Components

### Miller Set (`set` class)
**Purpose**: Represents a collection of Miller indices with associated crystal symmetry
**Key Functions**:
- `indices()`: Access Miller indices
- `space_group_info()`: Get space group information
- `anomalous_flag()`: Check if data includes anomalous pairs
- `d_min()`, `d_max()`: Resolution limits
- `completeness()`: Calculate data completeness
- `map_to_asu()`: Map indices to asymmetric unit

**Input/Output**: Crystal symmetry, Miller indices, anomalous flag
**Dependencies**: `cctbx.crystal`, `cctbx.sgtbx`, `cctbx.array_family`

### Miller Array (`array` class)
**Purpose**: Extends Miller set with associated data (amplitudes, intensities, phases)
**Key Functions**:
- `data()`: Access numerical data
- `sigmas()`: Access uncertainty estimates
- `amplitudes()`, `intensities()`, `phases()`: Data type conversions
- `merge_equivalents()`: Merge symmetry-equivalent reflections
- `scale()`: Scale data against reference
- `wilson_plot()`: Wilson plot analysis

**Input/Output**: Miller set + numerical data arrays
**Dependencies**: `set` class, `flex.double`, `flex.complex_double`

### Binning System (`binner` class)
**Purpose**: Organize data into resolution bins for analysis
**Key Functions**:
- `counts_given()`: Get reflection counts per bin
- `counts_complete()`: Get expected counts for complete data
- `bin_legend()`: Generate bin descriptions
- `show_summary()`: Display binning statistics

**Input/Output**: Binning scheme, Miller set, bin assignments
**Dependencies**: `bins.h`, `index_span.h`

### Display System (`display.py`)
**Purpose**: Visualize Miller data in 2D and 3D
**Key Functions**:
- `scene`: 3D visualization data structure
- `render_2d`: 2D rendering capabilities
- `generate_systematic_absences()`: Show systematic absences

**Input/Output**: Miller arrays, visualization settings, graphical output
**Dependencies**: `libtbx.phil`, `cctbx.crystal`

### Reindexing Assistant (`reindexing.py`)
**Purpose**: Handle indexing ambiguities and symmetry operations
**Key Functions**:
- `assistant`: Analyze indexing ambiguities
- `show_summary()`: Display reindexing options

**Input/Output**: Lattice symmetry, intensity symmetry, Miller indices
**Dependencies**: `cctbx.sgtbx.cosets`

## Usage Examples

### Basic Usage
```python
# CODE_EXAMPLE_START
# Simple example showing the most common use case
from cctbx import miller
from cctbx import crystal
from cctbx.array_family import flex

# Create crystal symmetry
symmetry = crystal.symmetry(
    unit_cell=(10, 10, 10, 90, 90, 90),
    space_group_symbol="P1")

# Generate Miller indices
indices = flex.miller_index(((1,0,0), (0,1,0), (1,1,0)))

# Create Miller set
miller_set = miller.set(
    crystal_symmetry=symmetry,
    indices=indices,
    anomalous_flag=False)

# Create Miller array with data
data = flex.double((1.0, 2.0, 3.0))
miller_array = miller.array(
    miller_set=miller_set,
    data=data)

print(f"Array size: {miller_array.size()}")
print(f"Resolution range: {miller_array.d_min():.2f} - {miller_array.d_max():.2f}")
# CODE_EXAMPLE_STOP
```

### Advanced Usage
```python
# CODE_EXAMPLE_START
# More complex example showing advanced features
from cctbx import miller
from cctbx import crystal
from cctbx.array_family import flex
import math

# Create complex crystal symmetry
symmetry = crystal.symmetry(
    unit_cell=(50, 50, 50, 90, 90, 90),
    space_group_symbol="P212121")

# Generate complete set of Miller indices
complete_set = symmetry.build_miller_set(
    anomalous_flag=True,
    d_min=2.0)

# Create synthetic structure factor data
n_reflections = complete_set.size()
amplitudes = flex.double(n_reflections)
phases = flex.double(n_reflections)

for i in range(n_reflections):
    # Simple synthetic data
    d_star_sq = complete_set.d_star_sq()[i]
    amplitudes[i] = math.exp(-d_star_sq * 20)  # Wilson-like falloff
    phases[i] = 0.0  # Random phases would be more realistic

# Create complex structure factors
f_complex = amplitudes * flex.cos(phases) + 1j * amplitudes * flex.sin(phases)
miller_array = miller.array(
    miller_set=complete_set,
    data=f_complex)

# Analyze data
print(f"Total reflections: {miller_array.size()}")
print(f"Completeness: {miller_array.completeness():.1%}")
print(f"Mean amplitude: {miller_array.mean():.3f}")

# Setup binning for analysis
binner = miller_array.setup_binner(
    d_max=5.0,
    d_min=2.0,
    n_bins=10)

# Wilson plot
wilson_stats = miller_array.wilson_plot(use_binning=True)
print(f"Wilson B-factor: {wilson_stats.b_wilson:.1f}")
# CODE_EXAMPLE_STOP
```

### Data Processing Workflow
```python
# CODE_EXAMPLE_START
# Example showing data processing workflow
from cctbx import miller
from cctbx import crystal
from cctbx.array_family import flex

# Load experimental data (simulated here)
symmetry = crystal.symmetry(
    unit_cell=(50, 50, 50, 90, 90, 90),
    space_group_symbol="P1")

# Create "observed" data with noise
complete_set = symmetry.build_miller_set(
    anomalous_flag=False,
    d_min=2.0)

n_reflections = complete_set.size()
f_obs_data = flex.double(n_reflections)
f_obs_sigmas = flex.double(n_reflections)

import random
random.seed(42)
for i in range(n_reflections):
    d_star_sq = complete_set.d_star_sq()[i]
    # Wilson-like intensity with noise
    intensity = math.exp(-d_star_sq * 15) * (1 + 0.1 * random.gauss(0, 1))
    f_obs_data[i] = math.sqrt(max(intensity, 0))
    f_obs_sigmas[i] = f_obs_data[i] * 0.05  # 5% error

# Create observed data array
f_obs = miller.array(
    miller_set=complete_set,
    data=f_obs_data,
    sigmas=f_obs_sigmas)

# Remove systematic absences
f_obs_clean = f_obs.remove_systematic_absences()

# Merge equivalent reflections
merged = f_obs_clean.merge_equivalents()
print(f"R-merge: {merged.r_merge():.3f}")
print(f"R-meas: {merged.r_meas():.3f}")

# Resolution filtering
high_res = f_obs_clean.resolution_filter(d_min=2.5)
print(f"High resolution reflections: {high_res.size()}")

# Generate R-free flags
r_free_flags = f_obs_clean.generate_r_free_flags(
    fraction=0.1,
    max_free=2000)
# CODE_EXAMPLE_STOP
```

## API Reference

### Core Classes

#### `set` class
- `__init__(crystal_symmetry, indices, anomalous_flag=None)`: Initialize Miller set
- `indices() -> flex.miller_index`: Get Miller indices
- `size() -> int`: Number of reflections
- `d_min() -> float`: Minimum d-spacing
- `d_max() -> float`: Maximum d-spacing
- `completeness(use_binning=False, d_min_tolerance=1.e-6) -> float`: Data completeness
- `map_to_asu() -> set`: Map to asymmetric unit
- `expand_to_p1() -> set`: Expand to P1 symmetry
- `change_basis(cb_op) -> set`: Apply change of basis

#### `array` class
- `__init__(miller_set, data=None, sigmas=None)`: Initialize Miller array
- `data() -> flex.double`: Get data values
- `sigmas() -> flex.double`: Get uncertainty estimates
- `amplitudes() -> array`: Convert to amplitudes
- `intensities() -> array`: Convert to intensities
- `phases(deg=False) -> array`: Extract phases
- `merge_equivalents(algorithm="gaussian") -> merge_equivalents`: Merge equivalents
- `scale(other, resolution_dependent=False) -> array`: Scale data
- `wilson_plot(use_binning=False) -> wilson_plot`: Wilson plot analysis
- `generate_r_free_flags(fraction=0.1, max_free=2000) -> array`: Generate R-free flags

#### `binner` class
- `__init__(binning, miller_set)`: Initialize binner
- `counts_given() -> List[int]`: Reflection counts per bin
- `counts_complete(include_centric=True, include_acentric=True) -> List[int]`: Expected counts
- `bin_legend(i_bin, show_bin_number=True) -> str`: Bin description
- `show_summary(show_bin_number=True, show_counts=True) -> None`: Display summary

### Utility Functions
- `build_set(crystal_symmetry, anomalous_flag, d_min=None, d_max=None) -> set`: Create complete set
- `union_of_sets(miller_sets) -> set`: Combine multiple sets
- `match_indices(set1, set2) -> match_indices`: Find matching indices

## Configuration

The package uses several configuration options:

### Crystal Symmetry
- Unit cell parameters (a, b, c, α, β, γ)
- Space group symbol or information
- Anomalous flag for data type

### Binning Parameters
- Resolution limits (d_max, d_min)
- Number of bins or reflections per bin
- Binning algorithm (linear, logarithmic, etc.)

### Data Processing
- Merging algorithm (gaussian, simple)
- Scaling method (resolution-dependent, global)
- R-free flag generation parameters

## Data Flow

### Input Formats
- **Miller Indices**: Integer triplets (h, k, l)
- **Crystal Symmetry**: Unit cell + space group
- **Data Arrays**: Amplitudes, intensities, phases, or complex values
- **Uncertainties**: Sigma values for error estimation

### Processing Steps
1. **Index Generation**: Create Miller indices based on symmetry
2. **Symmetry Operations**: Apply space group operations
3. **Data Association**: Attach numerical data to indices
4. **Quality Control**: Remove systematic absences, outliers
5. **Merging**: Combine symmetry-equivalent reflections
6. **Analysis**: Statistical analysis, scaling, normalization

### Output Formats
- **Miller Arrays**: Data with associated indices and symmetry
- **Binned Data**: Resolution-dependent statistics
- **Maps**: Electron density maps via FFT
- **Files**: MTZ, CIF, CNS, SHELX formats

## Common Use Cases

1. **Data Loading and Validation**
```python
# CODE_EXAMPLE_START
# Load and validate diffraction data
from cctbx import miller
from cctbx import crystal

# Load from file (example)
# miller_array = miller.array.from_mtz("data.mtz")

# Validate data quality
print(f"Data completeness: {miller_array.completeness():.1%}")
print(f"Resolution range: {miller_array.d_min():.2f} - {miller_array.d_max():.2f}")

# Check for systematic absences
sys_absent = miller_array.sys_absent_flags()
print(f"Systematic absences: {sys_absent.data().count(True)}")

# Remove negative intensities
if miller_array.is_xray_intensity_array():
    miller_array = miller_array.select(miller_array.data() > 0)
# CODE_EXAMPLE_STOP
```

2. **Structure Factor Calculation**
```python
# CODE_EXAMPLE_START
# Calculate structure factors from atomic model
from cctbx import miller
from cctbx import xray

# Create structure
structure = xray.structure(
    crystal_symmetry=crystal_symmetry,
    scatterers=flex.xray_scatterer(
        (xray.scatterer("C", (0,0,0)),)))

# Calculate structure factors
f_calc = miller_array.structure_factors_from_scatterers(
    xray_structure=structure,
    algorithm="direct")

# Compare with observed data
r_factor = miller_array.r1_factor(f_calc)
print(f"R-factor: {r_factor:.3f}")
# CODE_EXAMPLE_STOP
```

3. **Map Generation and Analysis**
```python
# CODE_EXAMPLE_START
# Generate electron density maps
from cctbx import miller

# Create difference map
f_obs = miller_array
f_calc = f_calc_array
f_diff = f_obs.f_obs_minus_f_calc(f_obs_factor=1.0, f_calc=f_calc)

# Generate map
fft_map = f_diff.fft_map(
    resolution_factor=1/3,
    grid_step=0.5)

# Access map data
map_data = fft_map.real_map()
print(f"Map statistics: min={map_data.min():.3f}, max={map_data.max():.3f}")

# Save map
fft_map.as_ccp4_map("difference_map.ccp4")
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues

1. **Issue**: "No data selected" error in binning
   - **Cause**: Resolution limits exclude all data
   - **Solution**: Check d_min and d_max parameters
   - **Prevention**: Verify resolution range before binning
   ```python
   # CODE_EXAMPLE_START
   # Example of correct usage
   from cctbx import miller
   
   # Check resolution range first
   print(f"Data range: {miller_array.d_min():.2f} - {miller_array.d_max():.2f}")
   
   # Use safe binning
   binner = miller_array.safe_setup_binner(
       n_bins=10,
       min_in_bin=10)
   # CODE_EXAMPLE_STOP
   ```

2. **Issue**: Symmetry mismatch between arrays
   - **Cause**: Arrays have different space groups or unit cells
   - **Solution**: Ensure compatible symmetry before operations
   - **Code Example**: 
   ```python
   # CODE_EXAMPLE_START
   # Example of correct usage
   from cctbx import miller
   
   # Check symmetry compatibility
   if not array1.crystal_symmetry().is_similar_symmetry(array2.crystal_symmetry()):
       print("Symmetry mismatch detected")
       # Apply change of basis if needed
       array2 = array2.change_basis(change_of_basis_op)
   # CODE_EXAMPLE_STOP
   ```

3. **Issue**: Memory errors with large datasets
   - **Cause**: Insufficient memory for complete operations
   - **Solution**: Use binning or selection to reduce memory usage
   - **Prevention**: Process data in chunks or use resolution filtering

### Error Messages
- `Sorry: No data in resolution range`: Adjust d_min/d_max parameters
- `RuntimeError: Unexpected data type`: Check data type compatibility
- `ValueError: Symmetry mismatch`: Verify crystal symmetry compatibility

### Performance Tips
- Use `setup_binner()` for large datasets to enable binning operations
- Apply resolution filters early to reduce memory usage
- Use `map_to_asu()` to work with asymmetric unit only
- Consider using `expand_to_p1()` sparingly as it multiplies data size

## Dependencies
- `cctbx.crystal`: Crystal symmetry handling
- `cctbx.sgtbx`: Space group operations
- `cctbx.array_family`: Array data structures
- `scitbx.math`: Mathematical utilities
- `libtbx`: Utility functions and error handling

## Testing
```python
# CODE_EXAMPLE_START
# Example test cases
import pytest
from cctbx import miller
from cctbx import crystal
from cctbx.array_family import flex

def test_basic_functionality():
    # Create test data
    symmetry = crystal.symmetry(
        unit_cell=(10, 10, 10, 90, 90, 90),
        space_group_symbol="P1")
    
    indices = flex.miller_index(((1,0,0), (0,1,0)))
    data = flex.double((1.0, 2.0))
    
    miller_set = miller.set(
        crystal_symmetry=symmetry,
        indices=indices,
        anomalous_flag=False)
    
    miller_array = miller.array(
        miller_set=miller_set,
        data=data)
    
    assert miller_array.size() == 2
    assert miller_array.d_min() > 0

def test_binning():
    # Test binning functionality
    symmetry = crystal.symmetry(
        unit_cell=(20, 20, 20, 90, 90, 90),
        space_group_symbol="P1")
    
    complete_set = symmetry.build_miller_set(
        anomalous_flag=False,
        d_min=2.0)
    
    binner = complete_set.setup_binner(
        d_max=5.0,
        d_min=2.0,
        n_bins=5)
    
    assert binner.n_bins_used() == 5
# CODE_EXAMPLE_STOP
```

## Integration Notes

### Upstream Components
- **Crystal Symmetry**: Requires valid unit cell and space group
- **Data Sources**: MTZ files, CIF files, or synthetic data
- **Atomic Models**: For structure factor calculations

### Downstream Components
- **Map Generation**: Provides Fourier coefficients for FFT
- **Refinement**: Supplies observed data for structure refinement
- **Analysis Tools**: Statistical analysis and quality metrics

### Shared Resources
- **Crystal Symmetry**: Passed through all operations
- **Binning Objects**: Reused across multiple analyses
- **R-free Flags**: Shared between refinement and validation

## Changelog/Version Notes

### Recent Additions
- Enhanced type hints throughout the package
- Improved error messages and validation
- Extended support for complex data types
- Enhanced binning algorithms for better performance

### Compatibility Notes
- Python 3.6+ required for type hints
- CCTBX 2023.1+ recommended for full functionality
- Backward compatibility maintained for core functionality 