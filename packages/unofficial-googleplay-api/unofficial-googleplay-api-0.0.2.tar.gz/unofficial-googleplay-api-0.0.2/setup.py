from setuptools import setup, find_packages
import os
import sys

_dir = os.path.dirname(os.path.realpath(__file__))

setup(
  name = 'unofficial-googleplay-api',
  packages = find_packages(exclude=["test"]),
  version = '0.0.2',
  description = '',
  author = 'Marco Montagna',
  author_email = 'marcojoemontagna@gmail.com',
  url = 'https://github.com/mmontagna/googleplay-api',
  download_url = 'https://github.com/mmontagna/googleplay-api/archive/v0.0.2.tar.gz',
  keywords = ['googleplay', 'apk', 'android', 'download'],
  classifiers = [],
  install_requires = ['requests','protobuf'],
  entry_points = {
      'console_scripts': ['googleplay-download=googleplay.download:main']
  }
)