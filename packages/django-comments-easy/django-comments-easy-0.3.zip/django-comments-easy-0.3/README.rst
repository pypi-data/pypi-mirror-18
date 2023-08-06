Quick start
-----------

1. Add the following to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django.contrib.humanize',
    	'django_commentseasy',
    	'bootstrap3',
    ]

2. Include the django_commentseasy URLconf in your project urls.py like this::

    url(r'^comment/', include('django_commentseasy.urls')),

3. Run `python manage.py migrate` to create the models.

4. Start the development server

