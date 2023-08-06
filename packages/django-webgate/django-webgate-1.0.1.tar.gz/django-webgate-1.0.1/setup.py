import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-webgate',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    description=('Django Authentication Middleware for WebGate Oracle Access'
                 'Manager.'),
    long_description=README,
    url='https://github.com/boundlessgeo/django-webgate/',
    author='Daniel Berry',
    author_email='dberry@boundlessgeo.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
