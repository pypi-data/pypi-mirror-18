# -*- coding: utf-8 -*-
from setuptools import setup


short_description = 'Checks for old string formatting.'


long_description = '{0}\n{1}'.format(
    open('README.rst').read(),
    open('CHANGES.rst').read()
)


setup(
    name='flake8-pep3101',
    version='0.6',
    description=short_description,
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Framework :: Flake8",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ],
    keywords='pep8 pycodestyle flake8 string formatting',
    author='Gil Forcada',
    author_email='gil.gnome@gmail.com',
    url='https://github.com/gforcada/flake8-pep3101',
    license='GPL version 2',
    py_modules=['flake8_pep3101', ],
    include_package_data=True,
    test_suite = 'run_tests',
    zip_safe=False,
    install_requires=[
        'flake8',
    ],
    entry_points={
        'flake8.extension': ['S001 = flake8_pep3101:Flake8Pep3101'],
    },
)
