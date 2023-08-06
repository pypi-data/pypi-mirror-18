import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangosourcecontrol',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    license='gpl-3.0',
    description='A simple Django app to conduct create Web-based Python projects and files. Powered by KnockoutJs and django-rest-framework',
    long_description=README,
    url='https://github.com/kull2222/DjangoSourceControl/',
    author='Daniel J Pepka',
    author_email='pepkad@wsu.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
