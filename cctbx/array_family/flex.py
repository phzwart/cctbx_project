from __future__ import absolute_import, division, print_function
import scitbx.array_family.flex

import boost_adaptbx.boost.python as bp
ext_ = bp.import_ext("cctbx_array_family_flex_ext")
from scitbx_array_family_flex_ext import *
from cctbx_array_family_flex_ext import *
ext = ext_
del ext_

scitbx.array_family.flex.export_to("cctbx.array_family.flex")

# Add docstrings to Boost.Python exposed functions
def _add_docstrings():
    """Add docstrings to functions exposed via Boost.Python."""
    
    # Add docstrings to hendrickson_lattman functions
    if hasattr(ext, 'hendrickson_lattman'):
        hendrickson_lattman = ext.hendrickson_lattman
        
        # Constructor docstrings
        if hasattr(hendrickson_lattman, '__init__'):
            hendrickson_lattman.__init__.__doc__ = """
            Initialize hendrickson_lattman array.
            
            Args:
                a (flex.double): A parameters
                b (flex.double): B parameters
                c (flex.double, optional): C parameters. Defaults to None.
                d (flex.double, optional): D parameters. Defaults to None.
            """
        
        # Method docstrings
        if hasattr(hendrickson_lattman, 'slice'):
            hendrickson_lattman.slice.__doc__ = """
            Extract a slice of parameters.
            
            Args:
                i_param (int): Parameter index (0-3)
                
            Returns:
                flex.double: Array of parameter values
            """
        
        if hasattr(hendrickson_lattman, 'conj'):
            hendrickson_lattman.conj.__doc__ = """
            Return complex conjugate.
            
            Returns:
                flex.hendrickson_lattman: Conjugate array
            """
        
        if hasattr(hendrickson_lattman, 'as_abcd'):
            hendrickson_lattman.as_abcd.__doc__ = """
            Extract A, B, C, D parameters as separate arrays.
            
            Returns:
                tuple: (a, b, c, d) arrays
            """
    
    # Add docstrings to miller_index functions
    if hasattr(ext, 'miller_index'):
        miller_index = ext.miller_index
        
        if hasattr(miller_index, 'as_vec3_double'):
            miller_index.as_vec3_double.__doc__ = """
            Convert to vec3_double array.
            
            Returns:
                flex.vec3_double: Array of 3D vectors
            """
        
        if hasattr(miller_index, 'fourier_transform_real_part_at_x'):
            miller_index.fourier_transform_real_part_at_x.__doc__ = """
            Calculate Fourier transform real part at given position.
            
            Args:
                fourier_coeffs (flex.complex_double): Fourier coefficients
                x (tuple): Position vector (x, y, z)
                
            Returns:
                float: Real part of Fourier transform
            """
        
        if hasattr(miller_index, 'first_index'):
            miller_index.first_index.__doc__ = """
            Find first occurrence of given miller index.
            
            Args:
                miller_index (tuple): Target miller index (h, k, l)
                
            Returns:
                Optional[int]: Index of first occurrence, or None if not found
            """
    
    # Add docstrings to xray_scatterer functions
    if hasattr(ext, 'xray_scatterer'):
        xray_scatterer = ext.xray_scatterer
        
        if hasattr(xray_scatterer, 'extract_labels'):
            xray_scatterer.extract_labels.__doc__ = """
            Extract scatterer labels.
            
            Returns:
                flex.std_string: Array of scatterer labels
            """
        
        if hasattr(xray_scatterer, 'extract_sites'):
            xray_scatterer.extract_sites.__doc__ = """
            Extract scatterer sites.
            
            Returns:
                flex.vec3_double: Array of scatterer positions
            """
        
        if hasattr(xray_scatterer, 'set_sites'):
            xray_scatterer.set_sites.__doc__ = """
            Set scatterer sites.
            
            Args:
                sites (flex.vec3_double): New scatterer positions
            """
        
        if hasattr(xray_scatterer, 'extract_occupancies'):
            xray_scatterer.extract_occupancies.__doc__ = """
            Extract scatterer occupancies.
            
            Returns:
                flex.double: Array of occupancies
            """
        
        if hasattr(xray_scatterer, 'set_occupancies'):
            xray_scatterer.set_occupancies.__doc__ = """
            Set scatterer occupancies.
            
            Args:
                occupancies (flex.double): New occupancy values
            """

# Apply docstrings
_add_docstrings()
