#from setuptools import setup
from distutils.core import setup

setup(name='tmpr',
      license='MIT License',
      author='Matt Bierbaum',
      version='0.3',

      install_requires=["tornado>=4.3"],
      scripts=['tmpr']
)
