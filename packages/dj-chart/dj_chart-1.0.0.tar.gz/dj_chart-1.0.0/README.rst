=============================
dj_chart
=============================

.. image:: https://badge.fury.io/py/dj_chart.png
    :target: https://badge.fury.io/py/dj_chart

The goal of dj_chart is generate charts with the awesome `Chart.js <http://www.chartjs.org/>`_ library.


Requirements
------------

::

    Django 1.9

Quickstart
----------

Install dj_auth::

    pip install dj_chart

Put dj_auth into your INSTALLED_APPS at settings module::

    INSTALLED_APPS = (
       ...
       'dj_chart',
    )

    TEMPLATES = [
        {'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'DIRS': (your dirs, ),
         'APP_DIRS': True,
         'OPTIONS': { },
         },
    ]

========
Features
========


ChartMixin
---------------------

You can use this Mixin for example with a Templateview or also ListView::

    from django.views.generic import TemplateView

    from dj_chart.views import ChartMixin

    from .models import Fruits

    class YourView(ChartMixin, Templateview):

        chart_title_show = True
        chart_title = u"Your Chart Title"
        chart_types_available = [PIE, DOUGHNUT]
        show_grid = False

        def get_chart_data(self):
            # populate self.chart_data
            # Apples
            self.chart_data['labels'].append("Apple")
            self.chart_data['datasets'][0]['backgroundColor'].append("rgb(0,148,63)")
            self.chart_data['datasets'][0]['data'].append(Fruits.filter(fruit_type=1).count())
            # Pear
            self.chart_data['labels'].append(Pear")
            self.chart_data['datasets'][0]['backgroundColor'].append("rgb(222,6,19)")
            self.chart_data['datasets'][0]['data'].append(Fruits.filter(fruit_type=2).count())
            # Banana
            self.chart_data['labels'].append("Banana")
            self.chart_data['datasets'][0]['backgroundColor'].append("rgb(187,187,187)")
            self.chart_data['datasets'][0]['data'].append(Fruits.filter(fruit_type=3).count())

        def get_context_data(self, **kwargs):
            context = super(YourView, self).get_context_data(**kwargs)
            context = self.set_chart_context(context)
            return context

Example with Dates on the x-axis::

    from django.db import models
    from django.views.generic import TemplateView

    from dj_chart.constants import MONTH
    from dj_chart.views import ChartMixin

    class Category(models.Model):
        description models.CharField(max_length=100, verbose_name='Decscription')

    class Person(models.Model):
        first_name = models.CharField(max_length=100, verbose_name='Firstname')
        last_name = models.CharField(max_length=100, verbose_name='Lastname')
        birthday = models.DateField(verbose_name=_(u'Birthday'))
        category = models.ForeignKey(Category, verbose_name=_(u'Category'))

    class ChartPie(ChartMixin, TemplateView):

        chart_title_show = True
        chart_title = u"My Chart"
        chart_types_available = [PIE, DOUGHNUT, BAR]
        show_grid = False
        x_axis = MONTH
        steps = 6

        def get_chart_data(self):
            if self.queryset:
                self.set_labels_and_filter_values_for_xaxes(steps=self.steps, type=self.x_axis)
                
                for label in self.chart_data['labels']:
                    self.label_urls[label] = {}
                self.chart_data['datasets'] = []
                for record in self.queryset:
                    qs = Person.objects.filter(category=record)
                    for i in range(1, len(self.filter_values)):
                        data.append(qs.filter(birthday__gte=self.filter_values[i - 1], birthday__lt=self.filter_values[i]).count())
                        self.label_urls["%s" % self.chart_data['labels'][i]]["%s" % record.description] = {"url": "%s" % reverse('your-url')}

        def get_context_data(self, **kwargs):
            context = super(ChartPie, self).get_context_data(**kwargs)
            self.queryset = Category.objects.all()
            context = self.write_chart_to_context(context)
            return context

====
Todo
====

* Python 3

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ coverage run --source=dj_auth runtests.py && coverage html


Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
