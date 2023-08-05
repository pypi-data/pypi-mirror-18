#!/usr/bin/env python
"""
uModbus is a pure Python implementation of the Modbus protocol with support
for Python 2.7, 3.3, 3.4 and 3.5.

"""
import os
from setuptools import setup

cwd = os.path.dirname(os.path.abspath(__name__))

long_description = open(os.path.join(cwd, 'README.rst'), 'r').read()

setup(name='uModbus',
      version='0.8.1',
      author='Auke Willem Oosterhoff',
      author_email='oosterhoff@baopt.nl',
      description='Implementation of the Modbus protocol in pure Python.',
      url='https://github.com/AdvancedClimateSystems/umodbus/',
      long_description=long_description,
      license='MPL',
      packages=[
          'umodbus',
          'umodbus.client',
          'umodbus.client.serial',
          'umodbus.server',
          'umodbus.server.serial',
      ],
      install_requires=[
          'pyserial~=3.2.1',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Embedded Systems',
      ])
