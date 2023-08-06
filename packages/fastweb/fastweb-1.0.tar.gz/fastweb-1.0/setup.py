# coding:utf8

try:
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

kwargs = {}

version = '1.0'

with open('README.rst') as f:
        kwargs['long_description'] = f.read()

if setuptools is not None:
    install_requires = []
    with open('requirements.txt') as f:
        for require in f:
            install_requires.append(require[:-1])

    kwargs['install_requires'] = install_requires
print kwargs
setup(
    name='fastweb',
    version=version,
    packages=['fastweb'],
    author='OKer',
    description="FastWeb is a Python fast web frame refered by Tornado",
    **kwargs
)
