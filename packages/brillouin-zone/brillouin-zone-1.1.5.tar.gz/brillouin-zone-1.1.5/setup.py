# CC=g++ python3 setup.py install
# from distutils.core import setup, Extension
#!export CC=g++
from setuptools import setup, Extension

from codecs import open
from os import path

module = Extension( 'brillouin_zone',
        include_dirs = ['/usr/local/Cellar/boost/1.62.0/include'],
        libraries    = ['boost_python-mt'],
        extra_compile_args = ["-std=c++14"],
        sources      = ['brillouin_zone/bz_wrapper.cpp',
                        'brillouin_zone/brillouin_zone.cpp',
                        'brillouin_zone/functions.cpp'
                        ]
                    )

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup ( name = 'brillouin-zone',

        # MAJOR.MINOR.MAINTENANCE
        # MAJOR version when making incompatible API changes
        # MINOR version when adding functionality in a backwards-compatible manner
        # MAINTENANCE when making backwards-compatible bug fixes
        version = '1.1.5',
        
        description = 'Provides the object bz, that defines a lattice in mometum space.',
        long_description=long_description,

        author='Marie-Therese Philipp',
        author_email='marie.therese1@gmx.de',

        license='MIT',

        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Physics',
            'Programming Language :: C++',
            'Programming Language :: Python :: 3.5',
            'Operating System :: MacOS'
            ],

        keywords=['condensed matter', 'many-body physics', 'TU Wien', 'Russian Quantum Center'],
        
        ext_modules = [module] 
)



