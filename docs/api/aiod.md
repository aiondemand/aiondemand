# Others 
The `aiod` top-level module also provides some functions.

::: aiod
    options:
        members:
            - counts
            - get

## Progress Indicators for Async Operations

Async functions like `get_assets_async()` and `get_list_async()` can provide progress 
feedback through Python's logging system.

To enable progress indicators, configure logging at INFO level:

```python
import logging
import aiod

# Enable progress output
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Now async operations show progress
datasets = await aiod.datasets.get_list_async(limit=1000, batch_size=50)
```

For more control, configure the `aiod.calls.calls` logger specifically:

```python
import logging

logger = logging.getLogger('aiod.calls.calls')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
```

### Example Output

When progress logging is enabled, you'll see output like:

```
Fetching 1000 datasets in 20 batches (batch_size=50)...
Progress: 2/20 datasets batches fetched (10%)
Progress: 4/20 datasets batches fetched (20%)
Progress: 6/20 datasets batches fetched (30%)
...
Progress: 20/20 datasets batches fetched (100%)
Successfully fetched 1000 datasets items
```