# -*- coding: utf-8 -*-
"""Setup for ps.plone.realestatefont package."""

from setuptools import setup, find_packages

version = '0.4'
description = 'Real Estate icon font.'
long_description = ('\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
]))

install_requires = [
    'setuptools',
]

plone_dependencies = [
    'plone.api',
]

test_dependencies = [
    'plone.app.robotframework',
    'plone.app.testing',
    'robotframework-selenium2screenshots',
]


setup(
    name='ps.plone.realestatefont',
    version=version,
    description=description,
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='plone fonts',
    author='Propertyshelf, Inc.',
    author_email='development@propertyshelf.com',
    url='https://github.com/propertyshelf/ps.plone.realestatefont',
    download_url='http://pypi.python.org/pypi/ps.plone.realestatefont',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['ps', 'ps.plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        plone=plone_dependencies,
        test=test_dependencies,
    ),
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
