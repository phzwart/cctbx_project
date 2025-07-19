from __future__ import absolute_import, division, print_function
from typing import Any, Optional, Union
import cctbx.array_family.flex # import dependency
from cctbx import uctbx # import dependency
import boost_adaptbx.boost.python as bp
ext = bp.import_ext("cctbx_orientation_ext")
from cctbx_orientation_ext import *

class basis_type:
    """Basis type constants for crystal orientation."""
    direct = False
    reciprocal = True

@bp.inject_into(ext.crystal_orientation)
class _():

    def __getattr__(self, tag: str) -> Any:
        """
        Get crystal orientation attributes.
        
        Args:
            tag: Attribute name to retrieve
            
        Returns:
            Any: Requested attribute value or None if not found
        """
        from scitbx.matrix import col
        if tag in ['astar','bstar','cstar']:
          F = self.reciprocal_matrix()
          if tag == 'astar': return col((F[0],F[3],F[6]))
          if tag == 'bstar': return col((F[1],F[4],F[7]))
          if tag == 'cstar': return col((F[2],F[5],F[8]))
        if tag in 'abc':
          direct = self.direct_matrix()
          if tag=='a':
            return col((direct[0],direct[1],direct[2]))
          elif tag=='b':
            return col((direct[3],direct[4],direct[5]))
          elif tag=='c':
            return col((direct[6],direct[7],direct[8]))
        mm = self.unit_cell().metrical_matrix()
        if tag=='A':
          return mm[0]
        elif tag=='B':
          return mm[1]
        elif tag=='C':
          return mm[2]
        elif tag=='D':
          return mm[5]
        elif tag=='E':
          return mm[4]
        elif tag=='F':
          return mm[3]
        mm = self.unit_cell().reciprocal().metrical_matrix()
        if tag=='As':
          return mm[0]
        elif tag=='Bs':
          return mm[1]
        elif tag=='Cs':
          return mm[2]
        elif tag=='Ds':
          return mm[5]
        elif tag=='Es':
          return mm[4]
        elif tag=='Fs':
          return mm[3]
        else:
          return

    def make_positive(self) -> Any:
        """
        Ensure the crystal orientation has positive volume.
        
        Returns:
            Any: Crystal orientation with positive volume
        """
        from scitbx import matrix
        signed_volume = matrix.sqr(self.direct_matrix()).determinant()
        if signed_volume<0:
          return self.change_basis((-1.,0.,0.,0.,-1.,0.,0.,0.,-1.))
        return self

    def reduced_cell(self) -> Any:
        """
        Transform the orientation matrix to the reduced cell.
        
        Returns:
            Any: Crystal orientation in reduced cell
        """
        #convenience function to transform the orientation matrix to the reduced cell
        from cctbx.uctbx import fast_minimum_reduction
        from scitbx import matrix
        uc = self.unit_cell()
        R = fast_minimum_reduction(uc)
        rinverse = matrix.sqr( R.r_inv() )
        return self.change_basis(rinverse.transpose().inverse().elems)

    def __copy__(self) -> Any:
        """
        Create a copy of the crystal orientation.
        
        Returns:
            Any: Copy of the crystal orientation
        """
        return crystal_orientation(self.reciprocal_matrix(),basis_type.reciprocal)

    def __getinitargs__(self) -> tuple:
        """
        Get initialization arguments for pickling.
        
        Returns:
            tuple: Arguments needed to recreate the object
        """
        return (self.reciprocal_matrix(),basis_type.reciprocal)

    def __str__(self) -> str:
        """
        String representation of the crystal orientation.
        
        Returns:
            str: String representation
        """
        return "A-star:%10.6f%10.6f%10.6f%10.6f%10.6f%10.6f%10.6f%10.6f%10.6f\n" \
               "cell:"%self.reciprocal_matrix()+\
           str(self.unit_cell())+"%.0f"%self.unit_cell().volume()

    def __eq__(self, other: Any) -> bool:
        """
        Compare crystal orientations for equality.
        
        Args:
            other: Other crystal orientation to compare with
            
        Returns:
            bool: True if orientations are equal
        """
        S = self.reciprocal_matrix()
        O = other.reciprocal_matrix()
        return S[0]==O[0] and S[1]==O[1] and S[2]==O[2] \
           and S[3]==O[3] and S[4]==O[4] and S[5]==O[5] \
           and S[6]==O[6] and S[7]==O[7] and S[8]==O[8]

    # The "U" matrix such that A(reciprocal) = U * B, where B is orthogonalization.transpose()
    def crystal_rotation_matrix(self) -> Any:
        """
        Get the crystal rotation matrix U.
        
        Returns:
            Any: Crystal rotation matrix
        """
        from scitbx import matrix
        return matrix.sqr(self.reciprocal_matrix()) \
             * matrix.sqr(self.unit_cell().orthogonalization_matrix()).transpose()

    def get_U_as_sqr(self) -> Any:
        """
        Get the U matrix as a square matrix.
        
        Returns:
            Any: U matrix as square matrix
        """
        U = self.crystal_rotation_matrix()
        assert U.is_r3_rotation_matrix()
        return U

    def set_new_crystal_rotation_matrix(self, mat3: Any) -> Any:
        """
        Set a new crystal rotation matrix.
        
        Args:
            mat3: New rotation matrix
            
        Returns:
            Any: New crystal orientation
        """
        from scitbx import matrix
        return crystal_orientation( mat3 \
             * matrix.sqr(self.unit_cell().fractionalization_matrix()).transpose(),\
             basis_type.reciprocal)

    def show(self, legend: Optional[str] = None, basis: bool = basis_type.direct) -> None:
        """
        Display crystal orientation information.
        
        Args:
            legend: Optional legend text. Defaults to None.
            basis: Basis type (direct or reciprocal). Defaults to basis_type.direct.
        """
        from scitbx import matrix
        uc = self.unit_cell()
        U  = self.crystal_rotation_matrix()
        A  = self.direct_matrix()
        B = matrix.sqr(self.unit_cell().fractionalization_matrix()).transpose()
        if legend is not None: print ("%s:"%legend)
        print ("""    Unit cell:  %9.4f,%9.4f,%9.4f,%7.2f,%7.2f,%7.2f"""%(uc.parameters()))
        print ("""    U matrix:   %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f"""%(U.elems)
        )
        print ("""    B matrix:   %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f"""%(B.elems)
        )
        print ("""    A recipr:   %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f"""%(self.reciprocal_matrix())
        )
        print ("""    A direct:   %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f,
                    %9.4f,%9.4f,%9.4f"""%(A)
        )
