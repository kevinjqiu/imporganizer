from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='imporganizer',
      version=version,
      description="Organize your imports according to PEP8",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Kevin J. Qiu',
      author_email='kevin.jing.qiu@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
