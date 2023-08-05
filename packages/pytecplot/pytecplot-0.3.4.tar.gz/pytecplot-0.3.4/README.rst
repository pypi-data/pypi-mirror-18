PyTecplot
=========

The pytecplot library is a high level API that connects your Python script
to the power of the |Tecplot 360 EX| visualization engine. It offers line
plotting, 2D and 3D surface plots in a variety of formats, and 3D volumetric
visualization. Familiarity with |Tecplot 360 EX| and the |Tecplot 360 EX|
macro language is helpful, but not required.

Documentation
-------------

The full documentation is at http://www.tecplot.com/docs/pytecplot

.. note::
    |PyTecplot| supports 64-bit Python versions 2.7 and 3.4+. |PyTecplot|
    does not support 32 bit Python. Please refer to INSTALL.rst for
    installation instructions and environment setup. For the best
    experience, developers are encouraged to use the **latest version of
    Python**.

Quick Start
-----------

Please refer to the documentation for detailed installation instructions and
environment setup. The short of it is something like this::

    pip install pytecplot

Linux and OSX users will have to set ``LD_LIBRARY_PATH`` or
``DYLD_LIBRARY_PATH`` to the directories containing the |Tecplot 360 EX|
dynamic libraries. For OSX, this will be something like::

    /Applications/Tecplot 360 EX/Tecplot 360 EX.app/Contents/MacOS

.. |Tecplot 360 EX| replace:: `Tecplot 360 EX <http://www.tecplot.com/products/tecplot-360/>`__
.. |PyTecplot| replace:: `PyTecplot <http://www.tecplot.com/docs/pytecplot>`__
