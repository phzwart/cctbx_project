# README.md Generation Prompt for Cursor

You are tasked with creating a comprehensive README.md file for this Python subpackage/directory. The README should serve as a complete knowledge base for both humans and RAG systems to understand functionality, usage, and troubleshooting.

## ANALYSIS REQUIREMENTS:

### 1. Code Discovery
- Analyze ALL Python files in the current directory
- Identify all classes, functions, and their purposes
- Map dependencies between modules
- Understand the overall architecture and data flow
- Note any configuration files, constants, or important variables

### 2. Documentation Depth
Create documentation that enables:
- **Human Understanding**: Clear explanations of what each component does
- **RAG System Usage**: Rich context for automated code generation and troubleshooting
- **Code Examples**: Practical usage patterns
- **Troubleshooting**: Common issues and solutions

## README.md STRUCTURE:

```markdown
# [Package/Directory Name]

## Overview
Brief description of what this subpackage does and its role in the larger system.

## Architecture
High-level description of the components and how they interact.

## Key Components

### [Module/Class Name 1]
**Purpose**: What this component does
**Key Functions**:
- `function_name()`: Brief description
- `another_function()`: Brief description

**Input/Output**: What it expects and returns
**Dependencies**: What it relies on

### [Module/Class Name 2]
[Same structure as above]

## Usage Examples

### Basic Usage
```python
# CODE_EXAMPLE_START
# Simple example showing the most common use case
from this_package import MainClass

# Initialize
instance = MainClass(param1="value")

# Common operations
result = instance.process_data(data)
# CODE_EXAMPLE_STOP
```

### Advanced Usage
```python
# CODE_EXAMPLE_START
# More complex example showing advanced features
from this_package import MainClass, HelperClass

# Advanced configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

# Complex workflow
processor = MainClass(config)
helper = HelperClass()
result = processor.advanced_process(data, helper.prepare_data())
# CODE_EXAMPLE_STOP
```

## API Reference

### Functions
- `function_name(param1: type, param2: type) -> return_type`: Description
- `another_function(param: type) -> return_type`: Description

### Classes
- `ClassName`: Purpose and main methods
  - `__init__(params)`: Constructor details
  - `method_name()`: Method descriptions

## Configuration
Detail any configuration options, environment variables, or settings files.

## Data Flow
Describe how data moves through the system, including:
- Input formats expected
- Processing steps
- Output formats produced
- Any transformations applied

## Common Use Cases
1. **Use Case 1**: Description and code example
```python
# CODE_EXAMPLE_START
# Use case 1 implementation
from this_package import SpecificClass

processor = SpecificClass()
result = processor.handle_use_case_1(input_data)
# CODE_EXAMPLE_STOP
```

2. **Use Case 2**: Description and code example
```python
# CODE_EXAMPLE_START
# Use case 2 implementation
from this_package import MainClass, UtilityClass

main = MainClass()
util = UtilityClass()
result = main.process_with_utility(data, util)
# CODE_EXAMPLE_STOP
```

3. **Use Case 3**: Description and code example
```python
# CODE_EXAMPLE_START
# Use case 3 implementation
from this_package import AdvancedClass

advanced = AdvancedClass(config=advanced_config)
result = advanced.complex_operation(complex_data)
# CODE_EXAMPLE_STOP
```

## Troubleshooting

### Common Issues
1. **Issue**: [Common error or problem]
   - **Cause**: Why this happens
   - **Solution**: How to fix it
   - **Prevention**: How to avoid it

2. **Issue**: [Another common problem]
   - **Cause**: Root cause
   - **Solution**: Step-by-step fix
   - **Code Example**: 
   ```python
   # CODE_EXAMPLE_START
   # Example of correct usage
   from this_package import MainClass
   
   # Proper initialization
   instance = MainClass(required_param="value")
   result = instance.safe_operation()
   # CODE_EXAMPLE_STOP
   ```

### Error Messages
- `ErrorType: Error message`: What causes this and how to fix
- `AnotherError: Message`: Explanation and solution

### Performance Tips
- Optimization suggestions
- Best practices for large datasets
- Memory usage considerations

## Dependencies
List all external dependencies and their purposes:
- `package_name`: What it's used for
- `another_package`: Its role in the system

## Testing
How to test the functionality:
```python
# CODE_EXAMPLE_START
# Example test cases
import pytest
from this_package import MainClass

def test_basic_functionality():
    instance = MainClass()
    result = instance.process_data(test_data)
    assert result is not None
# CODE_EXAMPLE_STOP
```

## Integration Notes
How this subpackage integrates with other parts of the system:
- What it expects from upstream components
- What it provides to downstream components
- Any shared resources or state

## Changelog/Version Notes
Any important version information or recent changes.
```

## SPECIFIC INSTRUCTIONS:

### For RAG System Optimization:
- Use **descriptive section headers** that clearly indicate content
- Include **multiple code examples** for different scenarios
- Provide **context-rich descriptions** that explain not just what, but why
- Add **keyword-rich content** that covers variations of how users might ask questions
- Include **error scenarios** with solutions for troubleshooting queries

### Content Guidelines:
- **Be Comprehensive**: Cover all major functionality
- **Be Specific**: Include actual parameter names, types, and examples
- **Be Practical**: Focus on real-world usage patterns
- **Be Searchable**: Use terms a user might search for
- **Be Contextual**: Explain relationships between components

## CODE EXAMPLE FORMATTING:

**CRITICAL**: All code examples must be wrapped with parsing markers:
- Start each code block with `# CODE_EXAMPLE_START`
- End each code block with `# CODE_EXAMPLE_STOP`
- These markers enable automated validation and testing of code examples

Example format:
```python
# CODE_EXAMPLE_START
# Your working code example here
from module import Class
instance = Class()
result = instance.method()
# CODE_EXAMPLE_STOP
```

### Code Examples:
- Provide **working code** that can be copied and used
- **ALL code examples must be wrapped with `# CODE_EXAMPLE_START` and `# CODE_EXAMPLE_STOP`**
- Include **imports** and **setup** steps
- Show **both simple and complex** usage patterns
- Add **comments** explaining non-obvious steps
- Include **error handling** where relevant
- Ensure code examples are **syntactically correct and executable**

## EXECUTION STEPS:

1. **Analyze**: Read through all Python files in the directory
2. **Categorize**: Group related functionality
3. **Document**: Create comprehensive descriptions
4. **Exemplify**: Write practical code examples
5. **Troubleshoot**: Anticipate common issues and solutions
6. **Optimize**: Ensure content is RAG-friendly with rich context

Create a README.md that serves as the definitive guide for this subpackage, enabling both human developers and AI systems to understand and work with the code effectively.