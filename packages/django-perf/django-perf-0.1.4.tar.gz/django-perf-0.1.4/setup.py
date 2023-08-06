import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-perf',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    license='LGPL-3.0',
    description='A simple Django Middleware for sending request data to Perf.',
    long_description=open('README.rst').read(),
    url='https://github.com/perflabs/django-perf',
    author='Jonathan Grana',
    author_email='john@perf.sh',
    classifiers=[],
)
