#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2013-2016, Philippe Bordron <philippe.bordron@gmail.com>
#
# This file is part of sgs-utils.
#
# sgs-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sgs-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
# along with sgs-utils.  If not, see <http://www.gnu.org/licenses/>



from __future__ import absolute_import, print_function

import io
import re
import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='sgs-utils',
    version='0.53',
    summary='sgs-utils is a collection of python libraries that allows to manipulate SGS file, especially thoses related to shogen.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python'
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Unix',
    ],
    url='https://github.com/pbordron/sgs-utils',
    keywords='bioinformatics shogen SGS',
    author='Philippe Bordron',
    author_email='philippe.bordron+sgs@gmail.com',
    license='LGPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("*.py")],
    # bash scripts will be removed in the future
    scripts = [
        'src/sgs_utils/sgs-utils.py',
        'src/sgs_utils/shogen_queries.py',
        'src/sgs_utils/shogen2tab.py',
        'src/sgs_utils/two_columns_dict_extractor.sh',
        'src/sgs_utils/sgs_filter.sh',
        'src/sgs_utils/RGG_launcher.sh',
        'src/sgs_utils/shogen_queries.sh',
        'src/sgs_utils/SGS_filter_launcher.sh',
        'src/sgs_utils/Shogen_launcher.sh',
    ],
    install_requires=[
          'biopython',
          'networkx',
          'shogen',
          'python-libsbml>=5.12.0',
      ],
    zip_safe=False)
