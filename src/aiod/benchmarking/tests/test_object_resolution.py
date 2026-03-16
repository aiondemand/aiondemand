"""Tests for _resolve_obj spec-string resolution."""

import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier

from aiod.benchmarking._resolve_obj import _resolve_obj


class TestResolveClassifiers:
    def test_decision_tree(self):
        obj, obj_type = _resolve_obj("DecisionTreeClassifier()")
        assert isinstance(obj, DecisionTreeClassifier)
        assert obj_type == "classifier"

    def test_random_forest(self):
        obj, obj_type = _resolve_obj(
            "RandomForestClassifier(n_estimators=10, random_state=0)"
        )
        assert isinstance(obj, RandomForestClassifier)
        assert obj.n_estimators == 10
        assert obj.random_state == 0
        assert obj_type == "classifier"


class TestResolveMetrics:
    def test_accuracy_score(self):
        obj, obj_type = _resolve_obj("accuracy_score")
        assert callable(obj)
        assert obj is accuracy_score
        assert obj_type == "metric"


class TestResolveCVSplitters:
    def test_splitter(self):
        obj, obj_type = _resolve_obj("KFold()")
        assert isinstance(obj, KFold)
        assert obj_type == "cross_validator"

class TestResolveDatasets:
    def test_load_iris(self):
        obj, obj_type = _resolve_obj("load_iris")
        assert callable(obj)
        assert obj_type == "dataset"


class TestResolveErrors:
    def test_nonexistent_class_raises(self):
        with pytest.raises((RuntimeError, ValueError, KeyError)):
            _resolve_obj("inaccurate_class()")

    def test_nonexistent_function_raises(self):
        with pytest.raises((RuntimeError, ValueError, KeyError)):
            _resolve_obj("inaccurate_function")

    def test_obj_type_is_string(self):
        _, obj_type = _resolve_obj("DecisionTreeClassifier()")
        assert isinstance(obj_type, str)