Tapioca CircleCI
================

|CircleCI Status|

----

CircleCI API Wrapper using tapioca https://circleci.com/docs/api/

*Note: Not all endpoints are mapped, please open an issue if you need*


Installation
------------

**IMPORTANT**: Only Python 3.5+

.. code-block:: bash

    pip install tapioca-circleci


Documentation
-------------

.. code-block:: python

    from tapioca_circleci import CircleCI

    api = CircleCI(
        token='{your-token}'  # required,
        timeout=5,  # Optional, defaults to 5s
    )


To generate API tokens, access your dashboard: [https://circleci.com/account/api](https://circleci.com/account/api)


Serialization
-------------

* datetime
* Decimal


Deseralization
--------------

* datetime
* Decimal


More
----

* Learn how Tapioca works [here](http://tapioca-wrapper.readthedocs.org/en/stable/quickstart.html)
* Explore this package using iPython
* Have fun!


.. |CircleCI Status| image:: https://circleci.com/gh/georgeyk/tapioca-circleci/tree/master.svg?style=svg
   :target: https://circleci.com/gh/georgeyk/tapioca-circleci/tree/master
