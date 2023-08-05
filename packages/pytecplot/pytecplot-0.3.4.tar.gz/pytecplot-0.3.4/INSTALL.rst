Installation
============

|PyTecplot| is supported on 64 bit Python versions 2.7 and 3.4+. |PyTecplot|
does not support 32 bit Python. Interacting with the |Tecplot Engine|
requires a valid |Tecplot 360 EX| installation and |Tecplot License|. Visit
http://www.tecplot.com for more information about purchasing |Tecplot 360 EX|.

It is recommended to use ``pip`` to install PyTecplot from Python's official
`PYPI servers <https://pypi.python.org/pypi/pytecplot>`_::

    pip install pytecplot

For those with a restricted internet connection, |PyTecplot| ships with
|Tecplot 360 EX| and can be found in the installation under the "pytecplot"
directory. You may run pip from within this directory to install pytecplot as
follows. Notice the use of "." to indicate the current working directory::

    cd "C:\Program Files\Tecplot\Tecplot 360 EX\pytecplot"
    pip install .

If you get a "permission denied" error, then administrative (root) privileges
may be required if you are attempting to install |PyTecplot| with a
system-installed version of Python so you may have to open your console as an
Administrator on Windows or run under "sudo" on Unix::

    sudo pip install pytecplot

Alternatively, you may wish to install |PyTecplot| into your user-space (see
the output of the commmand ``pip help`` for details)::

    pip install --user pytecplot

If you do not have pip installed and you are running Python version 2.7, you
may be able to install it with ``easy_install``::

    easy_install pip

Again, you will likely need Administrative privileges to run the above
command. If you still do not have `pip <https://pip.pypa.io>`_ installed,
this `installation guide
<http://docs.python-guide.org/en/latest/starting/installation/>`_ may help.

All required dependencies will be included though you may install all optional
modules that |PyTecplot| can make use of, such as Numpy and IPython, with the
"extras" option passed to ``pip`` like this::

    pip install pytecplot[extras]

Once installed, you will need to setup your environment so PyTecplot can
find the dynamic libraries associated with the SDK. In general, this will be
platform-specific.

Environment Setup
-----------------

For all platforms, the |Tecplot 360 EX| application must be run once to
establish a licensing method. This will be used when running any script
which uses the python ``tecplot`` module.

Windows
^^^^^^^

If |Tecplot 360 EX|'s bin directory is not already in the system's ``PATH``
list, you will have to add it and make sure it is before any other |Tecplot
360 EX| installation. With a standard installation of |Tecplot 360 EX|, the
path is usually something like::

    C:\Program Files\Tecplot\Tecplot 360 EX\bin

Linux
^^^^^

If |Tecplot 360 EX|'s bin and bin/sys directories are not already in the
system's dynamic library loader search path, you will need to set the following
environment variable::

    export LD_LIBRARY_PATH=/path/to/tecplot360/bin:/path/to/tecplot360/bin/sys

Mac OS X
^^^^^^^^

If |Tecplot 360 EX|'s bin directory is not already in the system's dynamic
library loader search path, you will need to set the following environment
variable::

    export DYLD_LIBRARY_PATH="/Applications/Tecplot.../Contents/MacOS"

With a standard installation of |Tecplot 360 EX|, the "Tecplot..." above is
usually something like::

    "Tecplot 360 EX {VERSION}/Tecplot 360 EX {VERSION}.app"

Troubleshooting
---------------

1. Verify that you have installed and can run |Tecplot 360 EX|.
2. Verify that you are running 64 bit Python version ``2.7`` or ``3.4+``.
3. Verify that you have run ``python -mpip install pytecplot`` with the
   correct python executable.
4. Installing into the Python's ``site-packages`` typically requires elevated
   privileges. Therefore the ``pip install`` command may need a ``sudo`` or
   "Run as Administrator" type of environment.
5. Make sure the directory pointed to by PATH, LD_LIBRARY_PATH or
   DYLD_LiBRARY_PATH for Windows, Linux and OSX respectively exists and contains
   the |Tecplot 360 EX| executable and library files.
6. If your script throws an exception when you attempt to call any pytecplot
   API, the most likely cause is a missing or invalid |Tecplot License|.

.. note:: If the license is missing or invalid, try the following:

    1. Be sure that the latest version of |Tecplot 360 EX| is first in your path
    2. Check to see if you can run |Tecplot 360 EX| by double clicking on the
       desktop icon (Windows), or from the command prompt.
    3. pytecplot should be able to find your license if you are able to run
       |Tecplot 360 EX|
    4. If you are able to run |Tecplot 360 EX| but still cannot run pytecplot,
       contact `Tecplot Technical Support <support@tecplot.com>`_.
