====================
Tribe-Client
====================

Tribe-client is a portable Python app to connect your bioinformatics server
or tool to the 'Tribe' web service (located at https://tribe.greenelab.com).

This package allows web servers created using
`Django <https://docs.djangoprojects.com/en/dev/>`_ to connect directly
to Tribe and make use of its resources. Users of the client web server or tool
can access their Tribe resources via Tribe `OAuth2 <http://oauth.net/2/>`_
authentication.


Requirements
------------
If you are using tribe-client in a web server that uses Django, we recommend
you use Django version 1.8 or newer.


Download and Install
---------------------
Tribe-client is registered as "tribe-client" in PyPI and is pip
installable:

.. code-block:: shell

	pip install tribe-client



Quick Start with Django
------------------------


1. Add ``tribe_client`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'tribe_client',
    )


2. Include the tribe-client URLconf in your project's URLconf (usually
``urls.py``):

.. code-block:: python

    from django.conf.urls import url, patterns, include

    urlpatterns = patterns('',
      ...
      (r'^tribe_client/', include('tribe_client.urls')),
    )


3. Register your client server at
https://tribe.greenelab.com/oauth2/applications/. Make sure to:

  a. Be logged-in using your Tribe account
  b. Select "Confidential" under ``Client type`` and
  c. Select "Authorization Code" under ``Authorization grant type``
  d. Enter your client server's address plus "/tribe_client/get_token" in the ``Redirect uris`` box. If your client server's current address is http://example.com, enter **http://example.com/tribe_client/get_token**

  .. note:: Currently, Tribe supports the following ``Authorization grant types``:

      * Authorization code
      * Resource owner password-based

    and does not support the following:

      * Implicit
      * Client credentials


4. Write down the Client ID in the ``TRIBE_ID`` setting and the Client secret
in the ``TRIBE_SECRET`` setting in your ``settings.py`` file like so:

.. code-block:: python

    TRIBE_ID = '*****Tribe Client ID*****'
    TRIBE_SECRET = '*****Tribe Client Secret*****'


5. The ``TRIBE_REDIRECT_URI`` setting should be the address of the client
server plus "/tribe_client/get_token".

.. code-block:: python

    TRIBE_REDIRECT_URI = 'http://example.com/tribe_client/get_token'


6. Define in your settings the scope that your client server should have
for Tribe resources. The two options are: 'read' and 'write'.The default
is 'read'. **Note:** The 'write' scope includes the 'read' scope access. 

.. code-block:: python

    TRIBE_SCOPE = 'write'  # Or 'read'


7. (Optional) If you want to use tribe_client's templates, make sure you have
a base template (which gets extended by your other templates and contains
the ``{% block content %}   {% endblock %}`` statements) that the tribe_client
templates can extend, and specify its name in your settings. The name of this
setting is ``TRIBE_CLIENT_BASE_TEMPLATE``. By default, tribe_client will
look for a template called ``base.html``.

.. code-block:: python

    TRIBE_CLIENT_BASE_TEMPLATE = 'name_of_your_main_template.html'


8. (Optional) If you want to use tribe_client's built-in login templates and
urls, make a link that takes the user to the ``connect_to_tribe`` url in your
website. This url will show users the built-in Tribe login page.
Below is an example of this type of link in the webpage's navbar:

.. code-block:: html

    <div class="collapse navbar-collapse">
      <ul class="nav navbar-nav navbar-right">
        <li><a href="{% url "connect_to_tribe" %}">Login with Tribe</a></li>
      </ul>
    </div>


9. (Optional) If you want to redirect your users to somewhere other than
the ``/tribe_client/display_genesets`` url after they have logged in,
you can define this in the ``TRIBE_LOGIN_REDIRECT`` setting in your
``settings.py`` file. **Note:** If you are not using the tribe-client
built-in templates (see above), you will need to define this setting so
your users have somewhere to go after they log in.

.. code-block:: python

    TRIBE_LOGIN_REDIRECT = '/place-to-go-after-login'


10. (Optional) If you want to redirect your users to somewhere other than
the ``/tribe_client`` url after they log out, you can define this in the
``TRIBE_LOGOUT_REDIRECT`` setting in your ``settings.py`` file.
**Note:** If you are not using the tribe-client built-in templates (see above),
you will need to define this setting so your users have somewhere to go after
they log out.

.. code-block:: python

    TRIBE_LOGOUT_REDIRECT = '/place-to-go-after-logout'


A Closer Look
-----------------------------

Under the hood, tribe-client has functions that:

1) Get an access token (via the `OAuth2 <http://oauth.net/2/>`_ protocol) that
allows users to access and create resources in Tribe.

2) Retrieves public and private collections (and their versions) and displays
them on the client server using views and templates included in the package.

3) Allows users to create new collections and versions remotely, from the
client server.
