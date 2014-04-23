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
    version='1.1.8',
    author='Jeff Revesz and Andrew Kelleher',
    author_email='jeff.revesz@buzzfeed.com',
    packages=find_packages(),
    test_suite='test',
    install_requires=[
        'nose>=1.3.0',
        'BeautifulSoup==3.2.1',
        'Fabric==1.5.1',
        'pytz==2013b',
        'python-dateutil==2.1',
        'requests==1.2.3',
        'inflection==0.2.0',
        'simplejson'
    ],
    dependency_links=[
        'https://github.com/buzzfeed/tinymodel/tarball/0.1.6#egg=tinymodel-0.1.6'
    ]
)
