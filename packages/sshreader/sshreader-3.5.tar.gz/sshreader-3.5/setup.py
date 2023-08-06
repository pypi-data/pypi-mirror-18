#!/usr/bin/env python2
# coding=utf-8
"""Setup file for sshreader module"""

from setuptools import setup

setup(name='sshreader',
      version='3.5',
      description='Multi-threading/processing wrapper for Paramiko',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='http://pydoc.jacomputing.net/sshreader/',
      packages=['sshreader'],
      include_package_data=True,
      scripts=['bin/pydsh'],
      license='GNU Lesser General Public License v3 or later (LGPLv3+)',
      install_requires=['paramiko==2.0.2',
                        'future==0.16.0',
                        'progressbar2==3.11.0',
                        'python-hostlist==1.16',
                        'click==6.6'
                        ],
      platforms=['Linux', 'Mac OS X'],
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      )
