#!/usr/bin/env python2.7
from setuptools import setup


try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(name="dialectic_pipeline",

      # semantic versioning is a simple way to define versions
      # http://semver.org/
      version="0.2",

      description="Pipeline for augmenting text-fields with automatc, content-specific feedback to improve user generated text quality",
      license="MIT",
      author="Hamed Nilforoshan",
      author_email="hn2284@columbia.edu",
      url="http://github.com/cudbg/Dialectic",
      packages = ['dialectic_pipeline'],
      download_url='https://github.com/cudbg/Dialectic/tarball/0.1',
      include_package_data = True,

      # ensures that pipexample/*.txt is included in the package
      package_data={
        'dialectic_pipeline':['*.txt','*.py']
      },

      # ensures that runexample.py can be run from the command line as a program
      scripts = [
        'bin/run_pipeline.py','bin/test_imports.py'
      ],
      install_requires = [
        'click'
      ],
      keywords= "")