#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aleksandra Tarkowska <A(dot)Tarkowska(at)dundee(dot)ac(dot)uk>,
#
# Version: 1.0


import os
import json
from setuptools import setup, find_packages


# Utility function to read the README file. Also support json content
def read_file(fname, content_type=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    p = os.path.join(dir_path, fname)
    with open(p) as f:
        if content_type in ('json',):
            data = json.load(f)
        else:
            data = f.read()
    return data

VERSION = "2.0.1"
DESCRIPTION = "OMERO figure creation app"
AUTHOR = "The Open Microscopy Team"
LICENSE = "AGPLv3"
HOMEPAGE = "https://github.com/ome/omero-figure"

setup(name="omero-figure",
      packages=find_packages(exclude=['ez_setup']),
      version=VERSION,
      description=DESCRIPTION,
      long_description=read_file('README.rst'),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Affero General Public License v3 '
          'or later (AGPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python :: 2',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries :: '
          'Application Frameworks',
          'Topic :: Text Processing :: Markup :: HTML'
      ],  # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      author=AUTHOR,
      author_email='ome-devel@lists.openmicroscopy.org.uk',
      license=LICENSE,
      url=HOMEPAGE,
      download_url='https://github.com/ome/omero-figure/tarball/%s' % VERSION,
      keywords=['OMERO.web', 'figure'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False,
      )
