import pandas as pd
from aiod.utils._indexing._generic import get_contract_inhabitants
# Assuming you've defined this contract to match the old behavior
from sklearn.base import BaseEstimator
from aiod.contracts.sklearn.classification import SklearnClassificationContract
from sklearn.base import ClassifierMixin
# 1. THE OLD HARDCODED WAY
def old_way():
    from skbase.lookup import all_objects
    MODULES_IGNORE = ["array_api_compat", "tests", "experimental", "conftest"]
    return all_objects(
        object_types=ClassifierMixin,
        package_name="sklearn", # Smaller sub-pkg for speed
        return_names=True,
        modules_to_ignore=MODULES_IGNORE
    )

def new_way():
    return get_contract_inhabitants(
        contract_class=SklearnClassificationContract,
        package_name="sklearn",
        modules_to_ignore=["array_api_compat", "tests", "experimental", "conftest"]
    )

# --- THE COMPARISON ---
old_results = old_way()
new_results = new_way()

# Sort both lists by name to ensure order doesn't cause a false mismatch
old_results.sort(key=lambda x: x[0])
new_results.sort(key=lambda x: x[0])

# THE BIG TEST
print(f"Old count: {len(old_results)}")
print(f"New count: {len(new_results)}")

if old_results == new_results:
    print("SUCCESS: The outputs are IDENTICAL!")
else:
    # Show the difference
    old_names = set(n for n, o in old_results)
    new_names = set(n for n, o in new_results)
    print(f"Difference: {old_names.symmetric_difference(new_names)}")