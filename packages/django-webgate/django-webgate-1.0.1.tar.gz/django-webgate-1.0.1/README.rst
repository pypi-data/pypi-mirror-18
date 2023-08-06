django-webgate
==============

A Django Authentication Middleware for WebGate Oracle Access Manager.

This is a subclass of the RemoteUserMiddleware. The header value is
configurable by setting a django setting of WEBGATE\_HEADER.

.. code:: python

    WEBGATE_HEADER = 'CUSTOM_WEBGATE_HEADER'

**Note:** The default header value is ``OAM_REMOTE_USER``

Quick Start
-----------

**1. Install using pip:**
::

    pip install django-webgate

**2. Include "webgate" to your INSTALLED\_APPS:**

.. code-block:: python

    INSTALLED_APPS = [
        'webgate',
    ]

**3. Include "OracleAccessManagerMiddleware" in MIDDLEWARE\_CLASSES:**

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'webgate.middleware.OracleAccessManagerMiddleware',
    )
