PyKleen
=======

Input; simple, clean.

`readthedocs.org <http://pykleen.readthedocs.io/en/latest/>`_

Example
-------

This is how you do it.

.. code-block:: python

  # -*- coding: utf-8 -*-
  import pykleen as k

  schema = k.Schema({
      'name': k.string(min_len=1),
      'age': k.numeric(),
      'addresses': k.list_of(k.Schema({
          'number': k.numeric(),
          'postal': k.string(min_len=4, max_len=8),
      })),
  })

  person = schema({
      'name': 'Kleener',
      'age': '38',
      'addresses': [{
          'number': '40',
          'postal': '67768GG',
      }]
  })

There are more tests and you can build your own! You can view the documentation on
`readthedocs.org <http://pykleen.readthedocs.io/en/latest/>`_.
