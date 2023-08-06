python-t77-date
===============

.. image:: https://travis-ci.org/tomi77/python-t77-date.svg?branch=master
   :target: https://travis-ci.org/tomi77/python-t77-date
.. image:: https://coveralls.io/repos/github/tomi77/python-t77-date/badge.svg?branch=master
   :target: https://coveralls.io/github/tomi77/python-t77-date?branch=master
.. image:: https://codeclimate.com/github/tomi77/python-t77-date/badges/gpa.svg
   :target: https://codeclimate.com/github/tomi77/python-t77-date
   :alt: Code Climate

A set of functions related with dates

Installation
------------

Install via ``pip``

::

   pip install t77_date

datetime module
---------------

start_of_day
~~~~~~~~~~~~

Return a new datetime with values that represent a start of a day.

Example
::

   >>> dt = datetime(2016, 7, 2, 21, 49, 12)
   >>> sod = start_of_day(dt)
   >>> print(sod)
   2016-07-02 00:00:00

end_of_day
~~~~~~~~~~

Return a new datetime with values that represent a end of a day.

Example
::

   >>> dt = datetime(2016, 7, 2, 21, 49, 12)
   >>> eod = end_of_day(now)
   >>> print(eod)
   2016-07-02 23:59:59.999999

start_of_month
~~~~~~~~~~~~~~

Return a new datetime with values that represent a start of a month.

Example
::

   >>> dt = datetime(2016, 7, 2, 21, 49, 12)
   >>> som = start_of_month(dt)
   >>> print(som)
   2016-07-01 00:00:00

end_of_month
~~~~~~~~~~~~

Return a new datetime with values that represent a end of a month.

Example
::

   >>> dt = datetime(2016, 7, 2, 21, 49, 12)
   >>> eom = end_of_day(now)
   >>> print(eom)
   2016-07-31 23:59:59.999999

set_next_week_day
~~~~~~~~~~~~~~~~~

Set week day.
New date will be greater or equal than input date.

Example
::

   >>> saturday = datetime(2016, 7, 2, 21, 49, 12)
   >>> next_friday = set_next_week_day(saturday, ISO_FRIDAY, iso=True)
   >>> print(next_friday)
   2016-07-08 21:49:12
   >>> next_friday = set_next_week_day(saturday, FRIDAY, iso=False)
   >>> print(next_friday)
   2016-07-08 21:49:12

set_prev_week_day
~~~~~~~~~~~~~~~~~

Set week day.
New date will be less or equal than input date.

Example
::

   >>> saturday = datetime(2016, 7, 2, 12)
   >>> prev_friday = set_prev_week_day(saturday, ISO_FRIDAY, iso=True)
   >>> print(prev_friday)
   2016-07-01 21:49:12
   >>> prev_friday = set_prev_week_day(saturday, FRIDAY, iso=False)
   >>> print(prev_friday)
   2016-07-01 21:49:12
