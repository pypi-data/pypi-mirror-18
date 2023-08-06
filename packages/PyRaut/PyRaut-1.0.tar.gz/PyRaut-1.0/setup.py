# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='PyRaut',
      version=open('VERSION').read().strip(),
      packages=['pyraut'],
      url='https://bitbucket.org/creeerio/pyraut',

      author='Nils',
      author_email='nils@creeer.io',
      license='MIT',

      description='Routing; simple, configurable.',
      long_description=open('README.rst').read(),

      classifiers=[
          # 3 - Alpha, 4 - Beta, 5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],

      install_requires=[],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'])
