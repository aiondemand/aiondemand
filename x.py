
from aiod.utils._indexing._preindex_sklearn import _all_sklearn_estimators_locdict


print(_all_sklearn_estimators_locdict(package_name="lightgbm", serialized=False))