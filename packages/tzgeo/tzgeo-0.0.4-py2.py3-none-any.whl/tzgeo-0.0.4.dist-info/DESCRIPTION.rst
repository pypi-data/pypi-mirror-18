tzgeo
=====

tzgeo is a library with one simple purpose - to convert a lat/lon to a
timezone - really fast!


Installation
------------
The easiest way to install is using `pip`::

    pip install tzgeo


Usage
-----
Using tzgeo is very simple!

::

    >>> import tzgeo
    >>> tzgeo.tz_lookup(39.888724, -75.107952)
    u'America/New_York'


If the location is invalid, or points at the ocean, `tz_lookup` will return
`None`.


More Information
----------------
More information can be found on the project's `github page`_

.. _`github page`: https://github.com/judy2k/tzgeo


