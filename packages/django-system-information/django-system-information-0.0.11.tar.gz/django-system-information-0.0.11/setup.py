# coding:utf-8
import os
import systeminformation
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-system-information',
    version=systeminformation.__version__,
    packages=find_packages(),
    include_package_data=True,
    license="LGPLv3",
    description='A simple Django app to expose some technical information about your application',
    long_description=README,
    url='https://charmier@git.epfl.ch/repo/django-system-information.git',
    author='Charmier Grégory',
    author_email='gregory.charmier@epfl.ch',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
