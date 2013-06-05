from distutils.core import setup
from setuptools import find_packages

setup(name = 'edxdataanalytic', 
      version = '0.0',
      author="Piotr Mitros", 
      package_dir={"edxdataanalytic":"."},
      packages=["edxdataanalytic"], 
      license = "AGPLv3, see LICENSE.txt")
