# Sharing Models to AIoD

So you've trained a model and want to make it discoverable on AI-on-Demand? Great!
This guide shows you how to register, update, and manage your model metadata on the
AIoD catalogue step by step.

!!! tip "Before you start"

    Make sure you have the SDK installed:

    ```bash
    pip install aiondemand
    ```

    You'll also need an AIoD account — it only takes a minute
    (see [Step 1](#step-1-create-an-account-and-log-in) below).

---

## Step 1: Create an Account and Log In

Head over to [aiod.eu](https://aiod.eu) and click **Login**. You can sign in with Google,
your institution, or another supported identity provider — no separate AIoD password needed.

Once you have an account, authenticate from Python:

```python
import aiod

# This opens a browser-based login flow
aiod.create_token(write_to_file=True)
```

The SDK will print a URL and a short code. Open the URL in your browser, enter the code,
and confirm. That's it — your token is saved to `~/.aiod/token.toml` so you won't need to
log in again until it expires.

!!! warning "Keep your token safe"

    Never paste your token directly into a script or commit it to version control.
    The `write_to_file=True` option stores it in a local file outside your project,
    which is the recommended approach.

You can verify everything works:

```python
user = aiod.get_current_user()
print(user)
# User(name='your-name', roles=('default-roles-aiod', ...))
```

---

## Step 2: Register a New Model

To share a model, you provide its **metadata** as a Python dictionary. At a minimum, you need
a `name`, but richer metadata makes your model easier for others to find and use:

```python
model_metadata = {
    "name": "My Sentiment Classifier",
    "description": {
        "plain": (
            "A fine-tuned BERT model for binary sentiment classification "
            "on product reviews. Trained on 50k labelled examples."
        )
    },
    "keyword": ["sentiment-analysis", "bert", "nlp", "text-classification"],
    "license": "apache-2.0",
    "alternate_name": ["sentiment-clf-v1"],
    "relevant_link": [
        {"name": "GitHub Repository", "url": "https://github.com/you/sentiment-clf"}
    ],
}

identifier = aiod.ml_models.register(metadata=model_metadata)
print(f"Registered! Your model identifier is: {identifier}")
```

The returned `identifier` is a unique string like `"mlmo_aBcDeFgH..."`. Save it — you'll
need it to update or delete the entry later.

### Verify It's There

Pull the metadata back from the server to confirm:

```python
model = aiod.ml_models.get_asset(identifier=identifier, data_format="json")
print(model["name"])
# My Sentiment Classifier
```

---

## Step 3: Update the Metadata

Noticed a typo? Want to add more keywords? Use `update()` to change specific fields
without touching the rest:

```python
aiod.ml_models.update(
    identifier=identifier,
    metadata={"keyword": ["sentiment-analysis", "bert", "nlp", "reviews", "pytorch"]},
)
```

The fields you don't mention stay the same.

### Replace All Metadata

If you want to completely overwrite the metadata (resetting any field you don't include
back to its default), use `replace()` instead:

```python
aiod.ml_models.replace(
    identifier=identifier,
    metadata={
        "name": "My Sentiment Classifier v2",
        "description": {
            "plain": "Updated v2 model with improved accuracy on product reviews."
        },
        "keyword": ["sentiment-analysis", "bert", "nlp", "v2"],
        "license": "apache-2.0",
    },
)
```

!!! note "`update` vs `replace` — which should I use?"

    - Use **`update()`** when you want to change a few fields and keep everything else.
    - Use **`replace()`** when you want to start fresh or ensure the metadata is exactly
      what you specify.

    Under the hood, `update()` fetches the current metadata, merges your changes, and
    sends the result. If you run into issues with `update()`, try the `replace()` approach
    shown below in the [manual merge recipe](#recipe-manual-merge-before-replace).

---

## Step 4: Delete a Model

If you registered something by accident, you can remove it:

```python
aiod.ml_models.delete(identifier=identifier)
```

!!! danger "Deletion is permanent"

    There is no undo. Once you delete a model entry, it's gone for good.

You can confirm it's been removed:

```python
try:
    aiod.ml_models.get_asset(identifier=identifier)
except KeyError as e:
    print(e)
    # "No ml_models with identifier '...' found."
```

---

## Tips for Good Metadata

Writing good metadata helps others discover and trust your model. Here are a few pointers:

| Field | Why it matters |
|-------|---------------|
| `name` | A clear, descriptive name (not "model_v3_final_FINAL") |
| `description` | What the model does, what data it was trained on, its intended use |
| `keyword` | Tags that help with search — think about what someone would search for |
| `license` | Let people know how they can use your model (e.g. `"mit"`, `"apache-2.0"`) |
| `relevant_link` | Link to a repo, paper, or demo so people can learn more |
| `alternate_name` | Other names the model might be known by |

!!! tip "Be a good citizen"

    The AIoD catalogue is a shared resource. Please:

    - **Use real data.** Don't upload test entries to the production catalogue. Use a
      [local server](https://github.com/aiondemand/aiod-rest-api) for experiments.
    - **Clean up mistakes.** If you accidentally register something, delete it promptly.
    - **Be descriptive.** The more context you provide, the more useful your contribution is.

---

## Recipes

### Recipe: Manual Merge Before Replace

If `update()` isn't behaving as expected, you can do the merge yourself:

```python
# 1. Fetch the current metadata
model = aiod.ml_models.get_asset(identifier=identifier, data_format="json")

# 2. Remove server-managed fields
del model["aiod_entry"]

# 3. Make your changes
model["keyword"].append("new-tag")
model["description"]["plain"] = "Updated description with more details."

# 4. Send it back
aiod.ml_models.replace(identifier=model["identifier"], metadata=model)
```

### Recipe: Register and Immediately Verify

A safe pattern for scripts that register models automatically:

```python
def register_and_verify(metadata):
    """Register a model and confirm it was saved correctly."""
    identifier = aiod.ml_models.register(metadata=metadata)

    # Pull it back from the server
    saved = aiod.ml_models.get_asset(identifier=identifier, data_format="json")
    assert saved["name"] == metadata["name"], "Name mismatch after registration!"

    print(f"✅ Model '{saved['name']}' registered as {identifier}")
    return identifier
```

---

## Advanced Topics

!!! info "This section is optional"

    The content below covers less common scenarios. Skip ahead to
    [What's Next?](#whats-next) if you don't need these right now.

### Using a Local Test Server

For development and testing, you can run the
[AIoD REST API](https://github.com/aiondemand/aiod-rest-api) locally and point the
SDK at it:

```python
import aiod

aiod.config.api_server = "http://localhost/"
aiod.config.auth_server = "http://localhost/aiod-auth/"

# You'll need a new token for the local auth server
aiod.create_token()
```

This way you can experiment freely without affecting the production catalogue.

### Bulk Registration

If you need to register many models at once, a simple loop works fine:

```python
models_to_register = [
    {"name": "Model A", "keyword": ["nlp"], "license": "mit"},
    {"name": "Model B", "keyword": ["vision"], "license": "apache-2.0"},
    {"name": "Model C", "keyword": ["tabular"], "license": "bsd-3-clause"},
]

registered_ids = []
for metadata in models_to_register:
    identifier = aiod.ml_models.register(metadata=metadata)
    registered_ids.append(identifier)
    print(f"  Registered: {metadata['name']} → {identifier}")

print(f"\nDone! Registered {len(registered_ids)} models.")
```

---

## What's Next?

- **Discover and use models** → [Using Models from AIoD](using-models.md)
- **Try it interactively** → [Models Notebook](../examples/models.ipynb)
- **API reference** → [ML Models API](../api/assets/ml_models.md)
- **Authentication details** → [Authentication](../api/authentication.md)
