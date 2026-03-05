# Issue #158 Investigation: AIoD Server Down

## Current Status

The AIoD server (api.aiod.eu) is currently down, likely due to handover to DeployAI. This investigation documents the current state and proposes solutions.

## What's Already Done

✅ **PR #157 merged**: Server integration tests are commented out in `.github/workflows/tests.yml`
- The workflow now skips `pytest -m server tests`
- Local and package tests continue to run normally
- CI is no longer blocked by server downtime

## Affected Components

### 1. Integration Tests
**File**: `tests/test_integration.py`
- Contains 1 test marked with `@pytest.mark.server()`
- Test: `test_get_dataset_list_from_default_version_server`
- Tests both default and latest API versions

### 2. Server Configuration
**File**: `src/aiod/configuration/_config.py`
- API Server: `https://api.aiod.eu/`
- Auth Server: `https://auth.aiod.eu/aiod-auth/`
- Default version: `v2`
- Includes `_use_localhost()` method for local development

### 3. Pytest Configuration
**File**: `pyproject.toml`
```toml
[tool.pytest.ini_options]
markers = [
    "server: connects to an AIoD server",
]
addopts = "-m 'not server'"
```
Server tests are skipped by default unless explicitly run with `pytest -m server`

## Long-Term Solutions

### Option 1: Mock-Based Testing (Recommended)
**Pros:**
- No dependency on external servers
- Fast and reliable
- Can test edge cases and error conditions
- Works offline

**Implementation:**
- Use `responses` library (already in dev dependencies)
- Create fixtures with sample API responses
- Mock both API and auth endpoints

**Example:**
```python
import responses
import pytest

@responses.activate
def test_get_dataset_list_mocked():
    responses.add(
        responses.GET,
        "https://api.aiod.eu/v2/datasets",
        json={"results": [...]},
        status=200
    )
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
```

### Option 2: Dedicated Test Server
**Pros:**
- Tests real server behavior
- Catches integration issues

**Cons:**
- Requires infrastructure
- Maintenance overhead
- Can still fail if test server is down

**Implementation:**
- Set up a separate test instance
- Use environment variables to configure test server URLs
- Add health checks before running tests

### Option 3: Conditional Integration Tests
**Pros:**
- Keeps real integration tests
- Doesn't block CI when server is down

**Implementation:**
```python
import pytest
import requests

def is_server_available():
    try:
        response = requests.get("https://api.aiod.eu/health", timeout=5)
        return response.status_code == 200
    except:
        return False

@pytest.mark.server()
@pytest.mark.skipif(not is_server_available(), reason="AIoD server not available")
def test_get_dataset_list_from_server():
    # test implementation
```

### Option 4: Hybrid Approach (Best)
Combine multiple strategies:
1. **Unit tests with mocks** - Fast, reliable, run on every commit
2. **Integration tests with health checks** - Run only when server is available
3. **Scheduled integration tests** - Run nightly or weekly against production
4. **Local development mode** - Use `config._use_localhost()` for development

## Recommended Action Plan

### Phase 1: Immediate (Current)
- [x] Comment out server tests in CI (PR #157)
- [ ] Document server status in README
- [ ] Add note about running integration tests manually

### Phase 2: Short-term (1-2 weeks)
- [ ] Implement mock-based tests for critical paths
- [ ] Add server health check utility
- [ ] Update integration tests to skip gracefully when server is down

### Phase 3: Long-term (1-2 months)
- [ ] Set up dedicated test server or use mocks exclusively
- [ ] Implement scheduled integration test workflow
- [ ] Add monitoring/alerting for server availability
- [ ] Document testing strategy in contributing guide

## Files to Modify

1. **tests/test_integration.py** - Add mocked versions of tests
2. **tests/conftest.py** - Add fixtures for mocked responses
3. **.github/workflows/tests.yml** - Add scheduled integration test job
4. **docs/developer_setup.md** - Document testing strategy
5. **docs/README.md** - Add note about server status

## Related Issues

- Issue #158: This investigation
- PR #157: Temporary fix (merged)
- [AIOD-rest-api#717](https://github.com/aiondemand/AIOD-rest-api/issues/717): Server downtime issue
