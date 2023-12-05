# AIoD SDK Python

### Project structure

```
.
├── README.md
├── .gitignore
├── LICENSE
├── venv
└── python
    └── aiod_sdk                # maybe remove this directory since we're not building a mono-repo
        ├── README.md           # general README
        ├── aiod                # SDK code for different APIs: AIOD, AIDA, etc.
        │   ├── README.md       # how to use / build code
        │   ├── __init__.py     # importing stuff from _src, so that it's clear what you should be able to use if importing this project
        │   ├── _src            # all functionality
        │   └── scripts         # executable python stuff
        ├── pyproject.toml
        └── tests
            └── __init__.py
```
