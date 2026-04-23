"""Tests for AIoD API contracts and validators."""

import pytest

from aiod.contracts import BaseAPIContract, SklearnClassifier


class DummyValidClassifier:
    """Mock class mimicking a valid sklearn classifier."""

    def fit(self, x, y):
        """Mock fit."""
        pass

    def predict(self, x):
        """Mock predict."""
        pass


class DummyInvalidObject:
    """Mock class lacking methods required by classifier contract."""

    def fit(self, x, y):
        """Mock fit."""
        pass


def test_base_contract_raises_not_implemented():
    """Test that BaseAPIContract methods raise NotImplementedError."""
    dummy = DummyValidClassifier()
    
    with pytest.raises(NotImplementedError):
        BaseAPIContract.istypeof(dummy)
        
    with pytest.raises(NotImplementedError):
        BaseAPIContract.runtests(dummy)


def test_sklearn_classifier_istypeof():
    """Test that SklearnClassifier correctly identifies valid/invalid objects."""
    valid_obj = DummyValidClassifier()
    invalid_obj = DummyInvalidObject()
    string_obj = "not a classifier"

    assert SklearnClassifier.istypeof(valid_obj) is True
    assert SklearnClassifier.istypeof(invalid_obj) is False
    assert SklearnClassifier.istypeof(string_obj) is False


def test_sklearn_classifier_runtests():
    """Test the output dictionary of the runtests routine."""
    valid_obj = DummyValidClassifier()
    invalid_obj = DummyInvalidObject()

    # Valid objects should pass the cursory compliance checks
    result_valid = SklearnClassifier.runtests(valid_obj)
    assert result_valid["status"] == "PASSED"
    assert "checks" in result_valid

    # Invalid objects should immediately fail the compliance checks
    result_invalid = SklearnClassifier.runtests(invalid_obj)
    assert result_invalid["status"] == "FAILED"
    assert "Missing 'fit' or 'predict' methods" in result_invalid["checks"]
