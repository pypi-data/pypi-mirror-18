
=====
Django translation server
=====

Django translation server is a simple Django app to manage the project translations.


Requirements
-----------

Django REST framework - http://www.django-rest-framework.org/
django-filter
django-modeltranslation - http://django-modeltranslation.readthedocs.io/en/latest/installation.html#using-pip

Quick start
-----------

1. Add "translation_server" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'translation_server',
    ]

2. Include the Translation Server URLconf in your project urls.py like this::

    from translation_server import views as translation_server_views

    router = routers.DefaultRouter()
    router.register(r'translation', translation_server_views.TranslationViewSet)
    router.register(r'translation_type', translation_server_views.TranslationTypeViewSet)

    url(r'^api/last_translation_tag/(?P<tag>\w+)[/]?$', translation_server_views.LastTranslationTagView.as_view(), name='get_last_translation_tag'),


3. Run `python manage.py makemigrations` and `python manage.py migrate` to create the Translation models, and load the initial data.

4. Start the development server and visit http://127.0.0.1:8000/admin/ to create a translation (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/translation/ to view all translations

6. Run `python manage.py translate` to apply the basic translations for en-US and pt-BR