#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from setuptools import setup

setup(
	# Some general metadata. By convention, a plugin is named:
	# opensesame-plugin-[plugin name]
	name='opensesame-plugin-Pulse_EVT2',
	version='0.0.6',
	description='Send markers through an EVT2 (RUG USB interface)',
	author='Mark Span',
	author_email='m.m.span@rug.nl',
	url='https://github.com/markspan/EVT2',
	# Classifiers used by PyPi if you upload the plugin there
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: Win32 (MS Windows)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	#install_requires=[
	#	'pythonnet'
	#],
	# The important bit that specifies how the plugin files should be installed,
	# so that they are found by OpenSesame. This is a bit different from normal
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files=[
		# First the target folder.
		('share/opensesame_plugins/Pulse_EVT2',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'Pulse_EVT2.md',
			'Pulse_EVT2.png',
			'Pulse_EVT2_large.png',
			'Pulse_EVT2.py',
			'libevt.py',
			'EventExchanger.dll',
			'HidSharp.dll',
			'HidSharp.DeviceHelpers.dll',
			'info.yaml',
			'Example.osexp',
			]
		)]
	)