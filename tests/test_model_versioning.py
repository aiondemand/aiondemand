"""Tests for version-aware model index availability and location rules."""

from packaging.version import Version

from aiod.models.base import _AiodModelPkg


class _DummyVersionedPkg(_AiodModelPkg):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "dummy",
        "pkg_pypi_name": "dummy",
    }
    _obj_dict = {
        "Bar": "dummy.bar.Bar",
        "Foo": "dummy.foo.Foo",
        "Baz": "dummy.baz.Baz",
    }
    _obj_presence = {
        "Foo": ">=1.0,<2.0",
        "Baz": ">=2.0,<3.0",
    }
    _obj_locations = {
        "Foo": [
            {"specifier": "<1.5", "obj": "dummy.foo_old.Foo"},
            {"specifier": ">=1.5", "obj": "dummy.foo_new.Foo"},
        ],
        "Baz": {
            ">=2.0,<3.0": "dummy.baz.Baz",
        },
    }


def test_versioned_metadata_keys_are_subset_of_obj_dict_keys():
    obj_keys = set(_DummyVersionedPkg._obj_dict.keys())
    presence_keys = set(_DummyVersionedPkg._obj_presence.keys())
    location_keys = set(_DummyVersionedPkg._obj_locations.keys())

    assert presence_keys.issubset(obj_keys)
    assert location_keys.issubset(obj_keys)


def test_contained_ids_are_legacy_obj_dict_keys():
    ids = _DummyVersionedPkg.contained_ids()

    assert ids == ["Bar", "Foo", "Baz"]


def test_is_available_uses_pep440_presence_ranges():
    assert _DummyVersionedPkg.is_available("Foo", package_version="1.2")
    assert not _DummyVersionedPkg.is_available("Foo", package_version="2.1")


def test_resolve_obj_uses_versioned_location_rules(monkeypatch):
    monkeypatch.setattr(
        _DummyVersionedPkg,
        "_get_package_version",
        classmethod(lambda cls: Version("1.4")),
    )
    assert _DummyVersionedPkg("Foo")._obj == "dummy.foo_old.Foo"

    monkeypatch.setattr(
        _DummyVersionedPkg,
        "_get_package_version",
        classmethod(lambda cls: Version("1.7")),
    )
    assert _DummyVersionedPkg("Foo")._obj == "dummy.foo_new.Foo"


def test_resolve_obj_returns_none_for_unavailable_id(monkeypatch):
    monkeypatch.setattr(
        _DummyVersionedPkg,
        "_get_package_version",
        classmethod(lambda cls: Version("1.7")),
    )

    assert _DummyVersionedPkg("Baz")._obj is None


def test_resolve_obj_falls_back_to_legacy_obj_dict(monkeypatch):
    monkeypatch.setattr(
        _DummyVersionedPkg,
        "_get_package_version",
        classmethod(lambda cls: Version("1.7")),
    )

    assert _DummyVersionedPkg("Bar")._obj == "dummy.bar.Bar"
