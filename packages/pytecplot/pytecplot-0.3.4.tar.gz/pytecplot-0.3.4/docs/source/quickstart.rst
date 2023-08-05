.. _quick start:

Quick Start
===========

This page gives you an introduction on how to get started with |PyTecplot|.
For installation and system requirements, see the `installation
instructions <Installation>`.

Please refer to the `Installation` file for installation instructions and
environment setup. The short of it is something like this::

    pip install pytecplot

Linux and OSX users will have to set ``LD_LIBRARY_PATH`` or
``DYLD_LIBRARY_PATH`` respectively to the directory containing the |Tecplot 360
EX| executable. For OSX, this will be something like::

    "/Applications/Tecplot 360 EX/Tecplot 360 EX.app/Contents/MacOS"

Hello World
-----------

Here is a simple |PyTecplot| script which creates a simple plot with some
text and export an image of that plot. Note that the |Tecplot License| is
acquired automatically on the first call into the |PyTecplot| API:

.. literalinclude:: ../../examples/00_hello_world.py

After running this script, you should have a PNG image like this:

.. figure:: /_static/images/hello_world.png
    :width: 300px
    :figwidth: 300px

Macro Integration
-----------------

All macro commands can be executed from an active |PyTecplot| session. This
means you may wrap all of your existing macro commands into a python script
and one-by-one move the commands into native Python code. The "Hello,
World!" example above could have been written like this::

    >>> import tecplot
    >>> tecplot.macro.execute_command(r'''
    ...   $!ATTACHTEXT
    ...     ANCHORPOS { X = 35 Y = 50 }
    ...     TEXTSHAPE { HEIGHT = 35 }
    ...     TEXT = 'Hello, World!'
    ...   $!EXPORTSETUP EXPORTFNAME = 'hello_world.png'
    ...   $!EXPORT
    ...     EXPORTREGION = CURRENTFRAME
    ... ''')

We could pull out just the image creation part into Python by writing this::

    >>> import tecplot
    >>> tecplot.macro.execute_command(r'''
    ...   $!ATTACHTEXT
    ...     ANCHORPOS { X = 35 Y = 50 }
    ...     TEXTSHAPE { HEIGHT = 35 }
    ...     TEXT = 'Hello, World!'
    ... ''')
    >>> tecplot.export.save_png('hello_world.png', 600)

For more information, see the `tecplot.macro` reference documentation.

.. _getting help:

Getting Help
------------

Examples can be found in the ``examples`` directory and the primary
documentation (in HTML format) can found under the ``docs`` directory::

    docs/builds/html/index.html

It is generated directly from the source code under ``pytecplot/tecplot``.
In addition, all imported objects and methods that are part of the public
API have doc strings which can be accessed with python's native ``help()``
function. Additionally, users are encouraged to contact support@tecplot.com
for any questions they may have.
