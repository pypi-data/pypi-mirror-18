The ``jicparameters`` Python package
=======================================

.. image:: https://travis-ci.org/JIC-CSB/jicparameters.svg?branch=master
   :target: https://travis-ci.org/JIC-CSB/jicparameters
   :alt: Travis CI build status (Linux)

.. image:: https://ci.appveyor.com/api/projects/status/7llm3pjuk3ncr7sv?svg=true
   :target: https://ci.appveyor.com/project/tjelvar-olsson/jicparameters
   :alt: AppVeyor CI build status (Windows)


.. image:: http://codecov.io/github/JIC-CSB/jicparameters/coverage.svg?branch=master
   :target: http://codecov.io/github/JIC-CSB/jicparameters?branch=master
   :alt: Code Coverage

.. image:: https://readthedocs.org/projects/jicparameters/badge/?version=latest
   :target: https://readthedocs.org/projects/jicparameters?badge=latest
   :alt: Documentation Status


Python package making it easier to work with lots of parameters.

- Documentation: http://jicparameters.readthedocs.io/en/latest/
- GitHub: https://github.com/JIC-CSB/jicparameters
- Free software: MIT License

Features
--------

- Lightweight: only depends on PyYAML
- Cross-platform: Linux, Mac and Windows are all supported
- Tested with Python 2.7, 3.3, 3.4, and 3.5


Quick Guide
-----------

To install ``jicparameters``::

    git clone https://github.com/JIC-CSB/jicparameters.git
    cd jicparameters
    python setup.py install

Create some parameters::

    >>> from jicparameters import Parameters
    >>> params = Parameters(pi=3.14, radius=10)
    >>> params
    {'pi': 3.14, 'radius': 10}

Add another parameter::

    >>> params["fudge_factor"] = 42
    >>> params
    {'fudge_factor': 42, 'pi': 3.14, 'radius': 10}

View as YAML::

    >>> print(params.to_yaml())
    ---
    fudge_factor: 42
    pi: 3.14
    radius: 10
    <BLANKLINE>

Save to file::

    >>> params.to_file("params.yml")

Read from file::

    >>> p2 = Parameters.from_file("params.yml")
    >>> assert params == p2


History
-------

0.1.0
^^^^^

- Initial upload to PyPi
