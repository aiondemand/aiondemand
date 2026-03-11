import pytest

from aiod.benchmarking._resolve_obj import _resolve_obj


def test_resolve_classifier_with_params():
    spec = "DecisionTreeClassifier(random_state=42)"
    obj, obj_type = _resolve_obj(spec)
    
    assert obj is not None
    assert obj_type is not None


def test_resolve_metric_function():
    spec = "accuracy_score"
    obj, obj_type = _resolve_obj(spec)
    
    assert obj is not None
    assert obj_type is not None


def test_invalid_spec_raises_error():
    spec = "NonExistentClass()"
    
    with pytest.raises(RuntimeError):
        _resolve_obj(spec)