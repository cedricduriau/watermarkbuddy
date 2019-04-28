# stdlib modules
from setuptools import setup, find_packages


setup(name="watermarkbuddy",
      version="1.0.0",
      description="Watermarking tool using ffmpeg.",
      license="MIT",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/watermarkbuddy",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/watermarkbuddy", "bin/watermarkbuddycmd"])
