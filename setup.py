# stdlib modules
import os
import sys
from setuptools import setup
from setuptools import find_packages

# tool modules
f = os.path.abspath(__file__)
package_dir = os.path.join(os.path.dirname(f), "python")
sys.path.insert(0, package_dir)
from watermarkbuddy import __version__  # noqa

requirements_dev = ["flake8", "radon"]
requirements_install = ["PySide2"]


setup(name="watermarkbuddy",
      version=__version__,
      description="Watermarking tool using ffmpeg.",
      license="GPLv3",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/watermarkbuddy",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/watermarkbuddy-cli", "bin/watermarkbuddy-gui"],
      install_requires=requirements_install,
      extras_require={"dev": requirements_dev})
