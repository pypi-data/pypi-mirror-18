desmod
======

The desmod package provides a pythonic environment for composing
Discrete Event Simulation MODels. The excellent `SimPy`__ package
provides the discrete event simulation kernel. Desmod provides
additional capabilities useful for composing, monitoring, configuring,
and simulating arbitrarily complex models.

__ https://simpy.readthedocs.io/en/latest/

.. image:: https://readthedocs.org/projects/desmod/badge/?version=latest
    :target: https://desmod.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://travis-ci.org/SanDisk-Open-Source/desmod.svg?branch=master
    :target: https://travis-ci.org/SanDisk-Open-Source/desmod
    :alt: Build Status


Installation
------------

Desmod is available on PyPI and can be installed with `pip`::

    pip install desmod


Resources
---------

* `Documentation on ReadTheDocs <http://desmod.readthedocs.io/>`_
* `Questions and development discussion Google Group
  <https://groups.google.com/forum/?hl=en#!forum/desmod>`_
* `Source code and issue tracker on GitHub
  <https://github.com/SanDisk-Open-Source/desmod>`_
* `Package on PyPI <https://pypi.python.org/pypi/desmod>`_
* `Continuous integration on TravisCI
  <https://travis-ci.org/SanDisk-Open-Source/desmod>`_


MIT License

Copyright (c) 2016 Western Digital Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Changlog
========

desmod-0.2.0 (2016-10-25)
-------------------------
* [CHANGE] simulate_factors() now has factors parameter
* [NEW] simulate() can suppress exceptions
* [FIX] simulate_factors() respects sim.workspace.overwrite
* [CHANGE] Update config with missing defaults at runtime

desmod-0.1.6 (2016-10-25)
-------------------------
* [NEW] Add env.time() and 'sim.now' result
* [FIX] Enter workspace directory before instantiating env
* [CHANGE] Use yaml.safe_dump()
* [FIX] Add dist to .gitignore
* [FIX] Squash warning in setup.cfg

desmod-0.1.5 (2016-10-17)
-------------------------
* [NEW] Add Queue.size and Queue.remaining properties (#9)
* [NEW] Trace Queue's remaining capacity (#10)
* [NEW] Add Queue.when_new() event (#11)

desmod-0.1.4 (2016-09-21)
-------------------------
* [NEW] Add desmod.simulation.simulate_many()
* [FIX] Repair various docstring typos
* [FIX] Disable progress bar for simulate_factors() on Windows
* [NEW] Add CHANGELOG.txt to long description in setup.py

desmod-0.1.3 (2016-07-28)
-------------------------
* [NEW] Cancelable Queue events
* [CHANGE] Connection errors now raise ConnectError
* [FIX] Update pytest-flake8 and flake8 dependencies (yet again)

desmod-0.1.2 (2016-07-26)
-------------------------
* [NEW] Add "sim.log.buffering" configuration
* [FIX] Repair unit tests (pytest-flake8 dependency)
* [NEW] New optional `Queue.name` attribute
* [FIX] Use `repr()` for exception string in result dict

desmod-0.1.1 (2016-07-14)
-------------------------
* [FIX] Using 'True' and 'False' in expressions from the command line
* [CHANGE] Improve simulation workspace handling (sim.workspace.overwrite)
* [CHANGE] Make some 'sim.xxx' configuration keys optional
* [NEW] Gas Station example in docs
* [NEW] Add this CHANGELOG.rst and History page in docs

desmod-0.1.0 (2016-07-06)
-------------------------
* Initial public release


