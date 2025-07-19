from __future__ import absolute_import, division, print_function
from cctbx.array_family import flex # for tuple mappings
from typing import List, Tuple, Union, Any, Optional

import boost_adaptbx.boost.python as bp
from six.moves import range
ext = bp.import_ext("cctbx_adptbx_ext")
from cctbx_adptbx_ext import *

import scitbx.math
import random
import math

u_as_b_factor = u_as_b(1)
b_as_u_factor = b_as_u(1)

mtps = -2 * math.pi**2
mtpss = mtps**2

def random_rotate_ellipsoid(u_cart: List[float], r_min: float = 0, r_max: float = 360) -> List[float]:
    """
    Randomly rotate an ADP ellipsoid by applying random Euler angles.
    
    Args:
        u_cart (List[float]): U_cart parameters [U11, U22, U33, U12, U13, U23]
        r_min (float, optional): Minimum rotation angle in degrees. Defaults to 0.
        r_max (float, optional): Maximum rotation angle in degrees. Defaults to 360.
        
    Returns:
        List[float]: Rotated U_cart parameters
    """
    c = scitbx.math.euler_angles_as_matrix(
        [random.uniform(r_min,r_max) for i in range(3)], deg=True).elems
    return c_u_c_transpose(c, u_cart)

def random_u_cart(u_scale: float = 1, u_min: float = 0) -> List[float]:
    """
    Generate random U_cart parameters with specified scale and minimum values.
    
    Args:
        u_scale (float, optional): Scale factor for random values. Defaults to 1.
        u_min (float, optional): Minimum value for diagonal elements. Defaults to 0.
        
    Returns:
        List[float]: Random U_cart parameters [U11, U22, U33, 0, 0, 0]
    """
    return random_rotate_ellipsoid(u_cart=[random.random()*u_scale+u_min
        for i in range(3)] + [0,0,0])

def debye_waller_factor_u_star_gradients(h: Any, u_star: List[float]) -> flex.double:
    """
    Calculate gradients of Debye-Waller factor with respect to U_star parameters.
    
    Args:
        h (Any): Miller index or reflection vector
        u_star (List[float]): U_star parameters [U*11, U*22, U*33, U*12, U*13, U*23]
        
    Returns:
        flex.double: Gradient coefficients for Debye-Waller factor
    """
    return flex.double(debye_waller_factor_u_star_gradient_coefficients(h=h)) \
         * (mtps * debye_waller_factor_u_star(h, u_star))

def debye_waller_factor_u_star_curvatures(h: Any, u_star: List[float]) -> flex.double:
    """
    Calculate curvatures of Debye-Waller factor with respect to U_star parameters.
    
    Args:
        h (Any): Miller index or reflection vector
        u_star (List[float]): U_star parameters [U*11, U*22, U*33, U*12, U*13, U*23]
        
    Returns:
        flex.double: Curvature coefficients for Debye-Waller factor
    """
    return debye_waller_factor_u_star_curvature_coefficients(h=h) \
         * (mtpss * debye_waller_factor_u_star(h, u_star))

def random_traceless_symmetry_constrained_b_cart(crystal_symmetry: Any, u_scale: float = 1,
      u_min: float = 0.1) -> List[float]:
    """
    Generate random traceless symmetry-constrained B_cart parameters.
    
    This function creates random ADP parameters that respect the crystal symmetry
    and have zero trace (traceless), which is useful for certain types of
    crystallographic refinement.
    
    Args:
        crystal_symmetry (Any): Crystal symmetry object containing space group and unit cell
        u_scale (float, optional): Scale factor for random U values. Defaults to 1.
        u_min (float, optional): Minimum value for U parameters. Defaults to 0.1.
        
    Returns:
        List[float]: Traceless symmetry-constrained B_cart parameters [B11, B22, B33, B12, B13, B23]
    """
    from cctbx import sgtbx
    symbol = crystal_symmetry.space_group().type().lookup_symbol()
    point_group = sgtbx.space_group_info(
        symbol=symbol).group().build_derived_point_group()
    adp_constraints = sgtbx.tensor_rank_2_constraints(
        space_group=point_group,
        reciprocal_space=True)
    u_star = u_cart_as_u_star(crystal_symmetry.unit_cell(),
        random_u_cart(u_scale=u_scale,u_min=u_min))
    u_indep = adp_constraints.independent_params(all_params=u_star)
    u_star = adp_constraints.all_params(independent_params=u_indep)
    b_cart = u_as_b(u_star_as_u_cart(crystal_symmetry.unit_cell(), u_star))
    tr = (b_cart[0]+b_cart[1]+b_cart[2])/3
    b_cart = [b_cart[0]-tr, b_cart[1]-tr, b_cart[2]-tr,
             b_cart[3],b_cart[4],b_cart[5]]
    return b_cart

def intersection(u_1: Union[float, List[float]], u_2: Union[float, List[float]], 
                site_1: Tuple[float, float, float], site_2: Tuple[float, float, float], 
                unit_cell: Any) -> float:
    """
    Calculate the intersection of two scatterers, given coordinates and atomic
    displacements. If the scatterers do not actually intersect the result will
    be negative.
    
    Args:
        u_1 (Union[float, List[float]]): ADP parameters for first scatterer (isotropic float or anisotropic list)
        u_2 (Union[float, List[float]]): ADP parameters for second scatterer (isotropic float or anisotropic list)
        site_1 (Tuple[float, float, float]): Fractional coordinates of first scatterer
        site_2 (Tuple[float, float, float]): Fractional coordinates of second scatterer
        unit_cell (Any): Unit cell object for coordinate transformations
        
    Returns:
        float: Intersection value (negative if no intersection)
    """
    from scitbx.matrix import col
    if (site_1 == site_2):
        return sys.maxsize
    if isinstance(u_1, float):
        u_1 = u_iso_as_u_star(unit_cell, u_1)
    if isinstance(u_2, float):
        u_2 = u_iso_as_u_star(unit_cell, u_2)
    site_cart_1 = col(unit_cell.orthogonalize(site_frac=site_1))
    site_cart_2 = col(unit_cell.orthogonalize(site_frac=site_2))
    dxyz = abs(site_cart_1 - site_cart_2)
    proj_sum = projection_sum(
        ustar1=u_1,
        ustar2=u_2,
        site1=site_1,
        site2=site_2,
        unit_cell=unit_cell).delta_z()
    return proj_sum - dxyz
