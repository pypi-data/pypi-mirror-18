"""IPyMOL: View and control your PyMOL sessions from the IPython Notebook"""
import sys
from setuptools import setup, find_packages
from ipymol import __name__, __version__

NAME = __name__
VERSION = __version__


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

# if we are running on python 3, enable 2to3 and
# let it use the custom fixers from the custom_fixers
# package.
extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

setup(
    name=NAME,
    version=VERSION,
    description=('IPyMOL allows you to control PyMOL sessions via IPython.'),
    long_description = read('README.rst'),
    platforms = (
        "Windows", "Linux", "Mac OS-X", "Unix",
    ),
    keywords = 'ipython notebook pymol protein molecular visualization',
    author="Carlos Xavier Hernandez",
    author_email="cxh@stanford.edu",
    url = 'https://github.com/cxhernandez/%s' % NAME,
    download_url = 'https://github.com/cxhernandez/%s/tarball/master' % NAME,
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    package_data = {
        '': ['README.rst',
             'requirements.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    **extra
)
