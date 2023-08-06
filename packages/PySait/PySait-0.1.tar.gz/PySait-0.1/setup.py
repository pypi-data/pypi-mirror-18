# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='PySait',
      version='0.1',
      packages=['pysait'],
      url='https://bitbucket.org/creeerio/pysait',

      author='Nils',
      author_email='nils@creeer.io',
      license='MIT',

      description='Site; compact, fast.',
      long_description=open('README.rst').read(),

      classifiers=[
          # 3 - Alpha, 4 - Beta, 5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],

      install_requires=['Werkzeug'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'])
