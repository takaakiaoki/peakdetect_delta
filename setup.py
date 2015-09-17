import sys
import os
from setuptools import setup, find_packages

ver_file = os.path.join(os.path.dirname(__file__), 'iontof', 'version.py')
vars = {}
exec(open(ver_file).read(), vars)

setup(name='peakdetect_delta',
      version=vars['__version__'],
      description='find positive splike-like peaks, using Delta_raise and Delta_fall thresholds.',
      author="Takaaki AOKI",
      author_email='aoki.takaaki@gmail.com',
      download_url='not yet',
      packages=find_packages(),
      package_data={},
      scripts=[],
      long_description=open('README.rst').read(),
      options={},
      classifiers = [
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.4",
          "License :: OSI Approved :: MIT License",
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Operating System :: OS Independent"])
