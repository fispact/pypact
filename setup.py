from setuptools import setup


setup(name='pypact',
      version='1.3.1',
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
            'pypact.tools',
            'pypact.util',
      ],
      install_requires=[],
      python_requires='>=3',
      # scripts=[
      #       'pypact/tools/fispactconverter.py'
      # ],
      setup_requires=[
            'pytest-runner',
      ],
      test_suite='tests.testsuite',
      tests_require=[
            'pytest',
            'mock',
            'jsonschema',
      ],
      zip_safe=False,
      entry_points={
            'console_scripts': [
                  'fispactconverter = pypact.tools.fispactconverter:main',
            ]
      },
      )
