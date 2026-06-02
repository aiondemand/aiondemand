# Contributing to AIoD SDK

Welcome to the AI-on-Demand (AIoD) SDK! Contributions are welcome, and they
are greatly appreciated. Every little bit helps, and credit will always be given.

## Getting Involved

The best way to get started is to:

1. Join the [AIoD Discord server](https://discord.com/invite/6Z2PczwZd4) and
   say hello -- it's a great place to ask questions and coordinate with other
   contributors.
2. Browse open [issues](https://github.com/aiondemand/aiondemand/issues).
   Issues labelled `good first issue` or `help wanted` are especially suited
   for new contributors.
3. Set up your development environment by following the
   [Developer Setup Guide](developer_setup.md).

If you get stuck at any point, don't hesitate to ask on Discord or open a
discussion on [GitHub Discussions](https://github.com/aiondemand/aiondemand/discussions).

---

## Types of Contributions

### Report Bugs

Before reporting a bug, please check the
[issue tracker](https://github.com/aiondemand/aiondemand/issues) to make sure
it has not already been reported. If it has, you may add any additional
information that might be missing. If you have nothing to add, react with a
:+1: to communicate you are also experiencing the issue.

When filing a new bug report, please include:

- A clear description of the expected vs. observed behavior.
- Steps to reproduce the bug, preferably with a
  [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example).
- Your environment details. The following snippet prints the relevant info:
  ```python
  import aiod, platform
  print(f"{platform.platform()=}")
  print(f"{aiod.__version__=}")
  print(f"{platform.python_version()=}")
  ```
  or, in one command:
  ```
  python -c 'import aiod; import platform; print(f"{platform.platform()=}"); print(f"{aiod.__version__=}"); print(f"{platform.python_version()=}")'
  ```
- Any other details about your local setup that might be helpful.

### Fix Bugs and Add Features

The [issue tracker](https://github.com/aiondemand/aiondemand/issues) lists
known bugs (labelled `bug`) and proposed features (labelled `enhancement`).

Before working on an open issue, please post a comment indicating your interest
so that we can assign you and avoid duplicate work.

### Improve Documentation

You can never have enough documentation! Feel free to contribute to the
official docs, docstrings, tutorials, or blog posts.

### Submit Feedback / Feature Requests

When proposing a new feature, please explain:

- What problem does it solve, or what functionality does it add?
- Does it change an existing interface, or add a new one? What would the new
  interface look like?
- Give an example use case.
- How does it affect existing functionality? Is it a breaking change?

Keep the scope as narrow as possible -- this keeps discussion focused and makes
implementation easier. Even if a feature request is accepted, it is not a
guarantee that we have time to implement it ourselves. However, a well-scoped
request makes it much easier for any contributor to pick it up.
Contributions welcome!

---

## Contribution Workflow

### 1. Set Up Your Development Environment

Follow the [Developer Setup Guide](developer_setup.md) to fork, clone, and
install the project with development dependencies. The guide also covers
setting up the REST API backend for integration testing.

### 2. Create a Feature Branch

Even when working on a fork, we strongly recommend creating a new branch off
`main`:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

### 3. Make Your Changes

- Write clear, well-tested code.
- When fixing a bug, add a regression test that fails without your fix and
  passes with it, and reference the GitHub issue number in a comment.
- When adding a feature, add tests that cover the new code.

### 4. Validate Your Changes

Before opening a pull request, run the full quality checks:

```bash
# Run tests
python -m pytest -v

# Run linting
ruff check .

# Auto-fix linting issues (optional)
ruff check --fix .

# Run all pre-commit hooks
pre-commit run --all-files
```

### 5. Open a Pull Request

Push your branch and open a pull request against `main`. A core contributor
will review the changes and may request modifications. Once all concerns are
addressed, the PR will be merged and included in the next release.

---

## Pull Request Guidelines

1. The pull request should include tests where appropriate.
2. If the pull request adds functionality, update the docs accordingly.
3. The pull request should work on all currently supported operating systems
   and Python versions.

---

## Code of Conduct

The `aiondemand` project is released with a
[Code of Conduct](conduct.md). By contributing to this project you agree to
abide by its terms.
