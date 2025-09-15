# Configuration

### Defaults
The default configuration is as follows:

- api_server: "https://api.aiod.eu/"
- version: "v2"
- auth_server: "https://auth.aiod.eu/aiod-auth/"
- realm: "aiod"
- client_id: "aiod-sdk"

### Updating the Configuration
The configuration can be updated simply by setting its attributes.

```python
import aiod
aiod.config.version = "v3"
```

Updating authentication settings (e.g., `auth_server`, `realm`, or `client_id`) 
will automatically unset the token. When changing it back, the previous token 
is not loaded automatically. Tokens are not invalidated.

## `Config`
::: aiod.configuration.Config
    options:
      members: no
      heading: "My Fancy Heading"


## `load_configuration`
::: aiod.configuration.load_configuration
    options:
      heading: "My Fancy Heading"
    
