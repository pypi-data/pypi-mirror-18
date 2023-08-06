SHORTURLS
=========


Install
-------
This package provides some basic short url capabilities. To install:

1. ``pip install https://github.com/OpenTherapeutics/shorturls/archive/master.zip``

2. Add ``'shorturls',`` to your project's INSTALLED_APPS

3. Make sure you have ``django.contrib.sites`` installed and configured in
   your project. Let's assume that the project's domain is configured to be:
   ``example.com``.

4. Optionally add these settings to your project's settings: ::

    SHORTURLS_CODE_LENGTH = 6
    SHORTURLS_PROTOCOL = 'http'

    The default values are shown above.

5. Add ``url(r'^u/', include('shorturls.urls')),`` to your project's urls.

   In the above example, shorturls is "mounted" at the URL "/u/...". Naturally,
   this "mount point" can be anywhere the project requires.

Usage
-----

Let's assume that our project is hosted at "http://example.com/" and that, as
per above, we've attached the shorturls package at "/u/" in the URL patterns.

Register a new URL
~~~~~~~~~~~~~~~~~~

To shorten a URL, simply make a GET request to: ::

    http://example.com/u/register/?url=http://www.google.com/

Or, a POST request to: ::

    http://example.com/u/register/

with a payload of: ::

    url="http://www.google.com/"

This will create a new short url for ``http://www.google.com/`` and return a
shorturl of something like: ::

    http://example.com/u/abc123/


Resolve a URL
~~~~~~~~~~~~~

To resolve/expand/use a shortened URL, simply visit the URL. In this case,
visiting ``http://example.com/u/abc123/`` will result in an HTTP Redirect to the
original URL: ``http://www.google.com/``.
