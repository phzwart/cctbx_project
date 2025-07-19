# cctbx.command_line

## Overview
The `cctbx.command_line` directory contains command-line utilities and scripts for the Computational Crystallography Toolbox (cctbx). These tools provide entry points for crystallographic data processing, analysis, and utility operations, serving as both user-facing commands and programmatic interfaces for automation and integration.

## Architecture
This directory is organized as a collection of standalone Python scripts, each acting as a command-line entry point for a specific crystallographic task. Most scripts follow a pattern of parsing command-line arguments, invoking core cctbx or related library functionality, and printing results or writing output files. Some scripts wrap more complex workflows, while others provide simple utility functions.

- **Entry Points**: Each script is typically invoked as a command-line tool.
- **Core Logic**: Most scripts delegate heavy computation to cctbx core modules or submodules (e.g., `cctbx.sgtbx`, `cctbx.maptbx`).
- **Argument Parsing**: Many scripts use `libtbx.option_parser` or `iotbx.phil` for flexible argument parsing.
- **Output**: Results are printed to stdout, written to files, or visualized via plotting libraries.

## Key Components

### subgroups.py
**Purpose**: Lists subgroups of space groups, either all or specified by symbol/number.
**Key Functions**:
- `run(args: List[str])`: Displays subgroups for given space group symbols or numbers.
**Input/Output**: Expects a list of symbols/numbers; prints subgroup info.
**Dependencies**: `cctbx.sgtbx`, `libtbx.utils`

### version.py
**Purpose**: Prints the cctbx version from TAG files or environment.
**Key Functions**:
- `run()`: Prints version string.
**Input/Output**: No input; prints version.
**Dependencies**: `libtbx.env`, `os`

### wavelength_units.py
**Purpose**: Converts between wavelength units (Angstroms and keV).
**Key Functions**:
- `run(args: List[str])`: Converts and prints equivalent values.
**Input/Output**: List of values with units; prints conversion.
**Dependencies**: `cctbx.factor_kev_angstrom`, `libtbx.utils`

### euclidean_model_matching.py
**Purpose**: Matches atomic models using Euclidean distance.
**Key Classes**:
- `match_record`: Stores match statistics.
**Key Functions**:
- `run()`: Loads models, performs matching, prints summary and histogram.
**Input/Output**: Pickle files; prints match stats.
**Dependencies**: `libtbx.easy_pickle`, `cctbx.euclidean_model_matching`, `scitbx.python_utils.dicts`

### find_reticular_twin_laws.py
**Purpose**: Finds reticular twin laws for a given symmetry.
**Key Functions**:
- `run(args: List[str], command_name: str)`: Parses symmetry, prints twin laws.
**Input/Output**: Command-line args; prints twin law info.
**Dependencies**: `cctbx.sgtbx.reticular_twin_laws`, `iotbx.option_parser`

### form_factor_query.py
**Purpose**: Queries atomic form factor tables (Sasaki, Henke) for elements at given wavelengths.
**Key Functions**:
- `run(args: List[str], command_name: str)`: Parses args, queries tables, prints results.
**Input/Output**: Element, wavelength, table; prints form factor values.
**Dependencies**: `cctbx.eltbx`, `libtbx.phil`, `libtbx.utils`

### auto_sharpen.py
**Purpose**: Entry point for automated map sharpening (deprecated in favor of `phenix.map_sharpening`).
**Key Functions**: N/A (delegates to `cctbx.maptbx.auto_sharpen`)
**Input/Output**: Command-line args; runs sharpening or raises deprecation error.
**Dependencies**: `cctbx.maptbx.auto_sharpen`, `libtbx.utils`

### qscore.py
**Purpose**: Runs the qscore program for model-map validation.
**Key Functions**: N/A (delegates to `cctbx.programs.qscore`)
**Input/Output**: Command-line args; runs qscore.
**Dependencies**: `iotbx.cli_parser`, `cctbx.programs.qscore`

### samosa_join.py / samosa_scale.py
**Purpose**: Entry points for Samosa merging and scaling workflows.
**Key Functions**: N/A (delegates to `cctbx.examples.merging.samosa`)
**Input/Output**: Command-line args; runs join/scale, optionally shows plots.
**Dependencies**: `cctbx.examples.merging.samosa`, `wxtbx.command_line`

### segment_and_split_map.py
**Purpose**: Segments a map and writes out one map per segment.
**Key Functions**: N/A (delegates to `cctbx.maptbx.segment_and_split_map`)
**Input/Output**: Command-line args; runs segmentation.
**Dependencies**: `cctbx.maptbx.segment_and_split_map`

### space_group_info.py
**Purpose**: Displays detailed information about space groups.
**Key Functions**:
- `run(args: List[str])`: Prints info for specified space groups.
**Input/Output**: List of symbols; prints group info.
**Dependencies**: `cctbx.sgtbx`, `libtbx.option_parser`, `scitbx.matrix`

### structure_factor_timings.py
**Purpose**: Benchmarks structure factor calculation methods.
**Key Functions**:
- `timings(structure, d_min, ...)`: Runs timing tests.
- `read_structure(file_name)`: Loads structure from file.
- `run(args: List[str])`: Main entry point.
**Input/Output**: Structure files, d-spacings; prints timing results.
**Dependencies**: `cctbx.xray`, `cctbx.eltbx`, `cctbx.miller`, `iotbx.pdb`, `libtbx.utils`

### brehm_diederichs.py
**Purpose**: Performs Brehm-Diederichs reindexing analysis on multiple datasets.
**Key Functions**:
- `run(args: List[str])`: Processes files, runs analysis, writes reindexed files.
**Input/Output**: Reflection files; writes reindex.txt and reindexed MTZ files.
**Dependencies**: `iotbx.phil`, `cctbx.sgtbx`, `cctbx.array_family.flex`, `cctbx.merging.brehm_diederichs`

### cctbx_test_nightly.py
**Purpose**: Runs nightly regression tests for cctbx modules.
**Key Functions**: N/A (delegates to `libtbx.command_line.run_tests_parallel`)
**Input/Output**: None; runs tests, exits with status.
**Dependencies**: `libtbx.command_line.run_tests_parallel`, `libtbx.env`

## Usage Examples

### Basic Usage
```python
# CODE_EXAMPLE_START
# List subgroups for space group 19
from cctbx.command_line import subgroups
subgroups.run(["19"])
# CODE_EXAMPLE_STOP
```

### Advanced Usage
```python
# CODE_EXAMPLE_START
# Find reticular twin laws for a given MTZ file
from cctbx.command_line import find_reticular_twin_laws
find_reticular_twin_laws.run(["--max_index", "4", "--max_delta", "2.5", "data1.mtz"])
# CODE_EXAMPLE_STOP
```

## API Reference

### Functions
- `subgroups.run(args: List[str]) -> None`: List subgroups for given space group(s).
- `version.run() -> None`: Print cctbx version.
- `wavelength_units.run(args: List[str]) -> None`: Convert between wavelength units.
- `euclidean_model_matching.run() -> None`: Perform model matching and print results.
- `find_reticular_twin_laws.run(args: List[str], command_name: str = ...) -> None`: Find reticular twin laws.
- `form_factor_query.run(args: List[str], command_name: str = ...) -> None`: Query form factor tables.
- `space_group_info.run(args: List[str]) -> None`: Print space group information.
- `structure_factor_timings.run(args: List[str]) -> None`: Run structure factor timing benchmarks.
- `brehm_diederichs.run(args: List[str]) -> None`: Run Brehm-Diederichs analysis.

### Classes
- `euclidean_model_matching.match_record`: Stores match statistics
  - `__init__(n_matches: int, model_size: int)`: Initialize record
  - `__repr__() -> str`: String representation

## Configuration
- Many scripts accept command-line arguments (see each script's help or docstring)
- Some use PHIL or option_parser for flexible configuration
- Environment variables (e.g., `BOOST_ADAPTBX_FPE_DEFAULT` in `brehm_diederichs.py`)
- TAG files for versioning (`version.py`)

## Data Flow
- **Input**: Command-line arguments, structure files (PDB, MTZ, pickle), PHIL/option_parser configs
- **Processing**: Delegation to cctbx core modules for computation
- **Output**: Printed results, output files (e.g., reindexed MTZ, segmented maps), plots (optional)

## Common Use Cases
1. **List Subgroups of a Space Group**
```python
# CODE_EXAMPLE_START
from cctbx.command_line import subgroups
subgroups.run(["P 21 21 21"])
# CODE_EXAMPLE_STOP
```

2. **Convert Wavelength Units**
```python
# CODE_EXAMPLE_START
from cctbx.command_line import wavelength_units
wavelength_units.run(["1.0A", "12.398keV"])
# CODE_EXAMPLE_STOP
```

3. **Run Structure Factor Timing Benchmarks**
```python
# CODE_EXAMPLE_START
from cctbx.command_line import structure_factor_timings
structure_factor_timings.run(["model.pdb", "2.0", "1.5"])
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues
1. **Missing Dependencies**
   - **Cause**: Required cctbx or libtbx modules not installed
   - **Solution**: Ensure cctbx and all dependencies are installed and in PYTHONPATH
   - **Prevention**: Use official build instructions

2. **File Not Found or Format Error**
   - **Cause**: Input file path is incorrect or file format is unsupported
   - **Solution**: Check file path and format; use supported file types (PDB, MTZ, pickle)
   - **Code Example**:
   ```python
   # CODE_EXAMPLE_START
   from cctbx.command_line import structure_factor_timings
   try:
       structure_factor_timings.run(["missing.pdb"])
   except RuntimeError as e:
       print("Error:", e)
   # CODE_EXAMPLE_STOP
   ```

### Error Messages
- `Usage: ...`: Indicates incorrect or missing arguments; check script usage
- `RuntimeError: Unknown file format`: Input file is not recognized; use supported formats
- `Sorry: ...`: Indicates a deprecated command or invalid input; check documentation

### Performance Tips
- For large datasets, use multiprocessing options where available (e.g., `brehm_diederichs.py`)
- Use only required options to minimize memory usage
- For benchmarking, run on dedicated hardware for consistent results

## Dependencies
- `cctbx`: Core crystallography library
- `libtbx`: Utilities, argument parsing, environment
- `iotbx`: File I/O for crystallographic formats
- `scitbx`: Scientific computation utilities
- `wxtbx`: Plotting (optional, for some scripts)
- `pytest`: For testing (optional)

## Testing
```python
# CODE_EXAMPLE_START
import pytest
from cctbx.command_line import subgroups

def test_subgroups():
    # Should not raise
    subgroups.run(["P 21 21 21"])
# CODE_EXAMPLE_STOP
```

## Integration Notes
- Expects cctbx and dependencies to be installed and configured
- Provides command-line entry points for use in pipelines and GUIs
- Can be called from other Python code for automation
- Shares state via environment and configuration files (e.g., PHIL, option_parser)

## Changelog/Version Notes
- See `version.py` and TAG files for version information
- Deprecated commands (e.g., `auto_sharpen.py`) will raise errors and suggest alternatives
- Recent changes: Added type hints and docstrings for improved maintainability and RAG support 