# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '4.1.11'

setup(name='upc.genwebupctheme',
      version=version,
      description="Paquet de sabors del servei Genweb UPC",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        ],
      keywords='genwebupctheme genwebupc upc tema theme',
      author='PloneTeam@UPCnet',
      author_email='plone.team@upcnet.es',
      url='https://github.com/upcnet/upc.genwebupctheme',
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
