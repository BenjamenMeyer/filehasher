# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages

REQUIRES = [
	'setuptools >= 1.1.6'
]

DESCRIPTION = 'Recursive Hasher'

ENTRY_POINTS = {
	'console_scripts': [
		'sha1_hasher = filehasher.cmd:main' 
	]
}

setup(
	name='filehasher',
	version='0.1',
	description=DESCRIPTION,
	license='Apache License 2.0',
	url='https://github.com/BenjamenMeyer/filehasher',
	author='Benjamen R. Meyer',
	author_email='bm_witness@yahoo.com',
	install_requires=REQUIRES,
	zip_safe=False,
	entry_points=ENTRY_POINTS,
	packages=find_packages()
)
