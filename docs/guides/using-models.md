# Using Models from AIoD

The AI-on-Demand (AIoD) metadata catalogue indexes thousands of ML models from platforms like
[Hugging Face](https://huggingface.co), [OpenML](https://openml.org), and [Zenodo](https://zenodo.org).
This guide walks you through finding, exploring, and using those models in your own Python projects.

!!! tip "Before you start"

    Make sure you have the SDK installed:

    ```bash
    pip install aiondemand
    ```

    New to the SDK? Check out the [Getting Started](../examples/getting-started.ipynb) example first.

---

## Browse Available Models

The simplest way to see what's available is to grab a list of models:

```python
import aiod

# Fetch the first 10 models (default)
models = aiod.ml_models.get_list()
models.head()
```

This returns a [pandas](https://pandas.pydata.org/) DataFrame with columns like `name`,
`platform`, `identifier`, `keyword`, `license`, and more.

### Filter by Platform

If you only care about models from a specific platform, pass the `platform` parameter:

```python
# Only Hugging Face models
hf_models = aiod.ml_models.get_list(platform="huggingface", limit=20)

# Only OpenML models
openml_models = aiod.ml_models.get_list(platform="openml", limit=20)
```

### Paginate Through Results

By default you get 10 results. Use `offset` and `limit` to page through larger collections:

```python
# Get models 50–74
models = aiod.ml_models.get_list(offset=50, limit=25)
```

### Check How Many Models Exist

Want a quick count instead of the actual data?

```python
total = aiod.ml_models.counts()
print(f"There are {total} models in the catalogue!")

# Broken down by platform
per_platform = aiod.ml_models.counts(per_platform=True)
print(per_platform)
# e.g. {'huggingface': 12345, 'openml': 678, ...}
```

---

## Search for Models

If you know *what* you're looking for, search is faster than browsing:

```python
# Find models related to "sentiment analysis"
results = aiod.ml_models.search("sentiment analysis")
results[["identifier", "name", "platform"]].head()
```

You can narrow the search to a specific field:

```python
# Search only in the model name
results = aiod.ml_models.search("bert", search_field="name")
```

Or restrict results to certain platforms:

```python
results = aiod.ml_models.search("image classification", platforms=["huggingface"])
```

---

## Get Details for a Specific Model

Every asset on AIoD has a unique **identifier** — a short string like `"mlmo_abc123XYZ"`.
Once you have one, you can pull up the full metadata:

```python
model = aiod.ml_models.get_asset(identifier="mlmo_abc123XYZ")
print(model)
```

The result is a pandas Series (or a Python dict if you prefer):

```python
# Get raw JSON instead of a pandas Series
model = aiod.ml_models.get_asset(identifier="mlmo_abc123XYZ", data_format="json")
print(model["name"])
print(model["description"])
print(model["keyword"])
```

### Look Up by Platform Identifier

If you know the model's ID on its original platform (for example, its Hugging Face repo name),
you can look it up without knowing the AIoD identifier:

```python
model = aiod.ml_models.get_asset_from_platform(
    platform="huggingface",
    platform_identifier="bert-base-uncased",
)
print(model)
```

---

## Download Model Content

Some models have downloadable files (weights, configs, etc.) registered in their metadata.
You can fetch them directly:

```python
raw_bytes = aiod.ml_models.get_content(identifier="mlmo_abc123XYZ")

# Save to disk
with open("model_file.bin", "wb") as f:
    f.write(raw_bytes)
```

If a model has multiple files attached, pick the one you want by its position in the
distribution list:

```python
# Download the second file (0-indexed)
raw_bytes = aiod.ml_models.get_content(
    identifier="mlmo_abc123XYZ",
    distribution_idx=1,
)
```

---

## Use an Indexed Model Directly

AIoD doesn't just store metadata — it also **indexes** models from popular ML libraries.
This means you can instantiate well-known estimators straight from the SDK, without writing
import boilerplate yourself.

Currently indexed libraries include:

| Library | Examples |
|---------|----------|
| **scikit-learn** | `RandomForestClassifier`, `LogisticRegression`, `PCA`, `Pipeline`, … |
| **XGBoost** | `XGBClassifier`, `XGBRegressor` |
| **mlxtend** | Various classifiers and transformers |
| **auto-sklearn** | `AutoSklearnClassifier` |

### Quick Example

```python
import aiod

# Get a scikit-learn RandomForestClassifier class, ready to use
RandomForest = aiod.get("RandomForestClassifier")

# Instantiate with your own parameters
clf = RandomForest(n_estimators=100, max_depth=5)

# Use it like you normally would
from sklearn.datasets import load_iris
X, y = load_iris(return_X_y=True)
clf.fit(X, y)
print(f"Accuracy: {clf.score(X, y):.2%}")
```

Under the hood, `aiod.get()` looks up the class in the AIoD model registry and returns
the actual Python class — no manual imports needed. This is especially helpful when you're
working with model specifications stored as strings (e.g., from experiment logs or pipelines).

### Build a Pipeline

Since `Pipeline` is also indexed, you can compose full workflows:

```python
Scaler = aiod.get("StandardScaler")
SVM = aiod.get("SVC")
Pipe = aiod.get("Pipeline")

pipe = Pipe(steps=[
    ("scaler", Scaler()),
    ("classifier", SVM(kernel="rbf")),
])
pipe.fit(X, y)
```

---

## Advanced Topics

!!! info "This section is optional"

    The sections below cover less common scenarios. Feel free to skip them if the basics
    above are all you need.

### Async Bulk Retrieval

When you need to fetch metadata for many models at once, async calls are significantly faster
than looping one-by-one:

```python
import asyncio

identifiers = ["mlmo_abc123", "mlmo_def456", "mlmo_ghi789"]

# Fetch all three in parallel
models = asyncio.run(
    aiod.ml_models.get_assets_async(identifiers)
)
print(models)
```

Or grab a large list asynchronously in batches:

```python
# Fetch 200 models, 25 at a time
models = asyncio.run(
    aiod.ml_models.get_list_async(limit=200, batch_size=25)
)
```

### Working with JSON Instead of DataFrames

Every function that returns a DataFrame accepts `data_format="json"` to give you
plain Python dicts/lists instead:

```python
models_list = aiod.ml_models.get_list(limit=5, data_format="json")
# This is a list of dicts
for m in models_list:
    print(m["name"], "—", m["platform"])
```

This is handy when you want to post-process the data yourself or feed it into
a non-pandas workflow.

### Changing the API Server

By default the SDK talks to the production API at `https://api.aiod.eu/`. If you're
running a local instance for development or testing, you can point the SDK elsewhere:

```python
import aiod

aiod.config.api_server = "http://localhost/"
aiod.config.auth_server = "http://localhost/aiod-auth/"
```

---

## What's Next?

- **Share your own models** → [Sharing Models to AIoD](sharing-models.md)
- **Try it interactively** → [Models Notebook](../examples/models.ipynb)
- **API reference** → [ML Models API](../api/assets/ml_models.md)
