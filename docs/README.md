# [AI-on-Demand](https://aiodp.eu) - obtain and share AI resources with ease

* quick instantiation of AI models from string IDs across the ecosystem
* cross-platform metadata catalogue for papers, projects, datasets, models
* marketplace features for sharing models and assets (under development)

A web interface for assets is available through [the AIoD catalogue](https://catalogue.aiodp.eu) and the [Metadata Catalogue Editor](https://editor.aiodp.eu/) (under construction)

| Overview | **[AIoD Homepage](https://aiodp.eu)** · **[Tutorials](https://github.com/aiondemand/aiondemand/tree/main/docs/examples)** · **[Release Notes](https://github.com/aiondemand/aiondemand/releases)** |
|---|---|
| **Open Source** |  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/aiondemand/aiondemand/blob/main/LICENSE) |
| **Community** | [![!discord](https://img.shields.io/static/v1?logo=discord&label=discord&message=chat&color=lightgreen)](https://discord.gg/A7YDRyvqYE) |
| **CI/CD** | [![github-actions](https://img.shields.io/github/actions/workflow/status/aiondemand/aiondemand/release.yaml?logo=github)](https://github.com/aiondemand/aiondemand/actions/workflows/release.yaml) |
| **Code** |  [![!pypi](https://img.shields.io/pypi/v/aiondemand?color=orange)](https://pypi.org/project/aiondemand/) [![!python-versions](https://img.shields.io/pypi/pyversions/aiondemand)](https://www.python.org/) |

## Server Status

> **Note**: The AIoD platform is currently undergoing migration to DeployAI infrastructure. During this transition, some services may be temporarily unavailable. The Python SDK will continue to work once the migration is complete.

## Installation

Install from [PyPI](https://pypi.org/project/aiondemand/) via:

```bash
$ pip install aiondemand
```

## Quick start

### AI model instantiation

Also see the [AI model instantiation tutorial](https://github.com/aiondemand/aiondemand/blob/main/docs/examples/ai-on-demand.ipynb)

`aiod.get(id: str)` is the key entry point:

* `id` is a unique string describing a model
* return is the python object, or an exception informing the user of required dependencies

```python
from aiod import get

clf = get("RandomForestClassifier(n_estimators=42)")
clf
```

directly constructs the random forest from `scikit-learn`
```
RandomForestClassifier(n_estimators=42)
```

Works across the ecosystem! 

```python
from aiod import get

clf = get("XGBClassifier()")
clf
```

... constructs the `XGBClassifier`, or raises an informative error message to
install `xgboost` in the environment (if not available)

```
XGBClassifier()
```

Complex pipelines and composites are supported out-of-the-box:

```python
spec = """
pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100))])
cv = KFold(n_splits=5, shuffle=True, random_state=42)

return GridSearchCV(
    estimator=pipe,
    param_grid=[{
        "classifier__max_depth": [5, 10],
        "classifier__min_samples_split": [2, 5],
    },
    ],
    cv=cv,
    )
"""

get(spec)
```

* no more hassle with import statements!
* share your AI model specs as easy-to-handle strings!

#### Indexed libraries

The following libraries are indexed - the scope is expanding, roadmap contributions
are welcome!

##### `scikit-learn` tabular estimators

- `scikit-learn`
- `catboost`
- `feature-engine`
- `lightgbm`
- `imbalanced-learn`
- `mlxtend`
- `scikit-lego`
- `xgboost`

##### Probabilistic supervised learning and survival modelling

- `skpro`

##### Time series, forecasting

- `sktime`


### AI asset catalogue search

Also see the [AI metadata catalogue tutorial](https://github.com/aiondemand/aiondemand/blob/main/docs/examples/getting-started.ipynb)

You can directly access endpoints through the Python API, for example to browse datasets:
```python
import aiod

aiod.datasets.get_list()
```
And results will be returned as a [Pandas](https://pandas.pydata.org/docs/getting_started/overview.html) dataframe (though the `data_format` may be used to get JSON instead):
```bash
      platform platform_resource_identifier                    name       date_published                                            same_as  is_accessible_for_free  ...  relevant_link  relevant_resource relevant_to research_area scientific_domain identifier
0  huggingface       acronym_identification  acronym_identification  2022-03-02T23:29:22  https://huggingface.co/datasets/acronym_identi...                    True  ...             []                 []          []            []                []          1
...
9  huggingface              allegro_reviews         allegro_reviews  2022-03-02T23:29:22    https://huggingface.co/datasets/allegro_reviews                    True  ...             []                 []          []            []                []         10

[10 rows x 30 columns]
```

You can even query the elastic search endpoints:
```python
aiod.publications.search(query="Robotics")
```
```bash
      platform platform_resource_identifier                                               name date_published                                            same_as is_accessible_for_free  ... relevant_resource relevant_to      research_area  scientific_domain  type  identifier
0  robotics4eu                         1803  Responsible Robotics &amp; non-tech barriers t...           None  https://www.robotics4eu.eu/publications/respon...                   None  ...                []          []  [other materials]  [other materials]  None           4

[1 rows x 36 columns]
```
## Contributing

Interested in contributing? Check out the [contributing guidelines](contributing.md), then start with the [Developer Setup Guide](developer_setup.md) to set up your local development environment. Check out the complete documentation here: https://aiondemand.github.io/aiondemand/developer_setup
By contributing to this project, you agree to abide by our [Code of Conduct](conduct.md).

## Credits

The `aiondemand` package is being developed with funding from EU’s Horizon Europe research and innovation program under grant agreement [No. 101070000 (AI4EUROPE)](https://cordis.europa.eu/project/id/101070000).
Not all contributors are affiliated with this funding.

[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter) were used to create the repository structure.
