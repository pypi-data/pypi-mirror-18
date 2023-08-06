=====
Django-system-information
=====

Django-system-information is a simple Django app to expose some technical information about your application.

These information will be used by webtool dashboard.epfl.ch who centralizes technical information of EPFL.


Quick start
-----------

1. Add SYSTEM_INFORMATION_APPLICATION_NAME = 'name_of_your_application' to your INSTALLED_APPS settings.py


2. Include the system-information URLconf in your project urls.py like this::

    url(r'^system-information/', include('systeminformation.urls')),


3. Visit http://127.0.0.1:8000/system-information/ to view technical information
