#!/usr/bin/env python

from distutils.core import setup


setup(name='django-template-forms',
      version='2015.04.001',

      description='Easy way to generate simple forms with Django templates',
      long_description='''
          This Django_ app lets you design simple but pretty-looking
          forms. And the most awesome thing is that forms are completely
          described using Django templating language.

          See README_ for more details.

          .. _Django: https://www.djangoproject.com/
          .. _README: https://github.com/kirelagin/django-template-forms/blob/master/README.md
      ''',


      author='Kirill Elagin',
      author_email='kirelagin@gmail.com',

      url='https://github.com/kirelagin/django-template-forms',

      classifiers = ['Development Status :: 5 - Production/Stable',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 3',
                     'Topic :: Software Development :: Libraries',
                    ],
      keywords = ['Django', 'templates', 'forms'],

      packages = ['template_forms'],
     )
