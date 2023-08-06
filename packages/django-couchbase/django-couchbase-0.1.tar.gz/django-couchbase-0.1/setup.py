import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-couchbase',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Django ORM for Couchbase.',
    long_description=README,
    url='https://github.com/aswinkp/django-couchbase/',
    download_url = 'https://github.com/aswinkp/django-couchbase/tarball/0.1',
    author='Aswin Kumar K P',
    author_email='kp.aswinkumar@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
