AuthRocket
==========

Unofficial `AuthRocket`_ `API`_ client. Extends the Requests library,
provides a few helper functions.

See also
--------

The `Requests`_ documentation.

Making a request
----------------

.. code:: python

    import authrocket

    # Create an API object.
    # Config values can be found on your realm's integration page.
    api = authrocket.API(
        api_uri="https://api-e1.authrocket.com/v1/",
        api_key="ko_XYZ", # Must start with `ko_`, rather than old-style `key_`
        realm_id="rl_ABC"
    )

    # Fetch the first page of users.
    response = api.get("users")
    print response.json()

Pagination
----------

Use ``iter_from_pages`` to handle paginated responses:

.. code:: python

    for user in api.iter_from_pages("GET", "users"):
        print user

Path variables
--------------

Some APIs take variables via the path, e.g “users/123”. Rather than use
string interpolation, you should pass these via the ``variables``
argument - it’s more secure. For example:

.. code:: python

    response = api.get("user/{id}", variables={"id": "123"})
    print response.json()

.. _AuthRocket: https://authrocket.com/
.. _API: https://authrocket.com/docs/api
.. _Requests: http://docs.python-requests.org/en/master/
