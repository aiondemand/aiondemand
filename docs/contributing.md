# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

## Types of Contributions

### Report Bugs

Before reporting a bug, please check our [issue tracker](#) to ensure the bug has not already been reported. If it has, you may add any additional information that might be missing. If you have nothing to add, react with a 👍 to the original report to indicate you are also experiencing the issue.

If the bug has not been reported yet, please follow these steps to help us investigate and resolve it efficiently:

- Describe the bug clearly. What is the expected behavior, and what is the observed behavior?
- Provide steps to reproduce the issue, preferably with a minimal, reproducible example.
- Share your operating system name and version, Python version, and aiondemand version. You can use:

```python
import aiod
import platform
print(f"{platform.platform()=}")
print(f"{aiod.__version__=}")
print(f"{platform.python_version()=}")
```

Or in one command:

```bash
python -c 'import aiod; import platform; print(f"{platform.platform()=}"); print(f"{aiod.__version__=}"); print(f"{platform.python_version()=}")'
```

- Include any additional details about your local setup that may help with troubleshooting.

### Fixing Bugs and Adding Features

Our [issue tracker](#) contains known bugs (labelled bug) and proposed features (labelled enhancement). Issues labelled help wanted are particularly well suited for external contributors.

Before working on an issue, please indicate your interest by commenting on it. This allows maintainers to assign the issue and helps prevent duplicate work.

### Write Documentation

Documentation improvements are always welcome. You can contribute to:

- Official documentation
- Docstrings
- Tutorials or examples
- External blog posts or guides

Clear documentation improves adoption and contributor onboarding.

### Submit Feedback

When proposing a feature, provide a detailed explanation:

- What problem does the feature solve?
- Does it change an existing interface or add a new one?
- What would the proposed interface look like?
- Provide an example use case.
- Would this introduce a breaking change?

Keep proposals narrowly scoped to make discussion and implementation easier. Even if a feature is accepted, maintainers may not have time to implement it immediately — contributions are welcome.

## Get Started!

Ready to contribute? Follow these steps to set up aiondemand for local development.

### Setting up the Development Environment

1. Fork the repository on GitHub.
2. Clone your fork:

```bash
git clone https://github.com/USERNAME/aiondemand.git
```

Replace USERNAME with your GitHub username.

3. Navigate into the project directory.
4. Create and activate a virtual environment.
5. Install the project in editable mode with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

6. Before making changes, verify that everything works:

```bash
python -m pytest tests
```

All tests should pass.

### Making Changes

While working on a feature, you can work from the "main"-branch, provided you are working on a fork.
However, even if you are working on a fork we strongly recommend you to make changes on a new branch.
When working on the main repository, this is required. When working on a fork, this makes it easier to 
keep your fork in sync with the upstream repository (this one).
Your new branch should branch off "main":

Before creating your branch, make sure your local main branch is up to date:

```bash
git checkout main
git pull origin main
git checkout -b name-of-your-bugfix-or-feature
```

This ensures your work is based on the latest version of the repository and reduces the likelihood of merge conflicts.

After implementing your changes:

- Ensure code formatting and linting requirements are met.
- Run all tests and confirm they pass.
- Add new tests if appropriate.

When fixing a bug:

- Add a regression test that fails without your fix and passes with it.
- Reference the related GitHub issue number in a comment.

When adding a feature:

- Add tests covering the new functionality.
- Update documentation if necessary.

Once ready, open a pull request. A core contributor will review the changes and may request revisions. After review approval, the changes will be merged and included in a future release.

## Pull Request Guidelines

Before submitting a pull request, ensure:

- Tests are added or updated where appropriate.
- Documentation is updated if functionality changes.
- The changes work on all supported operating systems and Python versions.
- All CI checks pass.

## Code of Conduct

Please note that the aiondemand project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.
