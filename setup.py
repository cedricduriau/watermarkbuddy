# stdlib modules
import os
from setuptools import setup, find_packages


setup(name="watermarkbuddy",
      version="0.1.0",
      description="Watermarking tool using ffprobe and ffmpeg.",
      license="MIT",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/watermarkbuddy",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/watermarkbuddy", "bin/watermarkbuddycmd"])