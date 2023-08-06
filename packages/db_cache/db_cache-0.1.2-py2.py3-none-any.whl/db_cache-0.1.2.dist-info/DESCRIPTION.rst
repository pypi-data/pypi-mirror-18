===============================
DB Cache
===============================


.. image:: https://img.shields.io/pypi/v/db_cache.svg
        :target: https://pypi.python.org/pypi/db_cache

.. image:: https://img.shields.io/travis/bchiang2/db_cache.svg
        :target: https://travis-ci.org/bchiang2/db_cache

.. image:: https://readthedocs.org/projects/db-cache/badge/?version=latest
        :target: https://db-cache.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/bchiang2/db_cache/shield.svg
     :target: https://pyup.io/repos/github/bchiang2/db_cache/
     :alt: Updates


database caching for dynamic programming


* Free software: MIT license
* Documentation: https://db-cache.readthedocs.io.

Intro
--------


Guide
--------
TL;DR

    .. code-block:: python

        import db_cache

        # Instantiate cache object that connects to PostgreSQL with provided credential
        cache = db_cache.Cache(database="db_name", user="admin", password="12345", host="localhost")

        # Create decorater that cache function result using provided table name
        @cache.use_table("some_table_name")
        def some_expensive_function(large_int):
            prime1, prime2 = factoring(large_int)
            return (prime1, prime2)

        # Return cached value if possible, otherwise compute and cache result. 
        some_expensive_function(121103)


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.0 (2016-11-04)
------------------

* First release on PyPI.


