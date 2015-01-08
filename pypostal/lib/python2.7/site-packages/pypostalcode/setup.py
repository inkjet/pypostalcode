from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pypostalcode',
      version=version,
      description="Radius searches on Canadian postal codes, location data",
      long_description=open("README.txt").read() + '\n\n' + open('CHANGES.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Canada postal code code distance',
      author='Scott Rodkey',
      author_email='rodkeyscott@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'pysqlite'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
