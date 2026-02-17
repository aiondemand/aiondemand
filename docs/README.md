[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

# Connect to [AI-on-Demand](https://aiod.eu) in Python.

The [AI-on-Demand](https://aiod.eu) (AIOD) platform empowers AI research and innovation for industry and academia. 
At its core if the [metadata catalogue](https://api.aiod.eu) which indexes countless AI resources, such as datasets, papers, and educational material, 
from many different platforms such as [Zenodo](https://www.zenodo.org), [OpenML](https://www.openml.org), and [AIDA](https://https://www.i-aida.org/ai-educational-resources/).

This package is mainly intended for users that want to programmatically access the platform to, e.g., build a service, fetch resources in their scripts, or write a connector that registers metadata of another platform with AI-on-Demand. 
A web interface for browsing and registering assets is available on AI-on-Demand, through [MyLibrary](https://mylibrary.aiod.eu) and the Metadata Catalogue Editor services (to be deployed), respectively.

## Installation
The `aiondemand` package is on [PyPI](https://pypi.org/project/aiondemand/):

```bash
$ pip install aiondemand
```

Tip: install your dependencies in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/).

## Usage
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
Not all contributors need be affiliated with this funding.

[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter) were used to create the repository structure.
