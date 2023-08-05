#from setuptools import setup
import os
import re
from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

def version():
    return re.findall(r".*__version__ = \'(.*)\'.*", read('bin/loggr'))[0]

def readme():
    return read('README.md')

setup(name='loggr',
      license='MIT License',
      author='Matt Bierbaum',
      url='https://github.com/mattbierbaum/loggr',
      version=version(),

      packages=['loggr'],
      install_requires=["tornado>=4.3"],
      scripts=['bin/loggr'],

      description='Remote log platform with easy integration into Python logging.',
      long_description=readme(),
)
