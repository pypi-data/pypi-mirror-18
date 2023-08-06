# Copyright (C) Electronic Arts Inc.  All rights reserved.

from setuptools import setup
import muffin

setup(name='MuffinService',
      version=muffin.VERSION,
      description="Muffin is a solution for structured test result reporting",
      packages=['muffin', 'muffin/v2', 'muffin/manage'],
      py_modules=['wsgi', 'manage'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.5',
      ],
      install_requires=[
          'Flask',
          'jsonschema',
          'Flask-Script',
          'fake-factory',
          'jsonpatch',
          'Flask-SQLAlchemy'
      ]
     )
