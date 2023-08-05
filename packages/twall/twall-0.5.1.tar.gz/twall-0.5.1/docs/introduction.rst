Getting Started
===============

This section has everything you need to quickly get the TWall application up and running.

Installation
------------

To install TWall, simply run this simple command in your terminal of choice::

    pip install twall

TWall will be automatically downloaded and installed. We recommend installing TWall inside a
`virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

.. _oauth-setup:

Configuration
-------------

TWall accesses the Twitter Developer API which is a protected resource. You will need OAuth application credentials
provided by Twitter to make use of the API. These credentials must be given to TWall so it can request an authorization
token.

To access the Twitter Search API, we will use application-only authentication, as described in the
`Twitter docs <https://dev.twitter.com/oauth/application-only/>`_. First, you need to create a Twitter application
`here <https://apps.twitter.com>`_. This will immediately enable to use all public API methods that don't require
user login.

Once you have your OAuth credentials, you will need to put them in a configuration file for TWall to read.
To create an authentication file for TWall, you will need two strings: your app's `consumer key` and `consumer secret`.
Both can be found under your application's settings.

You can place this file anywhere you like - TWall will require you to provide a path to it.
The file's syntax is the following::

    [twitter_oauth]
    consumer_key = XXX
    consumer_secret = XXX

"XXX" needs to be replaced by your consumer key and secret. Please keep your consumer secret private, and **NEVER**
commit the authentication file to version control.


Launching The Console Application
---------------------------------

The console application will display tweets in the terminal. When the application is launched, it will display a
certain number of old tweets, then keep polling Twitter for newer tweets periodically and display them as they arrive
until you quit the application by entering the string ``Q``.

To launch the console application, type the following in your terminal::

    python -m twall console "your query" --auth-file path/to/your/authentication/file

The application will spawn two worker threads and start displaying tweets. Several other options are supported:

* ``-c/--count`` will control how many old tweets should be loaded at startup.
* ``-i/--interval`` will control how often the app will poll the Twitter API. Enter a value in seconds.
* ``-t/--result-type`` is one of ``recent``, ``popular`` or ``mixed`` and specifies what type of tweets should be returned.

If you don't specify the ``--auth-file`` option, the application will look for a file named ``auth.cfg`` in the current
working directory.

As it is impossible to format tweets the way they are supposed to be viewed on the web, it will only display
the tweeting user's screen name and the tweet text.

Launching The Web Application
-----------------------------

The web application runs on the `Flask <http://flask.pocoo.org>`_ framework and displays a simple search bar for the
user to enter his or her query, optionally specifying the result type.
Once a query is submitted, it displays the loaded tweets on a single page.
Unlike the console version, the web application enriches the tweet text to include hashtags, mentions, links and images.
Also unlike the console version, tweets currently aren't being loaded in real-time after a query is entered.

To launch the web application, type the following in your terminal::

    python -m twall web --auth-file path/to/your/authentication/file

Flask will start listening for requests on localhost using the default Flask port.

The following additional options are supported:

* ``--debug`` will launch Flask in debug mode.

If you don't specify the ``--auth-file`` option, the application will look for a file named ``auth.cfg`` in the current
working directory.
