"""
=================================
I/O Utilities (:mod:`osiris.io`)
=================================

.. currentmodule:: osiris.io

This module contains I/O Utilities

State Files
-----------
.. toctree::
   :maxdepth: 2

.. automodule:: osiris.io.netcdf
   :members:

.. automodule:: osiris.io.state
   :members:

.. automodule:: osiris.io.cfg
   :members:
"""

from .state import OceanStateFile
from .cfg import ConfigFile
from .raw import RawFile