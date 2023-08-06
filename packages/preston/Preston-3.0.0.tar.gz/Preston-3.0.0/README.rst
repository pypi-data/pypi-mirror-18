Preston
=======

Preston is a Python library for accessing EVE Online's CREST, XML, and
ESI APIs.

Installation
------------

From `pip <https://pip.pypa.io/en/stable/>`__:

.. code:: bash

    pip install preston

From GitHub:

.. code:: bash

    git clone https://github.com/Celeo/Preston.git
    cd Preston
    python setup.py install

Initialization
--------------

.. code:: python

    from preston.crest import Preston
    # or
    from preston.xmlapi import Preston
    # or
    from preston.esi import Preston

    preston = Preston()

Usage
=====

See the documents under ``docs/`` for the modules' usages.
