Contributing to pypact
=======================

We welcome contributions to pypact! This guide will help you get started.

Ways to Contribute
------------------

There are many ways to contribute to pypact:

- **Report bugs**: If you find a bug, please open an issue on GitHub
- **Suggest features**: Have an idea for improvement? Open an issue to discuss it
- **Fix bugs**: Look through the GitHub issues for bugs to fix
- **Add features**: Implement new features or improvements
- **Improve documentation**: Help make the documentation better
- **Write examples**: Share your pypact scripts as examples

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/YOUR_USERNAME/pypact.git
      cd pypact

3. Create a virtual environment:

   .. code-block:: bash

      python3 -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install development dependencies:

   .. code-block:: bash

      pip install -r requirements.dev.txt
      pip install -e .

5. Create a branch for your changes:

   .. code-block:: bash

      git checkout -b feature/my-new-feature

Code Style
----------

Pypact follows standard Python code style guidelines:

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

Linting
~~~~~~~

Run the linter before submitting:

.. code-block:: bash

   flake8 pypact tests

The project uses pylint configuration in ``.pylintrc``.

Testing
-------

Writing Tests
~~~~~~~~~~~~~

All new features should include tests. Tests are located in the ``tests/`` directory.

.. code-block:: python

   # Example test
   import pypact as pp
   import pytest

   def test_reader_basic():
       """Test basic reader functionality"""
       with pp.Reader('test_file.out') as output:
           assert output.run_data is not None
           assert len(output.inventory_data) > 0

Running Tests
~~~~~~~~~~~~~

Run all tests:

.. code-block:: bash

   pytest tests

Run specific test file:

.. code-block:: bash

   pytest tests/test_reader.py

Run with coverage:

.. code-block:: bash

   pytest tests --cov=pypact

Test Requirements
~~~~~~~~~~~~~~~~~

- All tests must pass before merging
- New features should have >80% code coverage
- Tests should be clear and well-documented
- Use fixtures for common test data

Documentation
-------------

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

The documentation is built with Sphinx:

.. code-block:: bash

   cd docs
   make html

View the built documentation:

.. code-block:: bash

   # Open docs/_build/html/index.html in your browser

Documentation Style
~~~~~~~~~~~~~~~~~~~

- Use reStructuredText (.rst) format
- Include code examples for new features
- Add docstrings to public functions and classes
- Keep documentation up-to-date with code changes

Docstring Format
~~~~~~~~~~~~~~~~

Use NumPy/SciPy style docstrings:

.. code-block:: python

   def my_function(param1, param2):
       """
       Brief description of the function.

       Longer description if needed, explaining what the
       function does in more detail.

       Parameters
       ----------
       param1 : str
           Description of param1
       param2 : int
           Description of param2

       Returns
       -------
       bool
           Description of return value

       Examples
       --------
       >>> my_function("test", 42)
       True
       """
       pass

Pull Request Process
--------------------

1. **Update documentation**: Ensure documentation reflects your changes
2. **Write tests**: Add tests for new functionality
3. **Run tests**: Make sure all tests pass
4. **Update CHANGELOG**: Add a note about your changes
5. **Commit your changes**: Use clear, descriptive commit messages
6. **Push to your fork**: Push your branch to GitHub
7. **Open a Pull Request**: Create a PR from your fork to the main repository

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

- **One feature per PR**: Keep PRs focused on a single feature or fix
- **Clear description**: Explain what your PR does and why
- **Reference issues**: Link to related issues (e.g., "Fixes #123")
- **Update docs**: Include documentation updates
- **Pass CI checks**: All CI checks must pass
- **Respond to feedback**: Address reviewer comments promptly

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Use clear, descriptive commit messages:

.. code-block:: text

   Short summary (50 chars or less)

   More detailed explanation if needed. Wrap at 72 characters.
   Explain what changed and why, not how.

   - Bullet points are okay
   - Use present tense ("Add feature" not "Added feature")
   - Reference issues: Fixes #123

Examples:

.. code-block:: text

   Add support for PRINTLIB 7 output

   Implements a new reader for PRINTLIB 7 output format,
   allowing users to parse pathway analysis data.

   Fixes #234

Code Review
-----------

All submissions require review before merging. Reviewers will look for:

- **Correctness**: Does the code work as intended?
- **Tests**: Are there adequate tests?
- **Documentation**: Is it properly documented?
- **Style**: Does it follow code style guidelines?
- **Performance**: Are there any performance concerns?

Responding to Review
~~~~~~~~~~~~~~~~~~~~

- Be open to feedback
- Explain your reasoning if you disagree
- Make requested changes promptly
- Push updates to the same branch

Release Process
---------------

Pypact uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

Releases are managed by the maintainers.

Common Tasks
------------

Adding a New Parser
~~~~~~~~~~~~~~~~~~~

1. Create parser class in ``pypact/output/`` or ``pypact/printlib/``
2. Implement required methods (``fispact_deserialize``, ``json_serialize``)
3. Add tests in ``tests/``
4. Document in ``docs/parsers.rst``
5. Add example usage

Adding a New Feature
~~~~~~~~~~~~~~~~~~~~

1. Open an issue to discuss the feature
2. Get feedback from maintainers
3. Implement the feature with tests
4. Update documentation
5. Submit pull request

Fixing a Bug
~~~~~~~~~~~~

1. Create a test that reproduces the bug
2. Fix the bug
3. Verify the test now passes
4. Submit pull request with test and fix

Getting Help
------------

If you need help:

- **Documentation**: Check https://pypact.readthedocs.io
- **Issues**: Search existing issues on GitHub
- **Discussions**: Start a discussion on GitHub
- **Contact**: Reach out to the FISPACT team at https://fispact.ukaea.uk/contact

Community Guidelines
--------------------

- Be respectful and inclusive
- Help others when you can
- Give constructive feedback
- Follow the code of conduct

Code of Conduct
~~~~~~~~~~~~~~~

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

License
-------

By contributing to pypact, you agree that your contributions will be licensed 
under the Apache License 2.0.

Thank You!
----------

Thank you for contributing to pypact! Your efforts help make this project better 
for everyone.
