# AIoD User Guide: Using and ML Models

This guide demonstrates how to use indexed machine learning models and datasets through the AI-on-Demand platform. Users can access models and datasets from popular machine learning libraries and platforms.

The key entry point is `aiod.get()`:

```python
import aiod

# Get a model
clf = aiod.get("RandomForestClassifier")

# Get a dataset from openml
dataset = aiod.get("openml://31")

# Get an instance with hyperparameters
pipeline = aiod.get("Pipeline(steps=[('scaler', StandardScaler()), ('clf', RandomForestClassifier(n_estimators=100))])")
```

## Indexed Libraries

AIoD indexes estimators from the following popular machine learning libraries and scikit-learn compatible packages (see [issue #57](https://github.com/aiondemand/aiondemand/issues/57)):

- scikit-learn
- LightGBM
- CatBoost
- mlxtend
- feature-engine
- scikit-lego
- imbalanced-learn

All indexed estimators can be accessed uniformly through `aiod.get()`.

## Retrieving Models

### 1a Getting Model Classes

Access any indexed model class using its name. AIoD automatically handles finding the estimator across indexed libraries:

```python
import aiod

# Scikit-learn classifiers and transformers
RandomForestClassifier = aiod.get("RandomForestClassifier")
LGBMClassifier = aiod.get("LGBMClassifier")
CatBoostClassifier = aiod.get("CatBoostClassifier")
```

If a required library is not installed, AIoD will raise an error message:

```
ModuleNotFoundError: scikit-learn is required. Install it with: pip install scikit-learn
```

### 1b Instantiating Models with Hyperparameters

Create model instances directly with specific hyperparameters:

```python
import aiod

# Simple classifier with hyperparameters
rf = aiod.get("RandomForestClassifier(n_estimators=100")

# Preprocessing pipeline
imputer = aiod.get("SimpleImputer(strategy='mean')")
scaler = aiod.get("StandardScaler()")
```

### 1c Building Complex Pipelines

Compose multi-step pipelines from string specifications:

```python
import aiod

pipeline = aiod.get("""
Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100))
])
""")

print(type(pipeline))
# <class 'sklearn.pipeline.Pipeline'>
```

### 1d Executable Specifications

For complex scenarios, use full Python specifications with multiple steps:

```py
import aiod

spec = """
pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100))])
cv = KFold(n_splits=5, shuffle=True, random_state=42)

return GridSearchCV(
    estimator=pipe,
    param_grid=[{
        "classifier__max_depth": [5, 10],
        "classifier__min_samples_split": [2, 5],
    },
    ],
    cv=cv,
    )
"""

print(aiod.get(spec))
```

## Loading Datasets

AIoD provides unified access to datasets from providers.

### 2a Getting Datasets from scikit-learn

```python
import aiod

# Get a dataset
iris_data = aiod.get("sklearn:iris")

# Load the data
X, y = iris_data.load()

print(X.shape, y.shape)
```

Available scikit-learn datasets: `iris`, `wine`, `digits`, `diabetes`, `linnerud`, `breast_cancer`

### 2b Getting Datasets from OpenML

Load any dataset from the OpenML platform by ID or name. OpenML is a comprehensive repository with thousands of publicly available datasets for machine learning research and benchmarking:

```python
import aiod

# By dataset ID
dataset = aiod.get("openml://31")

# By dataset name
dataset = aiod.get("openml://credit-g")

print(type(dataset))
# <class 'openml.OpenMLDataset'>

# Access the data using OpenML API
X, y, _, _ = dataset.get_data(
    target=dataset.default_target_attribute
)

print(X.shape, y.shape)
```

### 2c Getting Datasets from sktime

Load time series datasets:

```python
import aiod

airline_data = aiod.get("sktime:airline")
data = airline_data.load()

print(data.shape)
```

Available sktime datasets: `airline`, `gunpoint`, `arrow_head`, `austrailer`, `basic_motions`, `italy_power_demand`, `japanese_vowels`, and more.

## Model Catalogues

A catalogue is a curated collection of machine learning components. These components can be estimators, datasets, and metrics.

```python
import aiod

catalogue = aiod.get("DelgadoClassificationCatalogue()")

print(catalogue.fetch(object_type="all"))
```

## Model Benchmarking

### 3a Basic Benchmarking

```python
import aiod
from aiod.benchmarking import ClassificationBenchmark

benchmark = ClassificationBenchmark()

benchmark.add("RandomForestClassifier(n_estimators=100)")
benchmark.add("XGBClassifier(n_estimators=100)")
benchmark.add("LGBMClassifier(n_estimators=100)")

benchmark.add("SklearnDatasets(name='iris', return_X_y=True)").load()
benchmark.add("KFold(n_splits=2, shuffle=True, random_state=42)")
benchmark.add("accuracy_score")

results = benchmark.run()
```

Output:

| Model                  | Organization/Library | Accuracy | Accuracy Rank |
|------------------------|--------------|----------|---------------|
| RandomForestClassifier | scikit-learn   | 0.9733   | 1             |
| XGBClassifier          | xgboost | 0.9533   | 2             |
| LGBMClassifier         | lightgbm    | 0.9467   | 3             |

### 3b Reproducing and Extending Experiments

Reproduce models from a published paper and add your own:

```python
import aiod
from aiod.benchmarking import ClassificationBenchmark

benchmark = ClassificationBenchmark()
catalogue = aiod.get("DelgadoClassificationCatalogue()")

# adds all the estimators from the catalogue (reproduce the experiment)
benchmark.add(catalogue)

# add another estimaator (extend the experiment)
benchmark.add("LogisticRegression()")

# add tasks
benchmark.add("SklearnDatasets(name='iris', return_X_y=True)").load()
benchmark.add("KFold(n_splits=2, shuffle=True, random_state=42)")
benchmark.add("accuracy_score")

benchmark.run()
```

Output:

| Model                  | Organization/Library | Accuracy | Accuracy Rank |
|------------------------|--------------|----------|---------------|
| RandomForestClassifier | scikit-learn   | 0.9733   | 1             |
| XGBClassifier          | xgboost | 0.9533   | 2             |
| LGBMClassifier         | lightgbm    | 0.9467   | 3             |
| LogisticRegression     | scikit-learn | 0.9343 | 4 |

Notice that we also have a fourth column now for `LogisticRegression`, that we added on top of the estimators from the catalogues, so we can see how _our_ added estimator/algorithm performs as compared to the algorithms in a given catalogue (or e.g. a NeurIPS paper)


## Sharing Your Models

Your model should Have sklearn-compatible estimators

AIoD has already index for popular libraries (see [issue #57](https://github.com/aiondemand/aiondemand/issues/57)):

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
