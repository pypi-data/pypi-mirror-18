==================
getpodcast
==================

Simplify downloading podcasts with getpodcast


Installation
------------

    .. code-block:: bash

        sudo python3 -m pip install getpodcast


Getting started
---------------

Create a new file mypodcast.py:

    .. code-block:: python

        #! /usr/bin/env python3

        import getpodcast

        opt = getpodcast.parseArguments_AsOptions(
            date_from='2016-07-07',
            root_dir='./podcast')

        podcasts = {
            "TPB" : "http://tpbpodcast.libsyn.com/rss"
        }

        getpodcast.getpodcast(podcasts, "", opt)


To download podcasts:

    .. code-block:: bash

        python3 mypodcast.py --run


More help:

    .. code-block:: bash

        python3 mypodcast.py --help


Setup cronjob to download once a day:

    .. code-block:: bash

        0 19 * * * /usr/bin/python3 /home/myuser/mypodcasts.py --quiet --onlynew --run


