zip-code-radius
===============

:info: Generate minimum sets of zip codes, based on a radius, that
       can be used in a series of searches to cover the entire USA

Features
********

* downloads an up-to-date reference set of US postal codes from 
  a repository hosted on ``github.com``

Installation
------------

.. code-block:: shell

    pip install zip-code-radius

Usage
-----

.. code-block:: python

    import sys

    from zip_code_radius import solver

    radius = float(sys.argv[1])

    results = solver.solve(radius)

    print "radius: %d, zip-codes: %d" % (radius, len(results))

Notes
-----

``zip-code-radius`` stores the US postal code data at your os temp dir (e.g. /tmp/).
