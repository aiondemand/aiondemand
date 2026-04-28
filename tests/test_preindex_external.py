"""Tests for external library preindex discovery helpers."""

from aiod.utils._indexing import _preindex_external as external

FakeEstimator = type(
    "FakeEstimator",
    (),
    {"__module__": "sktime.forecasting._fake"},
)


def test_sktime_locdict_prefers_registry(monkeypatch):
    monkeypatch.setattr(
        external,
        "_all_registry_objects_with_names",
        lambda package_name, registry_module_name: [("FakeEstimator", FakeEstimator)],
    )
    monkeypatch.setattr(
        external,
        "_all_skbase_objects_locdict",
        lambda package_name: {"ShouldNotBeUsed": "sktime.foo.ShouldNotBeUsed"},
    )

    locdict = external._all_sktime_estimators_locdict()

    assert locdict == {"FakeEstimator": "sktime.forecasting.FakeEstimator"}


def test_skpro_locdict_falls_back_to_skbase(monkeypatch):
    monkeypatch.setattr(
        external,
        "_all_registry_objects_with_names",
        lambda package_name, registry_module_name: [],
    )
    monkeypatch.setattr(
        external,
        "_all_skbase_objects_locdict",
        lambda package_name: {"FallbackEstimator": "skpro.foo.FallbackEstimator"},
    )

    locdict = external._all_skpro_estimators_locdict()

    assert locdict == {"FallbackEstimator": "skpro.foo.FallbackEstimator"}