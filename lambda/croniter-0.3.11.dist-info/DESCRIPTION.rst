Introduction
============

.. contents::


croniter provides iteration for datetime object with cron like format.

::

                          _ _
      ___ _ __ ___  _ __ (_) |_ ___ _ __
     / __| '__/ _ \| '_ \| | __/ _ \ '__|
    | (__| | | (_) | | | | | ||  __/ |
     \___|_|  \___/|_| |_|_|\__\___|_|


Website: https://github.com/kiorky/croniter

Travis badge
=============
.. image:: https://travis-ci.org/kiorky/croniter.png
    :target: http://travis-ci.org/kiorky/croniter

Usage
============

Simple example of usage is followings::

    >>> from croniter import croniter
    >>> from datetime import datetime
    >>> base = datetime(2010, 1, 25, 4, 46)
    >>> iter = croniter('*/5 * * * *', base)  # every 5 minites
    >>> print iter.get_next(datetime)   # 2010-01-25 04:50:00
    >>> print iter.get_next(datetime)   # 2010-01-25 04:55:00
    >>> print iter.get_next(datetime)   # 2010-01-25 05:00:00
    >>>
    >>> iter = croniter('2 4 * * mon,fri', base)  # 04:02 on every Monday and Friday
    >>> print iter.get_next(datetime)   # 2010-01-26 04:02:00
    >>> print iter.get_next(datetime)   # 2010-01-30 04:02:00
    >>> print iter.get_next(datetime)   # 2010-02-02 04:02:00

All you need to know is constructor and get_next, these signature are following::

    >>> def __init__(self, cron_format, start_time=time.time())

croniter iterate along with 'cron_format' from 'start_time'.
cron_format is 'min hour day month day_of_week', and please refer to
http://en.wikipedia.org/wiki/Cron for details.::

    >>> def get_next(self, ret_type=float)

get_next return next time in iteration with 'ret_type'.
And ret_type accept only 'float' or 'datetime'.

Now, supported get_prev method. (>= 0.2.0)::

    >>> base = datetime(2010, 8, 25)
    >>> itr = croniter('0 0 1 * *', base)
    >>> print itr.get_prev(datetime)  # 2010-08-01 00:00:00
    >>> print itr.get_prev(datetime)  # 2010-07-01 00:00:00
    >>> print itr.get_prev(datetime)  # 2010-06-01 00:00:00


Develop this package
====================

::

    git clone https://github.com/kiorky/croniter.git
    cd croniter
    python bootstrap.py -d
    bin/buildout -vvvvvvN
    bin/test


Make a new release
====================
We use zest.fullreleaser, a great releaser infrastructure.

Do and follow the instructions
::

    bin/fullrelease


Contributors
===============
Thank you to all who have contributed to this project!
If you contributed and not listed below please let me know.

    - mrmachine
    - Hinnack
    - shazow
    - kiorky
    - jlsandell
    - mag009
    - djmitche
    - GreatCombinator
    - chris-baynes
    - ipartola
    - yuzawa-san



Changelog
==============

0.3.11 (2016-01-13)
-------------------

- Bug fix: The get_prev API crashed when last day of month token was used. Some
  essential logic was missing.
  [Iddo Aviram <iddo.aviram@similarweb.com>]


0.3.10 (2015-11-29)
-------------------

- The fuctionality of 'l' as day of month was broken, since the month variable
  was not properly updated
  [Iddo Aviram <iddo.aviram@similarweb.com>]

0.3.9 (2015-11-19)
------------------

- Don't use datetime functions python 2.6 doesn't support
  [petervtzand]

0.3.8 (2015-06-23)
------------------
- Truncate microseconds by setting to 0
  [Corey Wright]


0.3.7 (2015-06-01)
------------------

- converting sun in range sun-thu transforms to int 0 which is
  recognized as empty string; the solution was to convert sun to string "0"

0.3.6 (2015-05-29)
------------------

- Fix default behavior when no start_time given
  Default value for `start_time` parameter is calculated at module init time rather than call time.
- Fix timezone support and stop depending on the system time zone



0.3.5 (2014-08-01)
------------------

- support for 'l' (last day of month)


0.3.4 (2014-01-30)
------------------

- Python 3 compat
- QA Relase


0.3.3 (2012-09-29)
------------------
- proper packaging



