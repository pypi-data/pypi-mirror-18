|PyPI package| |Documentation| |Test results| |Test coverage| |Code
analysis| |License| |Analytics|

nose2unitth
===========

Convert `nose <http://nose.readthedocs.io>`__-style XML test reports to
`UnitTH <http://junitth.sourceforge.net/>`__-compatible XML reports

Example
-------

-  `nose-style XML report <examples/nose.xml>`__
-  `UnitTH-style XML report <examples/unitth/1>`__
-  `UnitTH HTML test history
   report <https://cdn.rawgit.com/KarrLab/nose2unitth/master/examples/html/index.html>`__

Installation
------------

::

    pip install nose2unitth

Usage
-----

::

    # convert nose-style reports to UnitTH-style reports
    nosetests <package-to-test> --with-xunit --xunit-file=examples/nose.xml

    mkdir -p examples/unitth
    nose2unitth examples/nose.xml examples/unitth/1
    nose2unitth examples/nose.xml examples/unitth/2

    junit2html examples/nose.xml examples/unitth/1/index.html
    junit2html examples/nose.xml examples/unitth/2/index.html

    # generate HTML test report
    java \
        -Dunitth.generate.exectimegraphs=true \
        -Dunitth.xml.report.filter= \
        -Dunitth.html.report.path=. \
        -Dunitth.report.dir=examples/html \
        -jar unitth.jar examples/unitth/*

Documentation
-------------

Please see the documentation at `Read the
Docs <http://nose2unitth.readthedocs.io>`__.

Tests
-----

Running the tests
~~~~~~~~~~~~~~~~~

``nose`` can be used to run the tests:

::

    nosetests tests \
      --with-xunit --xunit-file=test-report.xml \
      --with-coverage --cover-package=nose2unitth

Please note that additional packages are required for testing (see
`tests/requirements.txt <tests/requirements.txt>`__).

License
-------

The example model is released under the `MIT license <LICENSE>`__.

Development team
----------------

``nose2unitth`` was developed by `Jonathan
Karr <http://www.karrlab.org>`__ at the Icahn School of Medicine at
Mount Sinai in New York, USA.

Questions and comments
----------------------

Please contact the `Jonathan Karr <http://www.karrlab.org>`__ with any
questions or comments.

.. |PyPI package| image:: https://img.shields.io/pypi/v/nose2unitth.svg
   :target: https://pypi.python.org/pypi/nose2unitth
.. |Documentation| image:: https://readthedocs.org/projects/nose2unitth/badge/?version=latest
   :target: http://nose2unitth.readthedocs.org
.. |Test results| image:: https://circleci.com/gh/KarrLab/nose2unitth.svg?style=shield
   :target: https://circleci.com/gh/KarrLab/nose2unitth
.. |Test coverage| image:: https://coveralls.io/repos/github/KarrLab/nose2unitth/badge.svg
   :target: https://coveralls.io/github/KarrLab/nose2unitth
.. |Code analysis| image:: https://codeclimate.com/github/KarrLab/nose2unitth/badges/gpa.svg
   :target: https://codeclimate.com/github/KarrLab/nose2unitth
.. |License| image:: https://img.shields.io/github/license/KarrLab/nose2unitth.svg
   :target: LICENSE
.. |Analytics| image:: https://ga-beacon.appspot.com/UA-86759801-1/nose2unitth/README.md?pixel
