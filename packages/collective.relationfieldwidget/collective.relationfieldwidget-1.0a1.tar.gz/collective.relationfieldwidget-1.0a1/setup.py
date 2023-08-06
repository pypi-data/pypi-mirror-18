# -*- coding: utf-8 -*-
"""Installer for the collective.relationfieldwidget package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() +
    '\n' +
    'Contributors\n' +
    '============\n' +
    '\n' +
    open('CONTRIBUTORS.rst').read() +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')


setup(
    name='collective.relationfieldwidget',
    version='1.0a1',
    description="RelationField Widget for Plone 5",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Matt Grant',
    author_email='matt.grant@foodstuffs-si.co.nz',
    url='https://pypi.python.org/pypi/collective.relationfieldwidget',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Acquisition',
        'Products.CMFCore',
        'Products.CMFPlone',
        'plone.app.z3cform'
    ],
    extras_require={
        'tests': [
            'plone.app.testing',
            'plone.browserlayer',
            'plone.testing',
            'zope.contentprovider',
            'zope.publisher',
            'zope.testing',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
