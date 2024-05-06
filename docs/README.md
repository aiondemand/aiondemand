# AI-on-Demand 

The [AI-on-Demand](https://aiod.eu) (AIOD) platform empowers AI research and innovation for industry and academia. 
At its core if the [metadata catalogue](https://aiod.i3a.es) which indexes countless AI resources, such as datasets, papers, and educational material, 
from many different platforms such as [Zenodo](https://www.zenodo.org), [OpenML](https://www.openml.org), and [AIDA](https://https://www.i-aida.org/ai-educational-resources/).
This package allows you to explore all resources in the metadata catalogue through Python.
You can also browse the contents of the AI-on-Demand metadata catalogue through the [MyLibrary](https://mylibrary.aiod.eu) service.

## Installation

```bash
$ pip install aiondemand
```

## Usage

```python
import aiod

aiod.datasets.get_list()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`aiondemand` is an AI-on-Demand under development initiative, and created by Jean Matias. It is licensed under the terms of the MIT license.

## Credits

`aiondemand` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
