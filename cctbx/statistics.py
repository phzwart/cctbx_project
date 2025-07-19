from __future__ import absolute_import, division, print_function

from typing import Dict, Optional, Any, Union, List
import cctbx.eltbx.xray_scattering
from cctbx import eltbx
from cctbx.array_family import flex
from libtbx.utils import plural_s
import math
from cctbx import xray, crystal

import boost_adaptbx.boost.python as bp
from six.moves import range
ext = bp.import_ext("cctbx_statistics_ext")
from cctbx_statistics_ext import *

mean_number_of_atoms_per_amino_acid: Dict[str, int] = {'C': 5, 'N': 3, 'O': 1}

class empty: 
    """Empty class used for storing plot information."""
    pass

class wilson_plot(object):
    """
    Wilson plot analysis for crystallographic data.
    
    Performs Wilson plot analysis to determine scale factors and B-factors
    from observed structure factor amplitudes.
    """

    def __init__(self, f_obs: Any, asu_contents: Dict[str, int], 
                 scattering_table: str = "wk1995", e_statistics: bool = False) -> None:
        """
        Initialize Wilson plot analysis.
        
        Args:
            f_obs: Observed structure factor amplitudes
            asu_contents: Dictionary mapping chemical types to number of atoms
            scattering_table: Scattering factor table to use. Defaults to "wk1995".
            e_statistics: Whether to compute E-statistics. Defaults to False.
        """
        assert scattering_table in [
          "n_gaussian", "it1992", "wk1995", "electron", "neutron"]
        assert f_obs.is_real_array()
        self.info = f_obs.info()
        f_obs_selected = f_obs.select(f_obs.data() > 0)
        f_obs_selected.use_binning_of(f_obs)
        # compute <fobs^2> in resolution shells
        self.mean_fobs_sq = f_obs_selected.mean_sq(
          use_binning=True,
          use_multiplicities=True).data[1:-1]
        n_none = self.mean_fobs_sq.count(None)
        if (n_none > 0):
          error_message = "wilson_plot error: %d empty bin%s:" % plural_s(n_none)
          if (self.info is not None):
            error_message += "\n  Info: " + str(self.info)
          error_message += "\n  Number of bins: %d" % len(self.mean_fobs_sq)
          error_message += "\n  Number of f_obs > 0: %d" % (
            f_obs_selected.indices().size())
          error_message += "\n  Number of f_obs <= 0: %d" % (
            f_obs.indices().size() - f_obs_selected.indices().size())
          raise RuntimeError(error_message)
        self.mean_fobs_sq = flex.double(self.mean_fobs_sq)
        # compute <s^2> = <(sin(theta)/lambda)^2> in resolution shells
        stol_sq = f_obs_selected.sin_theta_over_lambda_sq()
        stol_sq.use_binner_of(f_obs_selected)
        self.mean_stol_sq = flex.double(stol_sq.mean(
          use_binning=True,
          use_multiplicities=True).data[1:-1])
        #
        scatterers = flex.xray_scatterer()
        for chemical_type in asu_contents.keys():
          sc = xray.scatterer(
           scattering_type = chemical_type,
           site            = (0, 0, 0),
           u               = 0)
          scatterers.append(sc)
        cs = crystal.symmetry((1, 1, 1, 90, 90, 90), "P 1")
        sp = crystal.special_position_settings(cs)
        xrs = xray.structure(sp, scatterers)
        xrs.scattering_type_registry(table = scattering_table)
        scr = xrs.scattering_type_registry()
        self.expected_f_sq = flex.double()
        for stol_sq in self.mean_stol_sq:
          sum_fj_sq = 0
          for chemical_type, n_atoms in asu_contents.items():
            f0 = scr.gaussian(chemical_type).at_stol_sq(stol_sq)
            sum_fj_sq += f0 * f0 * n_atoms
          self.expected_f_sq.append(sum_fj_sq)
        self.expected_f_sq *= f_obs_selected.space_group().order_z() \
                            * f_obs_selected.space_group().n_ltr()
#
# Valuable example of an alternative was to calculate self.expected_f_sq
#
#    # cache scattering factor info
#    gaussians = {}
#    for chemical_type in asu_contents.keys():
#      gaussians[chemical_type] = eltbx.xray_scattering.wk1995(
#        chemical_type).fetch()
#    # compute expected f_calc^2 in resolution shells
#    self.expected_f_sq = flex.double()
#    for stol_sq in self.mean_stol_sq:
#      sum_fj_sq = 0
#      for chemical_type, n_atoms in asu_contents.items():
#        f0 = gaussians[chemical_type].at_stol_sq(stol_sq)
#        sum_fj_sq += f0 * f0 * n_atoms
#      self.expected_f_sq.append(sum_fj_sq)
#    self.expected_f_sq *= f_obs_selected.space_group().order_z() \
#                        * f_obs_selected.space_group().n_ltr()
#
        # fit to straight line
        self.x = self.mean_stol_sq
        self.y = flex.log(self.mean_fobs_sq / self.expected_f_sq)
        fit = flex.linear_regression(self.x, self.y)
        assert fit.is_well_defined()
        self.fit_y_intercept = fit.y_intercept()
        self.fit_slope = fit.slope()
        self.wilson_intensity_scale_factor = math.exp(self.fit_y_intercept) # intensity scale factor
        self.wilson_k = math.sqrt(self.wilson_intensity_scale_factor) # conversion to amplitude scale factor
        self.wilson_b = -self.fit_slope / 2
        self.fit_correlation = flex.linear_correlation(self.x,self.y).coefficient()

        if e_statistics:
          normalised = f_obs_selected.normalised_amplitudes(asu_contents, self)
          self.normalised_f_obs = normalised.array()
          self.mean_e_sq_minus_1 = normalised.mean_e_sq_minus_1()
          self.percent_e_sq_gt_2 = normalised.percent_e_sq_gt_2()

    def xy_plot_info(self) -> empty:
        """
        Get information for plotting the Wilson plot.
        
        Returns:
            empty: Object containing plot information including title, x/y data,
                   fit parameters, and legend information.
        """
        r = empty()
        r.title = "Wilson Plot"
        if (self.info != 0):
          r.title += ": " + str(self.info)
        r.x = self.x
        r.y = self.y
        r.xLegend = "(sin(theta)/lambda)^2"
        r.yLegend = "ln(<Fobs^2>/<Fcalc^2>)"
        r.fit_y_intercept = self.fit_y_intercept
        r.fit_slope = self.fit_slope
        r.fit_correlation = self.fit_correlation
        r.overlayLegend = ("k=%f, b=%f, corr=%f" % (
          self.wilson_k, self.wilson_b, self.fit_correlation))
        return r

class cumulative_intensity_distribution(object):
    """
    Cumulative intensity distribution analysis.
    
    As described by Howells, Phillips and Rogers, Acta Cryst. (1950). 3, 210
    """

    def __init__(self, f_obs: Optional[Any] = None, f_obs_sq: Optional[Any] = None) -> None:
        """
        Initialize cumulative intensity distribution analysis.
        
        Args:
            f_obs: Observed structure factor amplitudes (mutually exclusive with f_obs_sq)
            f_obs_sq: Observed structure factor intensities (mutually exclusive with f_obs)
        """
        assert [f_obs, f_obs_sq].count(None) == 1
        if f_obs is not None:
          assert f_obs.binner() is not None
          self.info = f_obs.info()
          f_obs_sq = f_obs.f_as_f_sq()
          f_obs_sq.use_binner_of(f_obs)
        else:
          assert f_obs_sq.binner() is not None
          self.info = f_obs_sq.info()
        mean_f_obs_sq = f_obs_sq.mean(use_binning=True)
        mean_data = flex.double(mean_f_obs_sq.data[1:f_obs_sq.binner().n_bins_used()+1])
        bin_d_max = flex.double([mean_f_obs_sq.binner.bin_d_range(i)[1]
                       for i in range(1,f_obs_sq.binner().n_bins_used()+1)])
        result = cumulative_intensity_core(f_obs_sq.data(),
                                        f_obs_sq.d_spacings().data(),
                                        mean_data,
                                        bin_d_max,
                                        f_obs_sq.indices())
        self.x = result.x()
        self.y = result.y()

    def xy_plot_info(self) -> empty:
        """
        Get information for plotting the cumulative intensity distribution.
        
        Returns:
            empty: Object containing plot information including title, x/y data,
                   and axis labels.
        """
        r = empty()
        r.title = "Cumulative Intensity Distribution"
        if (self.info != 0):
          r.title += ": " + str(self.info)
        r.x = self.x
        r.y = self.y
        r.xLegend = "z"
        r.yLegend = "N(z)"
        return r

class sys_absent_intensity_distribution(object):
    """
    Systematic absences intensity distribution analysis.
    
    I/sigma(I) vs I analysis for systematic absences.
    """

    def __init__(self, f_obs: Any) -> None:
        """
        Initialize systematic absences intensity distribution analysis.
        
        Args:
            f_obs: Observed structure factor amplitudes
        """
        self.info = f_obs.info()
        sys_absences = f_obs.select_sys_absent()
        if sys_absences.size() == 0:
          self.x = None
          self.y = None
          self.indices = None
        else:
          assert sys_absences.sigmas() is not None
          intensities = sys_absences.as_intensity_array()
          self.x = (intensities/sys_absences.sigmas()).data()
          self.y = intensities.data()
          self.indices = intensities.indices()

    def xy_plot_info(self) -> empty:
        """
        Get information for plotting the systematic absences intensity distribution.
        
        Returns:
            empty: Object containing plot information including title, x/y data,
                   indices, and axis labels.
        """
        r = empty()
        r.title = "Systematic Absences Intensity Distribution"
        if (self.info != 0):
          r.title += ": " + str(self.info)
        r.x = self.x
        r.y = self.y
        r.indices = self.indices
        r.xLegend = "I/sigma(I)"
        r.yLegend = "Intensity"
        return r
