from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-themeUrbanOpus',
	version=version,
	description="This serves to override default ckan front-end components with Urban Opus theme.",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='',
	author_email='',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.themeUrbanOpus'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	themeUrbanOpus=ckanext.themeUrbanOpus.plugin:UrbanOpusThemePlugin

	""",
)
