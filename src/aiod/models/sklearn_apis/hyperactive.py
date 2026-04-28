# ruff: noqa: E501
"""Index for the hyperactive optimization library."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__Hyperactive(_ModelPkgSklearnEstimator):
    """Indexes all gradient-free optimizer classes from hyperactive (v5+).

    hyperactive v5 moved its optimizers under ``hyperactive.opt.gfo``.
    All 21 classes available in that module are indexed here.

    References
    ----------
    https://github.com/hyperactive-project/Hyperactive
    https://pypi.org/project/hyperactive/
    """

    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "hyperactive",
        "pkg_pypi_name": "hyperactive",
        "object_types": ["optimizer"],
    }

    # each key is the class name, value is the full import path
    # confirmed by inspecting hyperactive.opt.gfo directly
    _obj_dict = {
        "BayesianOptimizer": "hyperactive.opt.gfo.BayesianOptimizer",
        "DifferentialEvolution": "hyperactive.opt.gfo.DifferentialEvolution",
        "DirectAlgorithm": "hyperactive.opt.gfo.DirectAlgorithm",
        "DownhillSimplexOptimizer": "hyperactive.opt.gfo.DownhillSimplexOptimizer",
        "EvolutionStrategy": "hyperactive.opt.gfo.EvolutionStrategy",
        "ForestOptimizer": "hyperactive.opt.gfo.ForestOptimizer",
        "GeneticAlgorithm": "hyperactive.opt.gfo.GeneticAlgorithm",
        "GridSearch": "hyperactive.opt.gfo.GridSearch",
        "HillClimbing": "hyperactive.opt.gfo.HillClimbing",
        "LipschitzOptimizer": "hyperactive.opt.gfo.LipschitzOptimizer",
        "ParallelTempering": "hyperactive.opt.gfo.ParallelTempering",
        "ParticleSwarmOptimizer": "hyperactive.opt.gfo.ParticleSwarmOptimizer",
        "PatternSearch": "hyperactive.opt.gfo.PatternSearch",
        "PowellsMethod": "hyperactive.opt.gfo.PowellsMethod",
        "RandomRestartHillClimbing": "hyperactive.opt.gfo.RandomRestartHillClimbing",
        "RandomSearch": "hyperactive.opt.gfo.RandomSearch",
        "RepulsingHillClimbing": "hyperactive.opt.gfo.RepulsingHillClimbing",
        "SimulatedAnnealing": "hyperactive.opt.gfo.SimulatedAnnealing",
        "SpiralOptimization": "hyperactive.opt.gfo.SpiralOptimization",
        "StochasticHillClimbing": "hyperactive.opt.gfo.StochasticHillClimbing",
        "TreeStructuredParzenEstimators": "hyperactive.opt.gfo.TreeStructuredParzenEstimators",
    }

    # all classes in hyperactive are optimizers
    _type_of_objs = {
        "BayesianOptimizer": "optimizer",
        "DifferentialEvolution": "optimizer",
        "DirectAlgorithm": "optimizer",
        "DownhillSimplexOptimizer": "optimizer",
        "EvolutionStrategy": "optimizer",
        "ForestOptimizer": "optimizer",
        "GeneticAlgorithm": "optimizer",
        "GridSearch": "optimizer",
        "HillClimbing": "optimizer",
        "LipschitzOptimizer": "optimizer",
        "ParallelTempering": "optimizer",
        "ParticleSwarmOptimizer": "optimizer",
        "PatternSearch": "optimizer",
        "PowellsMethod": "optimizer",
        "RandomRestartHillClimbing": "optimizer",
        "RandomSearch": "optimizer",
        "RepulsingHillClimbing": "optimizer",
        "SimulatedAnnealing": "optimizer",
        "SpiralOptimization": "optimizer",
        "StochasticHillClimbing": "optimizer",
        "TreeStructuredParzenEstimators": "optimizer",
    }

    # inverse lookup: scitype -> list of class names
    _objs_by_type = {
        "optimizer": [
            "BayesianOptimizer",
            "DifferentialEvolution",
            "DirectAlgorithm",
            "DownhillSimplexOptimizer",
            "EvolutionStrategy",
            "ForestOptimizer",
            "GeneticAlgorithm",
            "GridSearch",
            "HillClimbing",
            "LipschitzOptimizer",
            "ParallelTempering",
            "ParticleSwarmOptimizer",
            "PatternSearch",
            "PowellsMethod",
            "RandomRestartHillClimbing",
            "RandomSearch",
            "RepulsingHillClimbing",
            "SimulatedAnnealing",
            "SpiralOptimization",
            "StochasticHillClimbing",
            "TreeStructuredParzenEstimators",
        ],
    }