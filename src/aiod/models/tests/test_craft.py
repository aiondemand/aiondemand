"""Testing of crafting functionality for sklearn components."""

import pytest

from aiod.models._registry._craft import craft, imports

simple_spec = "RandomForestClassifier()"
simple_spec_with_params = "RandomForestClassifier(n_estimators=10, max_depth=3)"

pipeline_spec = """
pipe = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier())
])

return GridSearchCV(
    estimator=pipe,
    param_grid={
        "clf__n_estimators": [10, 50],
        "clf__max_depth": [None, 5],
    },
    cv=5,
)
"""

specs = [
    simple_spec,
    simple_spec_with_params,
    pipeline_spec,
]


@pytest.mark.parametrize("spec", specs)
def test_craft(spec):
    """Check that crafting works and is inverse to str coercion."""
    crafted_obj = craft(spec)

    new_spec = str(crafted_obj)

    crafted_again = craft(new_spec)

    # in sktime, we would assert crafted_again == crafted_obj,
    # but sklearn estimators do not implement __eq__ as parameter equality
    assert type(crafted_obj) is type(crafted_again)
    assert str(crafted_again) == str(crafted_obj)


def test_imports_simple():
    """Check that imports produces correct import for simple estimator."""
    expected = "from sklearn.ensemble import RandomForestClassifier"
    assert imports(simple_spec) == expected


def test_imports_pipeline():
    """Check that imports produces correct imports for pipeline spec."""
    expected = (
        "from sklearn.ensemble import RandomForestClassifier\n"
        "from sklearn.model_selection import GridSearchCV\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.preprocessing import StandardScaler"
    )
    assert imports(pipeline_spec) == expected
