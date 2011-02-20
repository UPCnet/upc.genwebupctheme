# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '4.0b1'

setup(name='upc.genwebupctheme',
      version=version,
      description="Paquet de sabors de Genweb UPC",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='genwebupctheme genwebupc upc tema theme',
      author='PloneTeam@UPCnet',
      author_email='plone.team@upcnet.es',
      url='https://genweb.upc.edu/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
