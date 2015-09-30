# coding: utf-8

from setuptools import setup

__version__ = "0.6.8"


def get_version():
    return __version__


def next_version():
    _v = __version__.split('.')
    _v[-1] = str(int(_v[-1]) + 1)
    return '.'.join(_v)


def read_file(f):
    with open(f, 'r') as _file:
        return _file.read()


setup(
    name='Gladiator',
    version=get_version(),
    url='https://github.com/laco/gladiator',
    download_url='https://github.com/laco/gladiator/tarball/' + get_version(),
    license='BSD',
    author='László Andrási',
    author_email='mail@laszloandrasi.com',
    description='Gladiator is a Data Validation Framework for Python3',
    long_description=read_file('README.rst') + '\n\n',
    packages=['gladiator'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
