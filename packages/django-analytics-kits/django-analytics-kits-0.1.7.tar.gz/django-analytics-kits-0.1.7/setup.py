import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-analytics-kits',
    version='0.1.7',
    packages=find_packages(),
    include_package_data=True,
    license='New BSD',
    description='A Django app to get analytics data from Google Analytics and save them in other django app models',
    long_description=README,
    url='https://github.com/smallmedia/django-analytics-kits',
    author='SmallMediaLab',
    author_email='lab@smallmedia.org.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'PyNaCl',
        'google-api-python-client',
        'mock'
    ],
)
