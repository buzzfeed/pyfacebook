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
    version='0.0.4rc2',
    author='Jeff Revesz and Andrew Kelleher',
    author_email='jeff.revesz@buzzfeed.com',
    packages=find_packages(),
    test_suite='test',
    install_requires=[
        'nose==1.2.1',
        'BeautifulSoup==3.2.1',
        'Fabric==1.5.1',
        'pytz==2012h',
        'caliendo==0.2.1'
    ],
    dependency_links=[
        'http://github.com/buzzfeed/caliendo/tarball/v0.2.1#egg=caliendo-0.2.1'
    ]
)
