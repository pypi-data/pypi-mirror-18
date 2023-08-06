import sys
import os
from setuptools import setup

# from createsend.createsend import __version__

setup(name = "vtscreatesend",
      version = '0.0.1',
      description = "fixed version of a library which implements the complete functionality of the Campaign Monitor API.",
      author = "James Dennes",
      author_email = 'jdennes@gmail.com',
      url = "http://campaignmonitor.github.io/createsend-python/",
      license = "MIT",
      keywords = "createsend campaign monitor email",
      packages = ['vtscreatesend'],
      install_requires=[
          'six',
      ],
      package_data = {'vtscreatesend': ['cacert.pem']})
