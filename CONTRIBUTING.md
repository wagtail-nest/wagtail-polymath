# Contributing to Wagtail Polymath

Thank you for considering to help Wagtail Polymath.

We welcome all support, whether on bug reports, code, reviews, tests, documentation, translations or just feature requests.

## Working on an issue

👉 If an issue isn’t being worked on by anyone, go for it! **No need to ask "please assign me this issue".** Add a comment to claim the issue once you’re ready to start.

Always start work on issues or features by creating a new git branch from the most up-to-date `main` branch.
When ready, open a pull request with as detailed a description as possible, including a reference to the GitHub issue
number that the PR addresses or relates to. Use `Fixes #123`, `Closes #123` or `Addresses #123` when fixing an issue.
Use `Relates to #123` or `Part of #123` if addressing a small part of a multi-item issue.


## Reporting bugs

To report bugs, use our [issue tracker](https://github.com/wagtail-nest/wagtail-polymath/issues).


## Feature requests

Use our [issue tracker](https://github.com/wagtail-nest/wagtail-polymath/issues) for feature requests


## Code reviews

We welcome code reviews from everyone. You can see a list of [pull requests](https://github.com/wagtail-nest/wagtail-polymath/pulls)


## Triaging issues

We welcome help with triaging issues and pull requests. You can help by:

- Adding more details or your own perspective to bug reports or feature requests.
- Reviewing or otherwise offering your feedback on pull requests.


## Development instructions

### Install

To make changes to this project, first clone this repository:

```sh
git clone git@github.com:wagtail-nest/wagtail-polymath.git
cd wagtail-polymath
```

With your preferred virtualenv activated, install testing dependencies:

```sh
pip install -e '.[testing]' -U
```

### pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit). To set up locally:

```shell
# if you don't have it yet, globally
$ pip install pre-commit
# go to the project directory
$ cd wagtail-polymath
# initialize pre-commit
$ pre-commit install

# Optional, run all checks once for this, then the checks will run only on the changed files
$ pre-commit run --all-files
```

### How to run tests

Now you can run tests as shown below:

```sh
tox
```

or, you can run them for a specific environment `tox -e python3.11-django4.2-wagtail5.2` or specific test
`tox -e python3.11-django4.2-wagtail5.2 -- tests/test_placeholder.py`

To run the test app interactively, use `tox -e interactive`, visit `http://127.0.0.1:8020/admin/` and log in with `admin`/`changeme`.
