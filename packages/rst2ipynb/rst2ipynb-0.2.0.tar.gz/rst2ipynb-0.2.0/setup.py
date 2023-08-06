## -*- encoding: utf-8 -*-
"""
reST to Jupyter notebook converter
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rst2ipynb',
    version='0.2.0',
    description='A reST to Jupyter notebook converter',
    long_description=long_description,
    url='https://github.com/nthiery/rst-to-ipynb',
    author='Scott Sievert, Nicolas M. Thiéry',
    author_email='nthiery@users.sf.net',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    scripts=["rst2ipynb", "rst2ipynb-sageblock-filter"],
    install_requires=['notedown', 'pandocfilters'],
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest'],
)
