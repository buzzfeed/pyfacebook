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
    version='1.1.5',
    author='Jeff Revesz and Andrew Kelleher',
    author_email='jeff.revesz@buzzfeed.com',
    packages=find_packages(),
    test_suite='test',
    install_requires=[
        'nose==1.3.0',
        'BeautifulSoup==3.2.1',
        'Fabric==1.5.1',
        'pytz==2013b',
        'python-dateutil==2.1',
        'tinymodel==0.1.4',
        'requests==1.2.3',
        'inflection==0.2.0',
        'caliendo==v2.0.5',
        'simplejson'
    ],
    dependency_links=[
        'https://github.com/buzzfeed/tinymodel/tarball/0.1.4#egg=tinymodel-0.1.4',
        'https://github.com/buzzfeed/caliendo/tarball/v2.0.5#egg=caliendo-v2.0.5'
    ]
)
