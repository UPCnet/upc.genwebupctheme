from setuptools import setup, find_packages
import os

version = '3.3.2'

setup(name='upc.genwebupctheme',
      version=version,
      description="Paquet de sabors de Genweb UPC",
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
      )

