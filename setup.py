import sys
from setuptools import setup, find_packages
from distutils.extension import Extension
import site
try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

BASEDIR = [x for x in sys.path if 'site-package' in x][0]
INCLUDE_DIRS = [BASEDIR + '/lxml', BASEDIR + '/lxml/includes']
if use_cython:
    ext_modules.append(Extension(
        "pydepta.trees_cython",
        ['pydepta/trees_cython.pyx'],
        include_dirs=INCLUDE_DIRS
    ))
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules.append(Extension(
        "pydepta.trees_cython",
        ['pydepta/trees_cython.c'],
        include_dirs=INCLUDE_DIRS
    ))

setup(name='pydepta',
      version='0.2',
      description="A Python implementation of DEPTA",
      long_description=("A Python implementation of DEPTA (Data Extraction "
                        "with Partial Tree Alignment)"),
      author="Terry Peng",
      author_email="pengtaoo@gmail.com",
      install_requires=['w3lib', 'scrapely'],
      packages=find_packages(),
      cmdclass=cmdclass,
      ext_modules=ext_modules
)
