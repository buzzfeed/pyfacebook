# coding=utf-8
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='pyfacebook',
    version='0.0.1',
    author='Jeff Revesz and Andrew Kelleher',
    author_email = 'jeff.revesz@buzzfeed.com',
    packages=find_packages(),
    test_suite='test',
    requires=['nose', 'pyfb']
)
