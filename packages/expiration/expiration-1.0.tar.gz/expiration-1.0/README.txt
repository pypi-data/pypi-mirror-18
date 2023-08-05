===========
expiration
===========

Overview
========

expiration is designed to manage complex expiration rules. My specific
use case is for backups, where I want to keep yearly backups forever,
monthly backups for 2 years, weekly backups for 3 months, daily
backups for 2 weeks, and hourly backups for 1 week. with expiration,
you'd implement the rules describing this as::

   >>> from __future__ import print_function
   >>> import expiration
   >>> from datetime import timedelta
   >>> expiration_rules = expiration.RetentionRules(timedelta(weeks=1),   # default value
   ...                                              [expiration.RetentionCriterion(expiration.date.year_of,
   ...                                                                             None),
   ...                                               expiration.RetentionCriterion(expiration.date.month_of,
   ...                                                                             timedelta(days=2*365)),
   ...                                               expiration.RetentionCriterion(expiration.date.week_of,
   ...                                                                             timedelta(days=30*3)),
   ...                                               expiration.RetentionCriterion(expiration.date.day_of,
   ...                                                                             timedelta(weeks=2)),
   ...                                               ])

Next, you need some items that you want to check for expiration. These
objects can be any type at all: expiration does not inspect them,
except to extract a timestamp from them. And you provide that
timestamp access function, called `time_key`.

For demonstration, I'll create a bunch of objects with expiration
dates::

   >>> from collections import namedtuple
   >>> from datetime import datetime
   >>> Item = namedtuple('Item', 'name expiration')
   >>> items = [Item(1, datetime(2012, 1, 1)),
   ...          Item(2, datetime(2014, 1, 3)),
   ...          Item(3, datetime(2014, 2, 1)),
   ...          Item(4, datetime(2014, 2, 2)),
   ...          Item(4, datetime(2014, 7, 1)),
   ...          Item(5, datetime(2014, 7, 25, 8, 0)),
   ...          Item(6, datetime(2014, 7, 25, 9, 0)),
   ...          Item(7, datetime(2014, 7, 25, 10, 0)),
   ...         ]

And now, we find which ones have expired::

   >>> from operator import attrgetter
   >>> for item, criterion in expiration.find_expired_items(items, attrgetter('expiration'),
   ...                                                             expiration_rules,
   ...                                                             asof_timestamp=datetime(2014, 8, 1)):
   ...    print(item)
   Item(name=4, expiration=datetime.datetime(2014, 2, 2, 0, 0))

This shows that under these rules, item 4 is the only one that would
be deleted. It's not the first one in a month and it's more than 3
months old, so it's due to be expired.

If, instead, we ask what items have expired as of January 1, 2020::

   >>> for item, criterion in expiration.find_expired_items(items, attrgetter('expiration'),
   ...                                                      expiration_rules,
   ...                                                      asof_timestamp=datetime(2020, 1, 1)):
   ...    print(item)
   Item(name=3, expiration=datetime.datetime(2014, 2, 1, 0, 0))
   Item(name=4, expiration=datetime.datetime(2014, 2, 2, 0, 0))
   Item(name=4, expiration=datetime.datetime(2014, 7, 1, 0, 0))
   Item(name=5, expiration=datetime.datetime(2014, 7, 25, 8, 0))
   Item(name=6, expiration=datetime.datetime(2014, 7, 25, 9, 0))
   Item(name=7, expiration=datetime.datetime(2014, 7, 25, 10, 0))

The only items that would be kept are 1 and 2, since they're the first
items at the start of each year, which has an infinite expiration
time.

Limitations
===========

Because `find_expired_items` only compares one item at a time to the
rules, it can effectively only implement "first of" rules. That is,
apply a criterion to the first backup of the year, or the first one of
the month, etc. It cannot currently implement rules like "keep the
second backup of the month". If you did delete the first backup and
kept the second one, then the next time `find_expired_items` ran, it
would see what used to be the second item as now being the first one.
