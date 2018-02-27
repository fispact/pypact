from setuptools import setup


setup(name='pypact',
      version='1.1.0',
      description='The package for reading and manipulating the fispact output text file.',
      url='https://github.com/fispact/pypact',
      author='UKAEA',
      author_email='thomas.stainer@ukaea.uk',
      license='Apache License 2.0',
      packages=[
            'pypact'
      ],
      install_requires=[],
      python_requires='>=3',
      scripts=['pypact/tools/fispactconverter.py'],
      setup_requires=['pytest-runner'],
      test_suite='pypact.tests.testsuite',
      tests_require=['pytest'],
      zip_safe=False)
