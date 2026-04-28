# Library Indexing and Model Sharing

## Sharing Your Models

Your model should have sklearn-compatible estimators.

AIoD has already indexed popular libraries (see [issue #57](https://github.com/aiondemand/aiondemand/issues/57)):

### Currently Indexed:
- [scikit-learn](https://github.com/aiondemand/aiondemand/issues/47)
- [lightgbm](https://github.com/aiondemand/aiondemand/issues/82)
- [catboost](https://github.com/aiondemand/aiondemand/issues/79)
- [mlxtend](https://github.com/aiondemand/aiondemand/issues/83)
- [feature-engine](https://github.com/aiondemand/aiondemand/issues/193)
- [scikit-lego](https://github.com/aiondemand/aiondemand/issues/91)
- [imbalanced-learn](https://github.com/aiondemand/aiondemand/issues/114)

To get a new library indexed:

1. **Open an issue** requesting indexing for your library
2. **Create an index definition** mapping estimator names to import paths
3. **Add tests** demonstrating all estimators can be retrieved and instantiated
4. **Submit a pull request** to integrate into AIoD

## Generating Scitype Mappings

When adding a new library to AIoD, you need to map each estimator to its scitype (e.g., "classifier", "transformer", "regressor", "outlier_detector", "sampler", etc.).

Instead of manually guessing scitypes, you can generate them automatically by using `_generate_sklearn_objs_by_type` function from `src/aiod/utils/_indexing/_preindex_sklearn.py`

```python
type_of_obj = _generate_sklearn_types_of_obj('feature_engine')

for key in sorted(type_of_obj.keys()):
    value = type_of_obj[key]
    
    if isinstance(value, str):
        val_str = f'"{value}"'
    else:
        val_str = "[" + ", ".join(f'"{v}"' for v in value) + "]"
        
    print(f'"{key}": {val_str},')
```

- Output:
```sh
"AddMissingIndicator": "transformer",
"ArbitraryDiscretiser": "transformer",
"ArbitraryNumberImputer": "transformer",
"ArbitraryOutlierCapper": "transformer",
"ArcSinhTransformer": "transformer",
"ArcsinTransformer": "transformer",
"BoxCoxTransformer": "transformer",
"CategoricalImputer": "transformer",
...
```

This approach is more reliable than manual type assignment because it:
- Inspects actual class inheritance hierarchies
- Detects multiple types when an estimator inherits from multiple mixins
- Automatically adapts to library updates
- Reduces the chance of type mapping errors
