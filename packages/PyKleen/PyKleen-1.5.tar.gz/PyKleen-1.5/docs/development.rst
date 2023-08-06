Development
===========

Some simple instructions for the development of PyKleen.

Setup
-----

Setup your virtual environment, activate it and install the requirements.

.. code-block:: bash

  virtualenv --no-site-packages -p `which python3.5` venv
  source venv/bin/activate
  pip install -r requirements.txt
  deactivate && source venv/bin/activate

Development
-----------

While doing your development run:

.. code-block:: bash

  PYTHONPATH=. ptw

Or, when you don't want to keep the test running:

.. code-block:: bash

  python setup.py test

After you are finished, you need to update the documentation:

.. code-block:: bash

  cd docs && make livehtml


Release
-------

#. Update the version number in `VERSION`.
#. Run the tests once more (better to be sure, right?).
#. Commit and push to GIT.
#. Release the code.

.. code-block:: bash

  echo "X.X" > VERSION
  python setup.py test
  ga . && gc -m 'Bump to version X.X' && gp
  python setup.py sdist upload -r pypi
