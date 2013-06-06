from distutils.core import setup
from setuptools import find_packages

setup(name = 'video_heatmap', 
      version = '0.0',
      author="Juho Kim",
      author_email="juhokim@edx.org",
      package_dir={"video_heatmap":"."},
      packages=["video_heatmap"], 
      license = "AGPLv3, see LICENSE.txt")
