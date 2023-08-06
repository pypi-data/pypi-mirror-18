"""A DeepDiff based structured-data diff utility.

See:
https://gitlab.com/Rtzq0/structurediff
https://github.com/seperman/deepdiff
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='structurediff',
    version='1.0',
    description='structurediff is a diff utility for structured data files',
    long_description=long_description,
    url='https://gitlab.com/Rtzq0/structurediff',
    author='Jason Ritzke (@Rtzq0)',
    author_email='jasonritzke@4loopz.com',
    license='AGPLv3+',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Affero General Public License v3 or \
later (AGPLv3+)',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='DeepDiff YAML JSON diff',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['pyyaml', 'pygments', 'deepdiff', 'termcolor'],

    entry_points={
        'console_scripts': [
            'structurediff=structurediff.cli:main',
        ],
    },
)
