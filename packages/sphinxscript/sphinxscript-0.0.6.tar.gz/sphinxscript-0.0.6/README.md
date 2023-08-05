sphinx-script Script Documentation Module
=========================================

[![Travis-CI](https://img.shields.io/travis/ClimateImpactLab/sphinxscript/master.svg?style=flat-square "Travis CI")](https://travis-ci.org/ClimateImpactLab/sphinxscript)
[![PyPi](https://img.shields.io/pypi/v/sphinxscript.svg?style=flat-square "PyPi")](https://pypi.python.org/pypi/sphinxscript)
[![Coveralls](https://img.shields.io/coveralls/delgadom/sphinxscript.svg?style=flat-square "Coveralls")](https://coveralls.io/github/ClimateImpactLab/sphinxscript)

Produced by the [Climate Impact Lab](http://impactlab.org)

Overview
--------

Tool for building restructured text documentation for projects with scripts in many languages

Installation
------------

To install use pip:

    $ pip install sphinxscript


Or clone the repo:

    $ git clone https://github.com/ClimateImpactLab/sphinxscript.git
    $ python setup.py install

Usage
-----

Set up your repository using sphinx. Near the top of the `conf.py` configuration 
file, place the following lines:

    
    import sphinxscript
    sphinxscript.build_docs()

Finally, in your sphinx index file `index.rst`, include the following:

    .. toctree::

       sphinxscript



Using Sphinx-script with ReadTheDocs
------------------------------------

Include `sphinxscript` in the file `requirements.txt` in your root project 
directory. Then follow the usage steps above.


    
Contributing
------------

TBD

Example
-------

TBD
