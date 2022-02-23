# django-searchable-select

A better and faster multiple selection widget with suggestions for Django.

## This project is looking for maintainers!

Please open an issue to request write access.

# What is this?

This plugin provides a replacement for standard multi-choice select on Django admin pages.

You can use this as custom widget for `ManyToManyField`.

# Features

  - Filtering is performed on server side and thus significantly improves performance.
  - Uses `Twitter Typeahead` to provide suggestion completion.
  - Works **great** with ManyToMany fields that can be chosen from thousands of thousands of choices, e. g. `User - City` relations.

### Before

![Before](https://habrastorage.org/files/dd9/f17/87e/dd9f1787e0dd4e05826fdde08e270609.png)

### After

![Before](https://habrastorage.org/files/db2/c87/460/db2c87460992470e9d8e19da307c169d.png)

# Installation

1. Install `django-searchable-select`.

    ```sh
    $ pip install django-searchable-select
    ```

2. Add 'searchableselect' to your settings.

    ```python
    # settings.py

    INSTALLED_APPS = (
        # ...
        'searchableselect',
        # ...
    )
    ```

3. Add URL pattern required for the suggesting engine to your root `urls.py`.

    ```python
    # urls.py

    urlpatterns = patterns(
        '',
        # ...
        re_path('^searchableselect/', include('searchableselect.urls')),
        # ...
    )
    ```

4. Use the widget in your model admin class:

    ```python
    from django import models, forms
    from searchableselect.widgets import SearchableSelect
    from models import Traveler

    class TravelerForm(forms.ModelForm):
        class Meta:
            model = Traveler
            exclude = ()
            widgets = {
                'cities_visited': SearchableSelect(model='cities.City', search_field='name', many=True, limit=10)
            }


    class TravelerAdmin(admin.ModelAdmin):
        form = TravelerForm

    admin.site.register(Traveler, TravelerAdmin)
    ```

    Remember to **always** initialize `SearchableSelect` with three keyword arguments: `model`, `search_field` and `many`.

    - `model` is the string in form `APP_NAME.MODEL_NAME` representing your model in the project, e. g. 'cities.City'
    - `search_field` is the field within model that will be used to perform filtering, e. g. 'name'
    - `many` must be `True` for `ManyToManyField` and `False` for `ForeignKey`.
    - `limit` (optional) specifies the maximum count of entries to retrieve.

# Example app

Just run the project from `example` directory, head to http://127.0.0.1:8000, login as `admin`/`admin` and try adding Cats!

# Supported versions

  - Python 3.5+ and Django 2.2, 3.0, 3.2 or 4.0.

# Testing

In order to support multiple Django and Python versions we use:

  - `py.test` - test runner
  - `tox` - handy tool to test app with different versions of Pythons & libraries
  - `selenium`
  - `coverage`

Install them via `pip install -r requirements/dev.txt`

To test things in specific environment, run the following commands:

```sh
# Clear previous coverage data.
coverage erase

# This command can be ran multiple times.
tox -e <python_ver>-<django_ver>
# Some python_ver values: `py3.5`, `py3.10`
# Some django_ver values: `dj2.2`, 'dj4.0'
# Values can be comma-separated, e. g. `-e py3.5-dj2.2,py3.10-dj3.2,py3.10-dj4.0`
# If you omit `-e ...` parameter, all environments will be tests.
# Also - not problems with running this within a virtualenv.
# Check tox.ini for these values.

# Run this once all tests passed on all environment.
coverage combine

# Render HTML with coverage info.
coverage html
# ...or simply display % of covered SLOC for each file.
coverage report
```

To add a new Django version for testing, add it into `tox.ini`.

Why do we need `tox` and `coverage combine`? Because different versions of Python & libraries lead to different code execution: for example, consider this code:

```python
import sys
if sys.version_info.major == 2:
    foo = 'spam'  # Not covered in Python 3.x, leads to coverage < 100%
else:
    foo = 'eggs'  # Not covered in Python 2.x, leads to coverage < 100%
```

Using `tox` and `coverage combine` we're able to "merge" coverage info from across different environments.

# Known issues

  - Not tested with empty fields.
  - Tests sometimes fail randomly due to some Selenium timeout issue. Weird.

# Contributing

I'm looking forward to bug reports and any kind of contribution.

# License

You are free to use this where you want as long as you keep the author reference.
Please see LICENSE for more info.
