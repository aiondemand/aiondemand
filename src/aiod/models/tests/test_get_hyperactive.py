"""Tests for hyperactive package index via models.get."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies

# pairs of (class name, module path) for every class we indexed
# list was built by running inspect on hyperactive.opt.gfo locally
_HYPERACTIVE_GFO_CLASSES = [
    ("BayesianOptimizer", "hyperactive.opt.gfo"),
    ("DifferentialEvolution", "hyperactive.opt.gfo"),
    ("DirectAlgorithm", "hyperactive.opt.gfo"),
    ("DownhillSimplexOptimizer", "hyperactive.opt.gfo"),
    ("EvolutionStrategy", "hyperactive.opt.gfo"),
    ("ForestOptimizer", "hyperactive.opt.gfo"),
    ("GeneticAlgorithm", "hyperactive.opt.gfo"),
    ("GridSearch", "hyperactive.opt.gfo"),
    ("HillClimbing", "hyperactive.opt.gfo"),
    ("LipschitzOptimizer", "hyperactive.opt.gfo"),
    ("ParallelTempering", "hyperactive.opt.gfo"),
    ("ParticleSwarmOptimizer", "hyperactive.opt.gfo"),
    ("PatternSearch", "hyperactive.opt.gfo"),
    ("PowellsMethod", "hyperactive.opt.gfo"),
    ("RandomRestartHillClimbing", "hyperactive.opt.gfo"),
    ("RandomSearch", "hyperactive.opt.gfo"),
    ("RepulsingHillClimbing", "hyperactive.opt.gfo"),
    ("SimulatedAnnealing", "hyperactive.opt.gfo"),
    ("SpiralOptimization", "hyperactive.opt.gfo"),
    ("StochasticHillClimbing", "hyperactive.opt.gfo"),
    ("TreeStructuredParzenEstimators", "hyperactive.opt.gfo"),
]

_HYPERACTIVE_INSTALLED = _check_soft_dependencies("hyperactive", severity="none")


@pytest.mark.skipif(
    not _HYPERACTIVE_INSTALLED,
    reason="run only if hyperactive is installed",
)
@pytest.mark.parametrize("cls_name,expected_module", _HYPERACTIVE_GFO_CLASSES)
def test_get_hyperactive_class(cls_name, expected_module):
    """Check that get() returns the correct hyperactive class.

    For each indexed class, ``get(cls_name)`` must return the exact same
    class object as a direct import from the declared module path.
    """
    import importlib

    from aiod.models import get

    cls_from_get = get(cls_name)
    mod = importlib.import_module(expected_module)
    cls_direct = getattr(mod, cls_name)

    assert cls_from_get is cls_direct, (
        f"get('{cls_name}') returned {cls_from_get!r}, "
        f"expected {cls_direct!r} from {expected_module}"
    )


@pytest.mark.skipif(
    not _HYPERACTIVE_INSTALLED,
    reason="run only if hyperactive is installed",
)
def test_get_all_hyperactive_classes_importable():
    """All indexed hyperactive classes must be importable without error."""
    import importlib

    for cls_name, module_path in _HYPERACTIVE_GFO_CLASSES:
        mod = importlib.import_module(module_path)
        cls = getattr(mod, cls_name, None)
        assert cls is not None, (
            f"Class '{cls_name}' not found in '{module_path}'. "
            "Check that the dotted path in _obj_dict is correct for "
            "the installed hyperactive version."
        )


@pytest.mark.skipif(
    _HYPERACTIVE_INSTALLED,
    reason="run only if hyperactive is NOT installed",
)
def test_get_hyperactive_softdep_not_present():
    """get() must raise ModuleNotFoundError when hyperactive is not installed.

    The error message must mention 'hyperactive' so the user knows which
    package to install.
    """
    from aiod.models import get

    with pytest.raises(ModuleNotFoundError, match=r"hyperactive"):
        get("HillClimbing")