# Contributing to wagtail-polymath

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/wagtail-nest/wagtail-polymath/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

### Write Documentation

wagtail-polymath could always use more documentation, whether as part of the
official wagtail-polymath docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/wagtail-next/wagtail-polymath/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

### Get Started!

Ready to contribute? Here's how to set up `wagtail-polymath` for local development.

1. Fork the `wagtail-polymath` repo on GitHub.
2. Clone your fork locally:

```sh
git clone https://github.com/your_name_here/wagtail-polymath
```

3. Install your local copy into a virtualenv:

```sh
cd wagtail-polymath/
python -m venv venv
source venv/bin/activate
pip install .
```

4. Create a branch for local development:

```sh
git checkout -b name-of-your-bugfix-or-feature
```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass `pre-commit` and the
   tests, including testing other Python versions with tox:

```sh
pre-commit
pip install .
tox
```

6. Commit your changes and push your branch to GitHub:

```sh
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, and 3.3, and for PyPy. Check
   https://travis-ci.org/JamesRamm/wagtail-mathblock/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests:

```sh
python -m unittest tests.test_mathblock
```
