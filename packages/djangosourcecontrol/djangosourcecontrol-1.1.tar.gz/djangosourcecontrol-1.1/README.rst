=====
DjangoSourceControl
=====

DjangoSourceControl is a simple Django app to create Web-based Python files and projects.
For each project, users can add, update, and create python projects, files, and versions.

Note: Django source control has a unit test suite which can be ran by 'python manage.py test' to run the repo and api authentication tests.

Quick start
-----------

1. Add "djangosourcecontrol" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangosourcecontrol',
    ]

2. Include the djangosourcecontrol URLconf in your project urls.py like this::

    url(r'^djangosourcecontrol/', include('djangosourcecontrol.urls')),

3. Run `python manage.py migrate` to create the djangosourcecontrol models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to assign the can_add_project, and/or the can_run_project to user.

5. Visit http://127.0.0.1:8000/djangosourcecontrol/ to start creating projects.

