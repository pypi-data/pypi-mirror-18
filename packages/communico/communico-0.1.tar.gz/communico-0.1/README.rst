=========
Communico
=========

Communico is a simple Django app for contact forms. 


Quick start
-----------

1. Install "communico" from PyPI:

    `pip install django-admin-honeypot`

2. Add "communico" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'communico',
    ]

3. Add the following email settings to your settings file::

    EMAIL_HOST = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587

4. Include the communico URLconf in your project urls.py like this::

    url(r'^contact/', include('communico.urls', namespace='communico')),

5. Start the development server and visit http://127.0.0.1:8000/contact/
   to view the contacts form.

6. Communico comes with a basic html and no styling, please tweak as needed.