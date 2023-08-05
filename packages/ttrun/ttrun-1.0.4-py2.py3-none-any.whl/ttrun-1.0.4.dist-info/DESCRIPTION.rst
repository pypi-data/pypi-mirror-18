=====
ttrun
=====

Simple CLI to run testtools tests

In a `testrepository` based workflow, sometimes you want/need to run individual
tests. Additionally, someitmes you want to use a pre-existing tox virtualenv
to do so. Or, at least, I do.

Typing

.. code-block:: bash

  .tox/py27/bin/python -m testtools.run some.test

Got boring. So this is a simple wrapper.

It has two modes.

.. code-block:: bash

  ttrun some.test

Will run that test with the system python.

If you want to re-use a tox virtualenv.

.. code-block:: bash

  ttrun -epy27 some.test

Will run some.test in the given tox venv.

Both modes can be run with no parameters to have testtools run all the tests.



