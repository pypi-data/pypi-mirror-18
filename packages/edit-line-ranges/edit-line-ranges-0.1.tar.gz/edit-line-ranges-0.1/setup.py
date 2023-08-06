#!/usr/bin/env python

from setuptools import setup

version = '0.1'

setup(name='edit-line-ranges',
      version=version,
      description='bulk change multiple lines in a text file',
      author='Davide Olianas',
      author_email='ubuntupk@gmail.com',
      url='https://github.com/davethecipo/edit-line-ranges',
      download_url='https://github.com/davethecipo/edit-line-ranges/tarball/0.1',
      packages=['lineranges'],
      entry_points={
            'console_scripts': [
                  'lineranges=lineranges.cli:main']
      },
      extras_require={
          'dev': [ 'Sphinx', 'pytest' ]
      }
     )
