=========
wraptools
=========

Utilities for wrapping and dispatching functions.

Supported Python versions:

* 2.7
* 3.4
* 3.5

pluggable
=========

``pluggable`` will take some decorators and simply apply it.
But applied decorators can be purged by ``purge_pluggable_decorators``.

.. code-block:: python

    from functools import lru_cache
    from wraptools.pluggable import pluggable

    @pluggable(
        lru_cache,
    )
    def get_data():
        """ Some function return data from RDB or so. """

``purge_pluggable_decorators`` is useful on tests.

.. code-block:: python

   from wraptools.pluggable import purge_pluggable_decorators

       @purge_pluggable_decorators
       def test__get_data(self):
            always_flesh_data = get_data()

Or it can be also used as a context manager.

.. code-block:: python

    with purge_pluggable_decorators():
        always_flesh_data = get_data()

``pluggable`` decorator can be useful for view functions of Web Frameworks,
like Django.

.. code-block:: python

    @pluggable(
        login_required,
    )
    def profile_view(request):
        return TemplateResponse(request, "profile.html")

dispatch
========

``dispatch`` will create function by some condition and functions.
Following example means

* When request is authenticated, ``dashboard`` function will be called.
* Other cases, ``landing_page`` function will be called.

.. code-block:: python

    from wraptools.dispatch import dispatch
    from wraptools.contrib.django.dispatchers import is_authenticated


    def landing_page(request):
        return TemplateResponse(request, "landing.html")


    def dashboard(request):
        return TemplateResponse(request, "dashboard.html")


    top_view = dispatch(
        (is_authenticated, dashboard),
        default=landing_page,
    )

Combine conditions
------------------

In this case ``dispatch`` is used for Django's view, but it can be used
generic Python functions.

``dispatcher`` functions can be combined and inverted.

* To create ``and`` condition, just combine dispatchers by ``&``
* ``or`` condition, by ``|``
* ``not`` condition, by ``~``

.. code-block:: python

    from wraptools.contrib.django.dispatchers import is_authenticated, method_get

    top = dispatch(
        (is_authenticated & method_get, dashboard_get),
        (is_authenticated & (method_post | method_put), dashboard_post),
        (~is_authenticated, landing),
    )

Create own dispatcher
---------------------

Basically dispatcher is just a function to get same arguments with dispatched functions
and return bool values.

.. code-block:: python

    def is_even(num):
        return num % 2 == 0

    def echo(num):
        return num

    dispatch(
        (is_even, echo),
        ...
    )

But by using ``dispatcher`` decorator, your dispatcher functions
will be able to be combined and inverted by ``&``, ``|``, or ``~``

.. code-block:: python

    from wraptools.dispatch import dispatcher

    dispatcher
    def is_even(num):
        return num % 2 == 0

    dispatch(
        (~is_even, ...),  # It will be called when the value is odd (not even).
        ...
    )


context
=======

``context`` is a decorator which injects additional arguments to wrapped functions.
Following example is to separate logic to get user object into ``get_user`` context function,
and applying it for ``profile_page`` view by ``context`` decorator.

.. code-block:: python

    from wraptools.context import context


    def get_user(user_id):
        return get_object_or_404(User, id=user_id)


    @context(
        get_user,
    )
    def profile_page(request, user_id, user):
        return TemplateResponse(request, "profile.html")

