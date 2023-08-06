# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ItunesLibrarian',
    version='1.0.3',
    description='',
    long_description=long_description,
    url='',
    author='Giacomo Rossetto',
    author_email='jackyman_cs4@live.it',
    license='MIT',

    classifiers=[
    ],

    # keywords='sample setuptools development',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    data_files=[('.', ['README.md'])],

    # py_modules=["my_module"],
    # install_requires=['peppercorn'],
    # extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },
    # package_data={
    #    'sample': ['package_data.dat'],
    # },
    entry_points={
       'console_scripts': [
           'ituneslibrarian=__main__',
       ],
    },
)
