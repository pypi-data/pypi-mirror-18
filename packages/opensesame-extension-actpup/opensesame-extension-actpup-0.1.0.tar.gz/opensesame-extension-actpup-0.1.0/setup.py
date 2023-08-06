#!/usr/bin/env python
# coding=utf-8

"""
This file is part of ActPup.

ActPup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ActPup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ActPup.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import glob
from setuptools import setup

def files(path):
	l = [fname for fname in glob.glob(path) if os.path.isfile(fname) \
		and not fname.endswith('.pyc')]
	print(l)
	return l


def data_files():

	return [
		("share/opensesame_extensions/actpup",
			files("opensesame_extensions/actpup/*")),
		("share/opensesame_extensions/actpup/_actpup",
			files("opensesame_extensions/actpup/_actpup/*")),		
		]

setup(
	name="opensesame-extension-actpup",
	version="0.1.0",
	description="Participate in ActPup, a vision-science experiment",
	author="Sebastiaan Mathot",
	author_email="s.mathot@cogsci.nl",
	url="https://www.cogsci.nl/smathot",
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	include_package_data=False,
	packages = [],
	data_files=data_files()
	)
