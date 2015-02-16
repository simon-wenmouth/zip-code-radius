from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zip-code-radius',

    version='0.0.1',

    description='Generate minimum sets of zip codes, based on a radius, that can be used in a series of searches to cover the entire USA',

    long_description=long_description,

    url='https://github.com/simon-wenmouth/zip-code-radius',

    author='Simon Wenmouth',

    license='http://www.apache.org/licenses/LICENSE-2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords=['zip code', 'radius', 'minimum search set'],

    packages=['zip_code_radius'],

    install_requires=['requests'],

)

