
##############
Brillouin Zone
##############

.. contents::
.. section-numbering::
.. raw:: pdf

    PageBreak oneColumn

=====
About
=====

This package provides an object bz, that defines a lattice in momentum (k) space
by means of the minimal wedge of the Brillouin Zone. The minimal wedge includes all
**k = (kx, ky)** *: kx in [0,pi], ky <= kx*.  It is initialized by
 
.. code-block:: python
     
    >>> import brillouin_zone 
    >>> brillouin_zone.bz( (int)kpts )

where kpts is the number of k points in one direction (e.g. kx).

* Python 3 support
* Linus, Mac OS X and Windows support
* Documentation
* Ongoing development

============
Installation
============
-----------
Requirement
-----------

#. **Phython3**

   **Mac OS X**: Assuming you are using `Homebrew <http://brew.sh>`_ as package manager 

   .. code-block:: bash
        
        # Install Python3
        $ brew install python3

        # Get access to the scientific Python formulas
        $ brew tap Homebrew/python
        
        # Install Numpy and Matplotlib
        $ brew install numpy --with-python3
        $ brew install matplotlib --with-python3

   **Linux**:

   .. code-block:: bash

        # Download and unpack source
        $ wget --no-check-certificate http://python.org/ftp/python/3.5.2/Python-3.5.2.tgz
        $ tar zxvf Python-3.5.2.tgz

        # Installation
        $ ./configure
        $ make
        $ make test
        $ sudo make install
        # Or else refere to the Python-3.5.2/README

#. **Boost-Python**

   **Mac OS X**:

   .. code-block:: bash

        # Insatll Boost
        $ brew install boost
        
        # Install Boost-Python for Python3
        $ brew install boost-python --with-python3 --without-python


#. **Pip3**: This is probably already installed, but if not please check 
   the `official site <https://pip.pypa.io/en/latest/installing/>`_.

   .. code-block:: bash

        # Check if installed
        $ pip3

   **Linux**:

   .. code-block:: bash

        $ wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
        $ python3 get-pip.py 

#. Set **g++** as compiler
   
   .. code-block:: bash

        # Install g++
        $ brew install gcc

        # **ATTENTION**: This may be the only step everyone needs to do!
        $ export CC=g++

   I am sorry for the inconvenience here. setup.py checks the enviroment 
   variable CC for the compiler and the default clang won't do.

Caveat: Numpy for python3

    **Mac OS X**:

    .. code-block:: bash

        # Install Numpy and Matplotlib
        $ brew install numpy --with-python3
        $ brew install matplotlib --with-python3

    **Linux**:

    .. code-block:: bash

        # Install Numpy
        $ pip3 install numpy
---------------
Get the package
---------------

A universal installation method (that works on **Windows**, **Mac OS X**, **Linux**, ...) is
to use **pip3**: 
 
.. code-block:: bash

    # Update setuptools used by python
    $ pip3 install -U setuptools

    # Download and install the package
    $ pip3 install brillouin-zone
 

-------------------
Development version
-------------------

This README and version currently undergoes heavy changes. 

---------
Extension
---------

 padefit - A package providing the objects selfenergy and greensfunctions as well
           as all functions needed to perfom an analytic continuation from the
           Matsubara axis to the real axis by means of a Pade Approximation.

=====
Usage
=====

-------
Example
-------

====
Meta
====

-------
Authors
-------

--------------
Acknowledgment
--------------




