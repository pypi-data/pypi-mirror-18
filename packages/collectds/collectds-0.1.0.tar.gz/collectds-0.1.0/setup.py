#!/usr/bin/env python
#
from setuptools import setup, find_packages

from collectds import __version__ as version

maintainer = 'You-Ming-Yang'
maintainer_email = 'ymyscugs@gmail.com'
author = maintainer
author_email = maintainer_email
description = 'This module references Fuel-LMA and is modified to collect OpenStack service running status.'

long_description = """
=========
Collectds
=========

Introduction
------------

Collectds references Fuel-LMA and is modified to collect OpenStack service running status.


Installation
------------
1. Via pip(recommend)::
	
	pip install collectds

2. Via easy_install::
	
	easy_install collectds

2. From source ::
	
	python setup.py install


"""

install_requires = [
	'MySQL-python>=1.2.5'
]

license = 'LICENSE'

name = 'collectds'
packages = [ 'collectds', ]
platforms = ['linux']
url = ''
download_url = ''
classifiers = [
	'Development Status :: 3 - Alpha',
	'Environment :: OpenStack',
	'Intended Audience :: Developers',
	'License :: OSI Approved :: Apache Software License',
	'Programming Language :: Python :: 2.7',
]

setup(author=author,
	author_email=author_email,
	description=description,
	license=license,
	long_description=long_description,
	install_requires=install_requires,
	maintainer=maintainer,
	name=name,
	packages=find_packages(),
	platforms=platforms,
	url=url,
	download_url=download_url,
	version=version,
	test_suite='test',
	classifiers=classifiers)
