import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_zodbconn',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_fanstatic',
    'ZODB3',
    'RelStorage',
    'waitress',
    'js.bootstrap',
    'js.jqueryui',
    'zope.component',
    'js.jquery_tools'
    ]

setup(name='giza',
      version='0.0',
      description='giza',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="giza",
      entry_points = """\
      [paste.app_factory]
      main = giza:main

      # Fanstatic resource library
      [fanstatic.libraries]
      giza = giza.resources:library

      # A console script to serve the application and monitor static resources
      [console_scripts]
      pserve-fanstatic = giza.resources:pserve

      """,
      )

