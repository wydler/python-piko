#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(name='pikopy',
      version='0.0.5',
      author='Michael Wydler',
      author_email='michael.wydler@gmail.com',
      url='https://github.com/wydler/python-piko',
      download_url='https://github.com/wydler/python-piko',
      description='',
      long_description='',

      packages=find_packages(),
      include_package_data=True,
      package_data={
          '': ['*.txt', '*.rst'],
          'piko': ['data/*.html', 'data/*.css'],
      },
      exclude_package_data={'': ['README.txt']},

      #scripts=['bin/my_program'],

      keywords='python kostal piko inverter',
      license='GPL',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   ],

      # setup_requires = ['python-stdeb', 'fakeroot', 'python-all'],
      install_requires=['setuptools'],
      )
