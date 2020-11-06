import os
from setuptools import setup

VERSION = ""
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.VERSION'), 'rt') as vfile:
    VERSION = vfile.readlines()[0].strip("\n").strip()


setup(name='pypact',
      version=VERSION,
      description='The package for reading and manipulating the fispact output text file.',
      url='https://github.com/fispact/pypact',
      author='UKAEA',
      author_email='thomas.stainer@ukaea.uk',
      license='Apache License 2.0',
      packages=[
          'pypact',
          'pypact.analysis',
          'pypact.library',
          'pypact.input',
          'pypact.output',
          'pypact.printlib',
          'pypact.tools',
          'pypact.util',
      ],
      install_requires=[],
      python_requires='>=3.6',
      scripts=[
          'pypact/tools/fispactconverter.py'
      ],
      setup_requires=[
          'pytest-runner',
      ],
      test_suite='tests.testsuite',
      tests_require=[
          'pytest',
          'pytest-cov>=2.3.1',
          'mock',
          'jsonschema',
          'numpy',
      ],
      package_data={'': ['library/data/*.json']},
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'fispactconverter = pypact.tools.fispactconverter:main',
          ]
      },
      )
