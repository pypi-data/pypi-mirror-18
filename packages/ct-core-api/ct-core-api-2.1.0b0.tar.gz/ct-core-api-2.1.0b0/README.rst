CT Core API
###########

.. _description:

CT Core API -- Catalant Core API Framework.

This framework enables developers to easily build and test **Flask web applications** that expose a **RESTful API**.

It is composed from a number of Python libraries and projects, most notably:

.. _documentation:

**Web Framework**

*Flask*
    http://flask.pocoo.org/

Flask -- ``0.11``
    http://flask.pocoo.org/docs/0.11/

webargs -- ``1.4``
    http://webargs.rtfd.org/

**Database / ORM**

*SQLAlchemy*
    http://www.sqlalchemy.org/

CT-Core-DB
    https://github.com/Catalant/ct-core-db/

**Object Serialization**

Marshmallow -- ``2.10``
    http://marshmallow.readthedocs.io/en/latest/

Flask-Marshmallow -- ``0.7``
    https://flask-marshmallow.readthedocs.io/en/latest/

Marshmallow-SQLAlchemy -- ``0.12``
    http://marshmallow-sqlalchemy.rtfd.org/

**REST / Swagger**

*Swagger (OpenAPI Specification)*
    https://github.com/OAI/OpenAPI-Specification

*Swagger-UI*
    https://github.com/swagger-api/swagger-ui

Flask-RESTful -- ``0.3``
    http://flask-restful.readthedocs.io/en/0.3.1/

apispec -- ``0.16``
    http://apispec.rtfd.org/

**Authentication / Authorization**

oauthlib -- ``2.0``
    http://oauthlib.rtfd.org/)

flask-oauthlib -- ``0.9``
    http://flask-oauthlib.rtfd.org/

flask-login -- ``0.3``
    http://flask-login.rtfd.org/

permission -- ``0.4``
    https://github.com/hustlzp/permission

bcrypt -- ``3.1``
    https://github.com/pyca/bcrypt/

**Distributed In-Memory Cache**

*memcached*
    https://memcached.org/

Dogpile-Cache -- ``0.6``
    http://dogpilecache.readthedocs.io/en/latest/usage.html

Flask-Dogpile-Cache -- ``0.2``
    https://bitbucket.org/ponomar/flask-dogpile-cache

**Distributed Task Queue**

*RabbitMQ*
    https://www.rabbitmq.com/

Celery -- ``3.1``
    http://www.celeryproject.org/

.. _requirements:

Requirements
============

- python ``2.6+``, ``3.3+`` / pypy2 (``2.5.0``)

.. _installation:

Installation
============

**CT Core API** is hosted on our internal `PyPi repository`_. It should be installed using pip::

    pip install ct-core-api

.. _PyPi repository: https://devpi.gocatalant.com/catalant/prod/ct-core-api

.. _usage:

Usage
=====

Please see the `Demo API Application`_ for a fully functioning example that demonstrates the setup and usage of the
framework components.

.. _Demo API Application: https://github.com/Catalant/ct-api-demo

Getting Started
---------------

This is how to create and register an API in your project::

    """catalant/example/app/__init__.py"""

    from ct_core_api.api import core
    from ct_core_api.api.app import create_api_app

    # TODO: Revise this example for 2.0

Here is what your application's main entry point should look like::

    """catalant/example/app/main.py"""

    #!/usr/bin/env python

    from catalant.example.app import create_example_api_app


    app = create_example_api_app()


    if __name__ == '__main__':
        from ct_core_api.api.app import runner
        runner.run(app)

Structuring the entry point as such allows us to invoke and run the Flask application as an executable script,
directly using Flask's development server, or using a uwsgi web server.

Changelog
---------
Every API application has it's own changelog. Developers are expected to update the changelog anytime a functional or
structural change to the API occurs.

"`Keep a CHANGELOG`_" has a good set of guiding principles for when and how a changelog should be maintained.

.. _Keep a CHANGELOG: http://keepachangelog.com/

By default, the API's changelog is accessible at ``/changelog`` and the entries live in ``changelog.yml`` in the
application's root folder (`APIApp.root_path`).

    You can modify the path to this file using the `API_CHANGELOG_PATH` config setting.

Format
``````

The changelog file uses the following YAML format::

    ---                                            # Separate changelog entries by date
    <yyyy-mm-dd>:                                  # The current date
      <added|changed|removed|deprecated>:          # The type of change
        - type: <operation|parameter|model|enum>:  # What kind of thing changed
          id: <identifier>                         # The changed thing's identifier
          [note]: <note>                           # An optional, human-friendly note of what changed


Legend
``````
operation
  A versioned endpoint operation

parameter
  An input parameter for one or more endpoint operation(s)

model
  A response model for one or more endpoint operations(s)

enum
  An Enum that one or more input parameter(s) use to represent a list of choices

.. _contributing:

Contributing
============

Development of ct-core-api happens at github: https://github.com/catalant/ct-core-api

Package Layout
--------------

The packages in this repository are carefully organized to avoid circular imports and to maintain the proper separation
of concerns.
It's safe to import and use modules from packages as long as they don't violate the ordering described below:

- ``ct_core_api.common``
- ``ct_core_api.core``
- ``ct_core_api.api.lib``
- ``ct_core_api.api.common``
- ``ct_core_api.api.core``
- ``ct_core_api.api.app``

Your module can reference other modules in the **same package** *or* in packages at the **same level or higher**
according to this list. For example, a module in ``ct_core_api.api.core`` can depend on one from
``ct_core_api.api.common`` but not on one from ``ct_core_api.api.app``.


Smoke Testing
-------------

Here's how you can run the dummy application to verify the basic functioning of the core API and web application:

Executable Python script::

    export PYTHONPATH=$PYTHONPATH:`pwd`
    ./ct_core_api/_main.py

Flask development server::

    export FLASK_APP=ct_core_api/_main.py
    export FLASK_DEBUG=1
    export FLASK_CONFIG=development
    flask run

.. _bugtracker:


Contributors
============

* jcrafford_ (Justin Crafford)

.. _license:

License
=======

Licensed under a `MIT license`_.

.. _links:

.. _MIT license: https://opensource.org/licenses/MIT
.. _jcrafford: https://github.com/jcrafford
