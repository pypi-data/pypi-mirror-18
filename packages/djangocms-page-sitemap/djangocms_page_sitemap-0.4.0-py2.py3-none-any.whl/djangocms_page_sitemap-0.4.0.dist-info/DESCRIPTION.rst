======================
djangocms-page-sitemap
======================

.. image:: https://img.shields.io/pypi/v/djangocms-page-sitemap.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-sitemap
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-page-sitemap.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-sitemap
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-page-sitemap.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-sitemap
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-page-sitemap.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-page-sitemap
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-page-sitemap/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-page-sitemap?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-page-sitemap/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-page-sitemap
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-page-sitemap/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-page-sitemap
   :alt: Code Climate

django CMS page extension to handle sitemap customization

Support Python version:

* Python 2.7, 3.3, 3.4, 3.5

Supported Django versions:

* Django 1.8, 1.9

Supported django CMS versions:

* django CMS 3.2+


Features
--------

* Support for changefreq and priority customisation per-page
* Option to exclude a page from the Sitemap
* Values are cached
* django CMS toolbar integration


Quickstart
----------

* Install djangocms-page-sitemap::

    pip install djangocms-page-sitemap

* Add to ``INSTALLED_APPS`` with ``django.contrib.sitemaps``::

    INSTALLED_APPS = [
        ...
        'django.contrib.sitemaps',
        'djangocms_page_sitemap',
    ]

* Add to the urlconf, eventually removing django CMS sitemap::

    from djangocms_page_sitemap.sitemap import ExtendedSitemap

    urlpatterns = patterns('',
        ...
        url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': ExtendedSitemap}}),
    )

Usage
-----

After installing as above, you will be able to tune the sitemap setting for each page.

A new menu item ``Sitemap properties`` will be available in the page toolbar.

Settings
--------

* PAGE_SITEMAP_CHANGEFREQ_LIST: List of frequency changes
* PAGE_SITEMAP_DEFAULT_CHANGEFREQ: Default changefrequency (default: django CMS value -monthly-)
* PAGE_SITEMAP_CACHE_DURATION: Cache duration: same as django CMS menu cache)




History
-------

0.4.0 (2016-10-26)
++++++++++++++++++

* Drop compatibility with django CMS 3.1 and below, Django 1.7 and below

0.3.1 (2015-10-18)
++++++++++++++++++

* Improve defaults

0.3.0 (2015-10-18)
++++++++++++++++++

* Add Python 3.5
* Add option to exclude page from sitemap

0.2.0 (2015-08-15)
++++++++++++++++++

* Update to support django CMS 3.1
* Drop support for Django 1.4, 1.5
* Add support for Django 1.8

0.1.0 (2014-08-26)
++++++++++++++++++

* Initial version.


