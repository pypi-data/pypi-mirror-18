from sys import version_info as pyversion
from setuptools import setup

py_version = (pyversion.major, pyversion.minor)

setup(
    name='serialobj',
    version='0.5',
    description='A library to define serializable classes.',
    author='Arnaud Calmettes',
    author_email='arnaud.calmettes@scality.com',
    url='http://bitbucket.org/scality/serialobj',
    packages=['serialobj'],
    long_description=open('README.rst').read(),
    install_requires=(
        ['chainmap', 'six'] if py_version < (3, 3)
        else ['six']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
