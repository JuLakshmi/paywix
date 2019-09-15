#!/usr/bin/pythoni

from setuptools import setup
from os import path

p = path.abspath(path.dirname(__file__))
with open(path.join(p, 'README.rst')) as f:
    README = f.read()

setup(
    name='paywix',
    version='1',
    description='Multipayment gateway wrapper for Django',
    long_description=README,
    long_description_content_type='text/markdown',

    install_requires=[
        "django"
    ],
    url='https://github.com/renjithsraj/paywix',
    maintainer='Renjith S Raj',
    maintainer_email='renjithsraj@live.com',
    download_url='',

    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Framework :: Django :: 2.2',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development'
    ],
)
