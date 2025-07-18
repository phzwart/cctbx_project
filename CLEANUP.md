# Code Refactoring Prompt for Cursor

You are tasked with adding type hints and docstrings to Python code while maintaining **STRICT STRUCTURAL INTEGRITY**. Follow these requirements precisely:

## CRITICAL REQUIREMENTS - MUST NOT VIOLATE:

### 1. Function Signature Preservation
- **NEVER** change the number of input arguments for any function or method
- **NEVER** add, remove, or rename parameters
- **NEVER** change default values
- **NEVER** change parameter order
- Only ADD type hints to existing parameters

### 2. File Structure Preservation  
- **NEVER** change the total number of functions in the file
- **NEVER** add new functions
- **NEVER** remove existing functions
- **NEVER** merge or split functions

### 3. Verification Steps
For EACH function you modify:
1. Count the original number of parameters
2. After modification, verify the parameter count remains identical
3. If counts don't match, STOP and fix the issue

## WHAT TO ADD:

### Type Hints
- Add appropriate type hints to all function parameters
- Add return type annotations
- Use standard typing imports (List, Dict, Optional, Union, etc.)
- For complex types, use the most specific type possible
- Use `Any` only when the actual type cannot be determined

### Docstrings
- Add comprehensive docstrings in Google/NumPy style
- Include:
  - Brief description of what the function does
  - Args section with parameter descriptions and types
  - Returns section with return value description and type
  - Raises section if applicable
  - Examples section for complex functions

## FORMAT EXAMPLE:

```python
from typing import List, Dict, Optional, Union, Any

def example_function(param1: str, param2: int = 10, param3: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Brief description of what this function does.
    
    Args:
        param1 (str): Description of param1
        param2 (int, optional): Description of param2. Defaults to 10.
        param3 (Optional[List[str]], optional): Description of param3. Defaults to None.
    
    Returns:
        Dict[str, Any]: Description of what is returned
        
    Raises:
        ValueError: When invalid input is provided
    """
    # existing function body remains unchanged
    pass
```

## SAFETY CHECKS:

Before completing your work:
1. **Parameter Count Verification**: Confirm each function has the same number of parameters as before
2. **Function Count Verification**: Confirm the file has the same number of functions as before
3. **Import Addition**: Only add necessary typing imports at the top
4. **No Logic Changes**: Ensure no function logic has been modified

## IF YOU ENCOUNTER ISSUES:
- If you cannot determine the appropriate type for a parameter, use `Any`
- If the existing code structure seems problematic, ADD ONLY type hints and docstrings - do NOT fix other issues
- If a function is too complex to understand fully, provide basic type hints and a general docstring

Remember: Your job is ONLY to add type hints and docstrings. Everything else must remain exactly the same. 