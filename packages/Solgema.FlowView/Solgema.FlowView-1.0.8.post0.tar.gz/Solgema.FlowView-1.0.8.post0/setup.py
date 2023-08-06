from setuptools import setup, find_packages
import os

version = '1.0.8'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])

setup(name='Solgema.FlowView',
      version=version,
      description="Solgema",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Solgema, JqueryTools, Flow, Tabs',
      author='Martronic SA',
      author_email='martronic@martronic.ch',
      url='http://www.martronic.ch/Solgema/plone_products/solgema_flowview',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Solgema'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.jquerytools'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
