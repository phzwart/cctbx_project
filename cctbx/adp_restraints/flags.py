from __future__ import absolute_import, division, print_function
from libtbx import adopt_init_args
import sys
from typing import Optional, TextIO, Any

class flags(object):
  """
  Class to manage flags for ADP restraints.
  
  This class holds boolean flags that control which types of ADP restraints
  are active during refinement.
  """

  def __init__(self,
        adp_similarity: Optional[bool] = None,
        rigid_bond: Optional[bool] = None,
        isotropic_adp: Optional[bool] = None,
        default: bool = False) -> None:
    """
    Initialize flags for ADP restraints.
    
    Args:
        adp_similarity (Optional[bool]): Flag for ADP similarity restraints. 
            If None, uses default value.
        rigid_bond (Optional[bool]): Flag for rigid bond restraints. 
            If None, uses default value.
        isotropic_adp (Optional[bool]): Flag for isotropic ADP restraints. 
            If None, uses default value.
        default (bool): Default value for flags that are None. Defaults to False.
    """
    if (adp_similarity is None): adp_similarity = default
    if (rigid_bond is None): rigid_bond = default
    if (isotropic_adp is None): isotropic_adp = default
    adopt_init_args(self, locals())

  def show(self, f: Optional[TextIO] = None) -> None:
    """
    Display the current flag values.
    
    Args:
        f (Optional[TextIO]): Output file stream. If None, uses sys.stdout.
    """
    if (f is None): f = sys.stdout
    print("adp_restraints.manager.flags:", file=f)
    print("  adp_similarity:", self.adp_similarity, file=f)
    print("  rigid_bond:", self.rigid_bond, file=f)
    print("  isotropic_adp:", self.isotropic_adp, file=f)
