django-path2css
===============

:author: Keryn Knight
:version: 0.2.0

.. |travis_stable| image:: https://travis-ci.org/kezabelle/django-path2css.svg?branch=0.2.0
  :target: https://travis-ci.org/kezabelle/django-path2css

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-path2css.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-path2css

==============  ======
Release         Status
==============  ======
stable (0.2.0)  |travis_stable|
master          |travis_master|
==============  ======


What it does
------------

A small Django package for rendering a request's URL as a series of CSS class names,
such that one can target sections or individual parts of a site using CSS only.

It can also look for path specific CSS files, and output those for you.

Generating class names
^^^^^^^^^^^^^^^^^^^^^^

For example, say all your blog posts are under ``/blog/``, then you might do::

  {% load path2css %}
  <body class="{% path2css request.path %}">...</body>

Subsequently, going to ``/blog/``, ``/blog/post/``, ``/blog/post/comments/`` etc
will all have the ``blog`` CSS class added to the body, which you could then use::

  body.blog {...}
  body.blog-post {...}
  body.blog-post-comments {...}

Note that blog-post-comments, being the deepest namespace reached, would also have
the ``blog`` and ``blog-post`` classes added.

Request specific CSS files
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have a URL like ``/blog/post/4/``, using the ``{% css4path %}`` tag
allows you to load hierarchy specific CSS files::

  {% load path2css %}
  <head>
  {% css4path request.path %}

might output the following::

  <link href="/static/css/blog.css" rel="stylesheet" type="text/css" />
  <link href="/static/css/blog-post-4.css" rel="stylesheet" type="text/css" />

...if those files exist in one of your static directories. In the above example,
I've not created a ``blog-post.css`` file, so the template tag knows not to
load it for output, because it would be a 404. It should only ever include files
that do exist.

This allows you to compartmentalise your CSS files into separate parts, like
we used to do in the old days when websites were often hand-crafted and different
sections had a different look and feel, or whatever, before the inevitable rise
of CMS made things a little more homogenized.


Installation
------------

It the stable release is on PyPI::

  pip install django-path2css==0.2.0


The templatetags
----------------

In case you're already using the class names that would be generated, ``{% path2css %}``
takes a ``prefix=x`` and/or ``suffix=y`` parameter, so that you can re-namespace things
without clobbering your existing styles::

  {% path2css '/blog/post/' prefix='path-' %}
  {% path2css '/blog/post/' suffix='-area' %}
  {% path2css '/blog/post/' prefix='pre_' suffix='_post' %}

The ``{% css4path %}`` takes the same ``prefix``/``suffix`` parameters, and
also takes an optional ``directory``, whose default value is ``css``

The context processor
---------------------

There's also a context processor which may be used by adding ``path2css.context_processor``
to your existing list. It does the same thing as ``{% path2css %}`` with no
prefix/suffix arguents.


Supported Django versions
-------------------------

The tests are run against Django 1.8 through 1.10, and Python 2.7, 3.3, 3.4 and 3.5.


Roadmap
-------

If I ever have a need for it, a JavaScript equivalent that can consume
window.location.path or whatever ... and potentially bridges to things like
angular, I guess?


The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
