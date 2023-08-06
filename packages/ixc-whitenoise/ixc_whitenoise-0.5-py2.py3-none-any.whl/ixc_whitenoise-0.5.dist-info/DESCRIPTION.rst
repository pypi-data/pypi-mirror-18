What is this?
=============

Improvements to `WhiteNoise <https://github.com/evansd/whitenoise/>`__:

-  Serve media as well as static files.
-  Save media with hashed filenames, so they can be cached forever by a
   CDN.
-  Do not crash the ``collectstatic`` management command when a
   referenced file is not found or has an unknown scheme.
-  Add
   `django-pipeline <https://github.com/jazzband/django-pipeline/>`__
   integration.
-  Add support for Django 1.6 via monkey patching.


