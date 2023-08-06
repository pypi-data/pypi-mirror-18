#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='picas',
      version='0.2.10',
      description='Python client using CouchDB as a token pool server.',
      author='Jan Bot,Joris Borgdorff',
      author_email='helpdesk@surfsara.nl',
      url='https://github.com/sara-nl/picasclient',
      download_url='https://github.com/sara-nl/picasclient/tarball/0.2.10',
      packages=['picas'],
      install_requires=['couchdb'],
      license="MIT",
      extras_require={
          'test': ['flake8', 'nose'],
      },
      classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        ]
      )
