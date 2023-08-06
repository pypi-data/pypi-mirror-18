# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='PyKyu',
      version=open('VERSION').read().strip(),
      packages=['pykyu'],
      url='https://bitbucket.org/creeerio/pykyu',

      author='Nils',
      author_email='nils@creeer.io',
      license='MIT',

      description='Process queueing; declarative, configurable.',

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
