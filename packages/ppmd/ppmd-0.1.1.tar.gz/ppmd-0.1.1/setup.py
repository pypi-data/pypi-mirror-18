"""
Setup module for ppmd
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
    name='ppmd',
    version='0.1.1',
    description='A tool to convert from PowerPoint OOXML files to Markdown Presentations',
    long_description=long_description,
    url='https://github.com/nathancastle/ppmd',
    author='Nathan C. Castle',
    author_email='nathan.castle@outlook.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],

    # What does your project relate to?
    keywords='powerpoint markdown ooxml converter document',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['click'],
    extras_require={},
    package_data={},
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'ppmd=ppmd:main',
        ],
    },
)
