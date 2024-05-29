# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Types of Contributions

### Report Bugs

Before reporting a bug, please check our [issue tracker](https://github.com/aiondemand/aiondemand/issues)
that the bug has not yet been reported. If it has, you may add any additional information that might be 
missing to that issue. If you have nothing to add, react with a 👍 to the original report to communicate
you are also experiencing the issue.

In case the bug has not been reported yet, please follow these steps to ensure that we can investigate
the issue and resolve it efficiently:

- Describe the bug. What is the expected behavior, and what is the observed behavior?
- As much as possible, provide steps to reproduce the bug. Preferably with a [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example).
- Share your operating system name and version, Python and `aiondemand` version. The following 
  code snippet can be used to automatically obtain the information:
  ```python
  import aiod
  import platform
  print(f"{platform.platform()=}")
  print(f"{aiod.__version__=}")
  print(f"{platform.python_version()=}")
  ```
  or, in one command; 
  ```
  python -c 'import aiod; import platform; print(f"{platform.platform()=}"); print(f"{aiod.__version__=}"); print(f"{platform.python_version()=}")'
  ```
- If you have any additional details about your local setup that might be helpful in troubleshooting, please share them.

### Fixing bugs and adding features

Our [issue tracker](https://github.com/aiondemand/aiondemand/issues) has a list of known bugs (labelled `bug`)
and proposed features (labelled `enhancement`). Of particular interest may be those issues labelled `help wanted`,
as those are best suited for outside contributors. 

Before working on an open issue, please first indicate your interest in fixing it by posting a comment on the issue.
That way, we can assign people (you) to the issue, and avoid multiple people working on fixing the same bug in parallel (and thus avoid double work).

### Write Documentation

You can never have enough documentation! Please feel free to contribute to any
part of the documentation, such as the official docs, docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

If you are proposing a feature, please explain in detail how it would work. 
Answer at least the following questions:

  - What is the goal of the new feature? Which problem does it solve, or what functionality does it add?
  - Does the feature change an existing interface, or add a new one? What does the suggested new interface look like?
  - Give an example of a use case where the feature would be of added benefit.
  - How does the change affect other existing functionality? Will it be a breaking change?

When suggesting a new feature, try to keep the scope as narrow as possible.
This keeps the discussion focused, and makes it easier to get to an agreement and subsequently implement it.
Even if a feature request is accepted, it is not a guarantee that we have time available to implement it ourselves.
However, it makes it much easier for any contributor to start implementing the feature. Contributions welcome :)

## Get Started!

Ready to contribute? Here's how to set up `aiondemand` for local development.

### Setting up the Development Environment 

1. Fork the repository from GitHub by clicking the `fork` button on the webpage.
1. Clone the fork: `git clone https://github.com/USERNAME/aiondemand.git`. Remember to substitute your username.
1. Install the project locally (after moving to the new directory). 
Similar to a regular installation, we strongly recommend you to make use of a virtual environment.
After activating the environment, install the package in editable mode and with the additional develop packages: `python -m pip install -e ".[dev]"`

Before making any changes, first check your setup works:
```console
python -m pytest tests
```
All tests should pass.

### Making Changes

While working on a feature, you can work from the "develop"-branch, provided you are working on a fork.
However, even if you are working on a fork we strongly recommend you to make changes on a new branch.
When working on the main repository, this is required. When working on a fork, this makes it easier to 
keep your fork in sync with the upstream repository (this one).
Your new branch should branch off "develop":

```console
git checkout -b name-of-your-bugfix-or-feature
```

When you're done making changes, check that your changes conform to any code formatting requirements and pass any tests.
Also add new tests. When fixing a bug, add a regression test that exposes the bug (i.e., it should fail without your changes, and pass with them)
and add a reference to the GitHub issue number as a comment. When adding a feature, add new tests to cover the new code.

Finally, you can open a pull request with the proposed changes. A core contributor will have a look at the changes,
and possibly request some changes. After all concerns have been addressed, the contributor will merge the change
and it will be included in the next release.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include additional tests if appropriate.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all currently supported operating systems and versions of Python.

## Code of Conduct

Please note that the `aiondemand` project is released with a Code of Conduct. 
By contributing to this project you agree to abide by its terms.
