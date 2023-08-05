Usage In Code
=============

It is possible to use TWall as a library in your code instead of a stand-alone application. There are two
general scenarios: using it to load tweets from Twitter (periodically or as a one-shot request) and using the web
application's helper methods to render enriched tweet text and images.


Configuring TWall
-----------------

In order to use any methods that call the Twitter API, you will first need to configure TWall with your own
authentication file. See :ref:`oauth-setup` for details on how to create this file.

Run the following code to obtain a ``configparser`` instance with the configuration all loaded and ready to go::

    import twall
    cfg = twall.read_config('path/to/auth/file')


Getting a Twitter Session
-------------------------

To communicate with the Twitter API, you will need a ``requests`` session containing the proper authorization data.
TWall makes this easy by providing a method that will create this session for you::

    from twall.twitter import twitter_session
    session = twitter_session(cfg)

``cfg`` is the configuration object you obtained in the previous step.


Loading Tweets Once
-------------------

You can use an initialized Twitter session to make one-shot requests to the API. To do so, use the
:func:`~twall.twitter.load_tweets` method with your configuration object and initialized session.
See the method documentation for information about the method's arguments.


Loading Tweets Periodically
---------------------------

You can make use of the :class:`~twall.console.WallWorker` to poll the Twitter API periodically. With this method,
there is no need to initialize a Twitter session - the worker will do it automatically. Simply construct a
``queue`` object and create a WallWorker like this::

    from twall.console import WallWorker
    worker = WallWorker(cfg, queue, query, interval, result_type, initial_count)

``cfg`` is again the configuration object you obtained in the first step. The ``interval`` should be an integer value
specifying the polling interval in seconds. The ``result_type`` parameter should be one
of ``recent``, ``popular`` or ``mixed``. The ``initial_count`` represents the number of old tweets to be loaded in the
first request.

To start the worker, use::

    worker.run()

The WallWorker will run on its own thread and place newly loaded tweets in the queue. To stop loading tweets, call::

    worker.stop()

Once stopped, a ``WallWorker`` cannot be started again. You have to instantiate a new one.


Rendering Tweet HTML
--------------------

You can use the web application's helper methods to get lightweight tweet HTML with mentions, hashtags and links, ready
for embedding into your own application.


The first method is :func:`~twall.web.render_tweet` that will return a Flask ``Markup`` object containing the tweet's
text with inline HTML containing ``<a>`` tags with links to Twitter and elsewhere. Here is an example of its usage.

Suppose we have a tweet that looks something like this:

.. testsetup::

    tweet = {
        'text': 'Connecting to an RDBMS from #Python - a cheat sheet about #SQLAlchemy https://t.co/EBy16BblVN',
        'entities': {'hashtags': [{'indices': [28, 35], 'text': 'Python'},
                           {'indices': [58, 69], 'text': 'SQLAlchemy'}],
              'symbols': [],
              'urls': [{'display_url': 'github.com/crazyguitar/py…',
                        'expanded_url': 'https://github.com/crazyguitar/pysheeet/blob/master/docs/notes/python-sqlalchemy.rst',
                        'indices': [70, 93],
                        'url': 'https://t.co/EBy16BblVN'}],
              'user_mentions': []}
    }


We can render this tweet using:

.. testcode::

   from twall.web import render_tweet
   html = render_tweet(tweet)
   print(html)

This will output:

.. testoutput::

    Connecting to an RDBMS from <a href="https://twitter.com/hashtag/Python" target="_blank">#Python</a> - a cheat sheet about <a href="https://twitter.com/hashtag/SQLAlchemy" target="_blank">#SQLAlchemy</a> <a href="https://github.com/crazyguitar/pysheeet/blob/master/docs/notes/python-sqlalchemy.rst" target="_blank">https://t.co/EBy16BblVN</a>

The other method renders an ``<img>`` tag from a media object. Here is an example usage. Suppose we have the following
media object:

.. testsetup::

    media = {'display_url': 'pic.twitter.com/MbvNBBnOAT',
                         'expanded_url': 'https://twitter.com/samm_emmanuel/status/795651771347640320/photo/1',
                         'id': 795651768160030725,
                         'id_str': '795651768160030725',
                         'indices': [93, 116],
                         'media_url': 'http://pbs.twimg.com/media/Cwq5EU4XEAUX5iM.jpg',
                         'media_url_https': 'https://pbs.twimg.com/media/Cwq5EU4XEAUX5iM.jpg',
                         'sizes': {'large': {'h': 368,
                                             'resize': 'fit',
                                             'w': 680},
                                   'medium': {'h': 368,
                                              'resize': 'fit',
                                              'w': 680},
                                   'small': {'h': 368,
                                             'resize': 'fit',
                                             'w': 680},
                                   'thumb': {'h': 150,
                                             'resize': 'crop',
                                             'w': 150}},
                         'source_status_id': 795651771347640320,
                         'source_status_id_str': '795651771347640320',
                         'source_user_id': 2892559686,
                         'source_user_id_str': '2892559686',
                         'type': 'photo',
                         'url': 'https://t.co/MbvNBBnOAT'}

We can generate the markup using this code:

.. testcode::

    from twall.web import render_media
    html = render_media(media)
    print(html)

The output of this will be:

.. testoutput::

    <img src="http://pbs.twimg.com/media/Cwq5EU4XEAUX5iM.jpg" width="400" height="216.47058823529412"/>