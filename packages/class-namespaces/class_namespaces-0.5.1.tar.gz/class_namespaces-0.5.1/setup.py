"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open as c_open
from os import path

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with c_open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='class_namespaces',

    version='0.5.1',

    description='Class Namespaces',
    long_description=LONG_DESCRIPTION,

    url='https://github.com/mwchase/class-namespaces',

    author='Max Woerner Chase',
    author_email='max.chase@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='class namespaces',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    extras_require={
        'test': ['coverage', 'pytest'],
    },
)
