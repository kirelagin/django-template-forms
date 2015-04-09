`django-template-forms` -- easy forms for [Django](http://www.djangoproject.com/)
========================================================

`django-orderedmodel` lets you design simple but pretty-looking forms
using Django templating system. Creating a new form is as easy as
adding a plaintext file to a folder in your project. This means
that _anyone_ can add forms, since Django template language
is very simple.


How to use
-------------

There are a few simple steps to follow to make your models orderable:

1. Install `django-template-forms` using your favourite way of installing Django packages.
3. Add `'template_forms'` to `INSTALLED_APPS` in your `settings.py`.
4. Instantiate `template_forms.FormsEngine` in your view.
5. Call `.get_form(template_name)` on the engine.
6. Render it using your favourite way of rendering templates.
7. Enjoy!


Example
-------

Use something like this in your view.

**views.py**:

```python
from django.http import Http404
from django.template.base import TemplateDoesNotExist
from django.template.response import TemplateResponse

from template_forms import FormsEngine


def test(request, name):
    forms_engine = FormsEngine('tests')

    try:
        t = forms_engine.get_form(name + '.html')
    except TemplateDoesNotExist:
        raise Http404


    context = {'something': 'just in case',
              }

    return TemplateResponse(request, t, context)
```

This will use Django’s `app_directories.Loader` to look for the template
called `name + '.html'` in the `tests` subdirectory of all the installed applications.


**tests/first.html**:

```HTML+Django
{% extends 'test.html' %}

{% block questions %}

  <p class="lead">
    Please, answer the following questions.
  </p>

  <p>
    Two plus two equals {% gap four | 4 %}. Thee plus three equals {% gap six | 6 %}.
  </p>

  <p>
    The last name of the president of the US is {% gap_case Obama %} (case sensitive!).
  </p>

{% endblock questions %}
```

The new tag is `{% gap %}` which creates a “gap” in the page to be filled in. As you can see
it knows the correct answers, so it also implements all the checking logic (we’ll see it in a minute).
Furthermore, it has a twin—`{% gap_case %}` which (surprise!) doesn’t ignore case.

You are free to use all the normal template tags and filters. Tags that interact with
template loading (e.g. `{% extends %}`) will load templates normally, respecting
your basic settings (i.e., likely, looking in `templates` directories, not `tests`).

The base template might look like this:

**templates/test.html**:

```HTML+Django
<!DOCTYPE html>
<html>
  <head>
    <title>Test</title>
  </head>

  <body>
    <form method="post">
      {% block questions %}{% endblock %}

      {% csrf_token %}

      {% if form_valid %}
        Congratulations!
      {% else %}
        <button type="submit">Check</button>
      {% endif %}
    </form>
  </body>
</html>
```

As I said, checking of the inputs is already implemented for you. First of all,
if all the values are correct, `form_valid` will be set to `True`. Individual
text controls get the `gap-valid` class if the answer is right and `gap-invalid` if
it is not (and if the control is not empty).

With a little bit of CSS magic you will be able to get some nice results:

![Empty form](https://raw.githubusercontent.com/kirelagin/django-template-forms/gh-pages/django_gaps.png)
![Filled form](https://raw.githubusercontent.com/kirelagin/django-template-forms/gh-pages/django_gaps_filled.png)

See? Beautiful and simple. You have to create just one view consisting of ten lines and suddenly
anyone can add forms to your website by simply putting templates into the `surveys` directory.


Django versions
---------------

It works starting with Django 1.8. Yes, they added some cool stuff I used heavily.


Python 3
--------

Of course. And Python 2 too (I hope).
