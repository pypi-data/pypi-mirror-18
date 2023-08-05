.. image:: https://travis-ci.com/DanielMaly/twall.svg?token=yoWLxXubPxheVtq154yv&branch=master
   :target: https://travis-ci.com/DanielMaly/twall.svg?token=yoWLxXubPxheVtq154yv&branch=master

TWall
=====

TWall is a simple application to display tweets returned by the
`Twitter's Search API <https://dev.twitter.com/rest/public/search>`_. You can run it from the command line to watch
newly added tweets in near real-time, or launch a simple web application on your machine that mirrors Twitter's search
feature. It supports all three modes of search offered by the API: recent, popular and mixed.

Developed for MI-PYT 2016/2017


Documentation
-------------
The module's documentation is located in the ``docs`` folder. To build HTML documentation, navigate to 
the directory, then run::

    pip install -r requirements.txt
    make html

This will create a ``_build/html`` folder containing an ``index.html`` file, which you can browse. If you don't
need the entire documentation and just want to get started quickly, follow the tutorial laid out in 
``docs/introduction.rst``.


Authors
-------

TWall is developed and maintained by `Daniel Maly <https://github.com/DanielMaly>`_


License
-------

`MIT <https://opensource.org/licenses/MIT>`_