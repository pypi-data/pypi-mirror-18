============
Installation
============

At the command line::

    $ easy_install xsconnect

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv xsconnect
    $ pip install xsconnect

Some of the scripts use Tcl/Tk for the GUI,
so if you're using virtualenv under Windows, you might
need to place the following inside the Scripts\\activate.bat 
file in your virtual environment::

    set "TCL_LIBRARY=C:\WinPython\python-2.7.6\tcl\tcl8.5"

Edit the above command to reflect the location of the Tcl library directory
on your system.
