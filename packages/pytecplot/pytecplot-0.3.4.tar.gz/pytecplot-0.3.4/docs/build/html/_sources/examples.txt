Examples
========

..  contents::
    :local:
    :depth: 1

.. _hello_world:

Hello World
-----------

A simple "Hello, World!" example that does the following:

    1. enables extremely verbose logging
    2. starts the |Tecplot 360 EX| engine
    3. add text to the active frame
    4. exports the frame to an image file
    5. releases the |Tecplot License|

.. figure:: /_static/images/hello_world.png
    :width: 300px
    :figwidth: 300px

.. literalinclude:: ../../examples/00_hello_world.py

Loading Layouts
---------------

Layouts can be loaded with the `tecplot.load_layout()` method. This will accept both ``lay`` and ``lpk`` (packaged) files. The exported image interprets the image type by the extension you give it. See `tecplot.export.save_png()` for more details.

.. figure:: /_static/images/jet_surface.png
    :width: 300px
    :figwidth: 300px

.. literalinclude:: ../../examples/01_load_layout_save_image.py

Exception Handling
------------------

It is the policy of the |PyTecplot| Python module to raise exceptions on any failure. It is the user's job to catch them or otherwise prevent them by ensuring the |Tecplot Engine| is properly setup to the task you ask of it. Aside from exceptions raised by the underlying Python core libraries, |PyTecplot| may raise a subclass of `TecplotError`, the most common being `TecplotRuntimeError`.

.. figure:: /_static/images/spaceship.png
    :width: 300px
    :figwidth: 300px

.. literalinclude:: ../../examples/02_exception_handling.py

Extracting Slices
------------------

This script produces two images: a 3D view of the wing and a simplified pressure coefficient plot half-way down the wing:

.. figure:: /_static/images/wing.png
    :width: 300px
    :figwidth: 300px
.. figure:: /_static/images/wing_pressure_coefficient.png
    :width: 300px
    :figwidth: 300px

.. literalinclude:: ../../examples/03_slices_along_wing.py

Numpy Integration
-----------------

.. note:: Numpy, SciPy Required

    This example requires both `numpy <http://www.numpy.org>`_ and `scipy <http://www.numpy.org/>`_ installed. SciPy, in turn, requires a conforming linear algebra system such as OpenBLAS, LAPACK, ATLAS or MKL. It is recommended to use your operating system's package manager to do this. Windows users and/or users that do not have root access to their machines might consider using `Anaconda <https://www.continuum.io/>`_ to setup a virtual environment where they can install python, numpy, scipy and all of its dependencies.

The spherical harmonic ``(n,m) = (5,4)`` is calculated at unit radius. The magnitude is then used to create a 3D shape. The plot-style is modified and the following image is exported and the layout is saved in "packaged format." The methods used in this example should be considered very low-level and in a "pre-alpha"/early stage in development:

.. figure:: /_static/images/spherical_harmonic_4_5.png
    :width: 300px
    :figwidth: 300px

.. literalinclude:: ../../examples/04_spherical_harmonic.py

Execute Equation
----------------

    This example illustrates altering data through equations in one or more zones. For complete information on the |Tecplot Engine| data alter syntax, see Chapter 21, *Data Operations*, in the Tecplot 360 User's Manual.

.. literalinclude:: ../../examples/07_execute_equation.py


Line Plots
----------

    This example shows how to set the style for a plot of three lines. The
    y-axis label and legend labels are changed and the axes are adjusted to
    fit the data.

.. figure:: /_static/images/linemap.png
    :width: 300px
    :figwidth: 300px

.. literalinclude:: ../../examples/11_linemaps.py
