from __future__ import absolute_import, division, print_function
from typing import Any, Optional, List, Dict, Union, Tuple

import operator
from cctbx import crystal
from cctbx import sgtbx
from cctbx.array_family import flex
from scitbx import matrix
from scitbx.python_utils import dicts
from libtbx.utils import user_plus_sys_time
from libtbx import adopt_init_args
import sys, math

import boost_adaptbx.boost.python as bp
from six.moves import range
from six.moves import zip
ext = bp.import_ext("cctbx_emma_ext")

def sgtbx_rt_mx_as_matrix_rt(s: Any) -> Any:
    """
    Convert sgtbx rt_mx to matrix.rt.
    
    Args:
        s: sgtbx rt_mx object
        
    Returns:
        Any: matrix.rt object
    """
    return matrix.rt((s.r().as_double(), s.t().as_double()))

class position(object):
    """Position class for storing atomic positions."""

    def __init__(self, label: str, site: Any) -> None:
        """
        Initialize position object.
        
        Args:
            label: Label for the position
            site: Site coordinates
        """
        adopt_init_args(self, locals())

    def __repr__(self) -> str:
        """
        String representation of position.
        
        Returns:
            str: Formatted position string
        """
        return "%-4s %7.4f %7.4f %7.4f" % ((self.label,) + tuple(self.site))

class model(crystal.special_position_settings):
    """Model class for crystal structure models."""

    def __init__(self, special_position_settings: Any, positions: Optional[List[Any]] = None) -> None:
        """
        Initialize model object.
        
        Args:
            special_position_settings: Crystal special position settings
            positions: List of positions. Defaults to None.
        """
        crystal.special_position_settings._copy_constructor(
          self, special_position_settings)
        self.reset_cb_op()
        self._positions = []
        if (positions is not None):
          self.add_positions(positions)

    def cb_op(self) -> Any:
        """
        Get change of basis operator.
        
        Returns:
            Any: Change of basis operator
        """
        return self._cb_op

    def reset_cb_op(self) -> Any:
        """
        Reset change of basis operator.
        
        Returns:
            Any: Self reference
        """
        self._cb_op = sgtbx.change_of_basis_op()
        return self

    def positions(self) -> List[Any]:
        """
        Get list of positions.
        
        Returns:
            List[Any]: List of position objects
        """
        return self._positions

    def __len__(self) -> int:
        """
        Get number of positions.
        
        Returns:
            int: Number of positions
        """
        return len(self._positions)

    def size(self) -> int:
        """
        Get number of positions.
        
        Returns:
            int: Number of positions
        """
        return len(self._positions)

    def __getitem__(self, key: int) -> Any:
        """
        Get position by index.
        
        Args:
            key: Position index
            
        Returns:
            Any: Position object
        """
        return self._positions[key]

    def add_position(self, pos: Any) -> None:
        """
        Add a position to the model.
        
        Args:
            pos: Position object to add
        """
        self._positions.append(position(
          pos.label,
          self.site_symmetry(pos.site).exact_site()))

    def add_positions(self, positions: List[Any]) -> None:
        """
        Add multiple positions to the model.
        
        Args:
            positions: List of position objects to add
        """
        for pos in positions:
          self.add_position(pos)

    def change_basis(self, cb_op: Any) -> Any:
        """
        Change basis of the model.
        
        Args:
            cb_op: Change of basis operator
            
        Returns:
            Any: New model with changed basis
        """
        positions = []
        for pos in self._positions:
          positions.append(position(pos.label, cb_op(pos.site)))
        result = model(
          crystal.special_position_settings.change_basis(self, cb_op),
          positions)
        result._cb_op = cb_op.new_denominators(self.cb_op()) * self.cb_op()
        return result

    def transform_to_reference_setting(self) -> Any:
        """
        Transform model to reference setting.
        
        Returns:
            Any: Model in reference setting
        """
        cb_op = self.space_group_info().type().cb_op()
        result = self.change_basis(cb_op)
        assert result.space_group_info().is_reference_setting()
        return result

    def change_hand(self) -> Any:
        """
        Change hand of the model.
        
        Returns:
            Any: Model with changed hand
        """
        ch_op = self.space_group_info().type().change_of_hand_op()
        return self.change_basis(ch_op)

    def expand_to_p1(self) -> Any:
        """
        Expand model to P1 symmetry.
        
        Returns:
            Any: Expanded model in P1
        """
        new_model = model(
          crystal.special_position_settings(
            crystal.symmetry.cell_equivalent_p1(self)))
        for pos in self._positions:
          site_symmetry = self.site_symmetry(pos.site)
          equiv_sites = sgtbx.sym_equiv_sites(site_symmetry)
          i = 0
          for site in equiv_sites.coordinates():
            i += 1
            new_model.add_position(position(
              label=pos.label+"_%03d"%i,
              site=site))
        return new_model

    def show(self, title: str, f: Optional[Any] = None) -> None:
        """
        Display model information.
        
        Args:
            title: Title for display
            f: Output file. Defaults to None (stdout).
        """
        if (f is None): f = sys.stdout
        print(title, file=f)
        crystal.special_position_settings.show_summary(self, f)
        if (not self.cb_op().is_identity_op()):
          print("Change of basis:", file=f)
          print("  c:", self.cb_op().c(), file=f)
          print("  c_inv:", self.cb_op().c_inv(), file=f)
        for pos in self.positions(): print(pos, file=f)
        print(file=f)

    def as_xray_structure(self, scatterer: Optional[Any] = None) -> Any:
        """
        Convert model to xray structure.
        
        Args:
            scatterer: Scatterer type. Defaults to None.
            
        Returns:
            Any: Xray structure object
        """
        from cctbx import xray
        if (scatterer is None):
          scatterer = xray.scatterer(scattering_type="const")
        result = xray.structure(special_position_settings=self)
        for position in self.positions():
          result.add_scatterer(scatterer.customized_copy(
            label=position.label,
            site=position.site))
        return result

    def combine_with_other(self, other_model: Any, tolerance: float = 1.5,
      models_are_diffraction_index_equivalent: bool = True,
      break_if_match_with_no_singles: bool = True, f: Any = sys.stdout,
      improved_only: bool = True, new_model_number: int = 0) -> List[Any]:
        """
        Combine this model with another model.
        
        Args:
            other_model: Other model to combine with
            tolerance: Matching tolerance. Defaults to 1.5.
            models_are_diffraction_index_equivalent: Whether models are diffraction index equivalent. Defaults to True.
            break_if_match_with_no_singles: Whether to break if match has no singles. Defaults to True.
            f: Output file. Defaults to sys.stdout.
            improved_only: Whether to include only improved matches. Defaults to True.
            new_model_number: Starting model number. Defaults to 0.
            
        Returns:
            List[Any]: List of combined models
        """
        # 2013-01-25 tt superpose other on this one and return composite
        match_list=self.best_superpositions_on_other(other_model,
          tolerance=tolerance,models_are_diffraction_index_equivalent=
               models_are_diffraction_index_equivalent,
               break_if_match_with_no_singles=break_if_match_with_no_singles,
               f=f,specifically_test_inverse=True)

        new_model_list=[]
        for x in other_model.component_model_numbers:
          if x in self.component_model_numbers:
            return new_model_list # cannot combine with something already used
        for match in match_list:
          if match is None: continue
          if improved_only and (len(match.singles2) ==0):
             continue

          test_new_model= model(special_position_settings=self)
          new_model= model(special_position_settings=self)
          new_model.model_number=new_model_number
          new_model.component_model_numbers=[new_model_number]+ \
             self.component_model_numbers+other_model.component_model_numbers
          new_model_number+=1
          for pos in self.positions():
            new_model.add_position(position(label=pos.label, site=(pos.site)))
          i=new_model.size()-1
          for s in match.singles2:
            site=match.ref_model2[s].site
            new_model.add_position(position(
               label="ATOM_%03d"%i,
               site=(match.rt*site).elems))
            test_new_model.add_position(position(
               label="ATOM_%03d"%i,
               site=(match.rt*site).elems))
          new_model_list.append(new_model)
        return new_model_list


    def best_superpositions_on_other(self, other_model: Any, tolerance: float = 1.5,
      models_are_diffraction_index_equivalent: bool = True,
      break_if_match_with_no_singles: bool = True, f: Any = sys.stdout,
      specifically_test_inverse: bool = True) -> List[Any]:
        """
        Find best superpositions on other model.
        
        Args:
            other_model: Other model to match against
            tolerance: Matching tolerance. Defaults to 1.5.
            models_are_diffraction_index_equivalent: Whether models are diffraction index equivalent. Defaults to True.
            break_if_match_with_no_singles: Whether to break if match has no singles. Defaults to True.
            f: Output file. Defaults to sys.stdout.
            specifically_test_inverse: Whether to test inverse. Defaults to True.
            
        Returns:
            List[Any]: List of best matches
        """
        # 2013-01-25 tt.Find best match to other_model and return it
        # 2013-01-19 return list of best ones (can be alternatives)

        # if you want the superposed model use:
        #  superposed_model2=match.get_transformed_model2(
        #     template=other_model)

        if not hasattr(self,'match_dict'):
          self.match_dict={}
          match_list=None
        else:
          match_list=self.match_dict.get(other_model,None)

        if match_list is None:   # need to get it
          from cctbx import euclidean_model_matching as emma
          test_list=[other_model]
          match_list=[]
          if specifically_test_inverse:
            from copy import deepcopy
            inv_other_model=other_model.change_hand()
            inv_other_model._cb_op=deepcopy(other_model._cb_op)
            test_list.append(inv_other_model)
          for test_model in test_list:
            matches = emma.model_matches(
              model1 = self,
              model2 = test_model,
              tolerance = tolerance,
              models_are_diffraction_index_equivalent = \
                  models_are_diffraction_index_equivalent,
              break_if_match_with_no_singles=break_if_match_with_no_singles,
              )
