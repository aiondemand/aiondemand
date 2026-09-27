"""Test preindex"""

import pytest
from aiod.utils._indexing._preindex_sklearn import _generate_sklearn_objs_by_type

def test_generate_sklearn_objs_by_type():
    type_of_objs = {
        "RandomForestClassifier": "classifier",
        "RandomForestRegressor": "regressor",
        "Pipeline": ["classifier", "regressor"],
    }
    expected_objs_by_type = {
        "classifier": ["RandomForestClassifier", "Pipeline"],
        "regressor": ["RandomForestRegressor", "Pipeline"],
    }
    
    result = _generate_sklearn_objs_by_type(type_of_objs)
    
    assert result == expected_objs_by_type

def test_generate_sklearn_objs_by_type_empty():
    assert _generate_sklearn_objs_by_type({}) == {}