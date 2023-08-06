"""Project setup file."""
from setuptools import find_packages, setup

setup(name='quick_debug',
      version='0.0.3',
      description='Quick and simple debugging for Python scripts.',
      author='Nitish Reddy Koripalli',
      author_email='nitish.k.reddy@gmail.com',
      url='https://github.com/nitred/quick_debug',
      download_url='https://github.com/nitred/quick_debug/master.tar.gz',
      license='MIT',
      install_requires=['future', 'requests', 'requests-futures'],
      packages=find_packages())
