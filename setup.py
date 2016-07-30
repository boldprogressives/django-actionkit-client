from setuptools import setup, find_packages
import sys, os

version = '0.12'

setup(name='django-actionkit-client',
      version=version,
      description="A Django wrapper around Actionkit's MySQL client-db, REST API and XML-RPC API",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Ethan Jucovy',
      author_email='',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "requests",
      ],
      entry_points="""
      [django.plugins]
      actionkit = actionkit
      """,
      )
