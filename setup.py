# coding: utf-8

from setuptools import setup

setup(
    name='Gladiator',
    version='0.1-dev',
    url='http://github.com/laco/gladiator',
    license='BSD',
    author='László Andrási',
    author_email='laco@laszloandrasi.com',
    description='Gladiator is (yet another) Validator Framework for Python3',
    long_description=open('README.rst').read() + '\n\n',
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
