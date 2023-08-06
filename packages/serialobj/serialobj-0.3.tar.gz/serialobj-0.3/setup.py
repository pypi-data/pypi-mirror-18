from sys import version_info as pyversion
from setuptools import setup

py_version = (pyversion.major, pyversion.minor)

setup(
    name='serialobj',
    version='0.3',
    description='A library to define serializable classes.',
    author='Arnaud Calmettes',
    author_email='arnaud.calmettes@scality.com',
    packages=['serialobj'],
    install_requires=(
        ['chainmap', 'six'] if py_version < (3, 3)
        else ['six']),
)
