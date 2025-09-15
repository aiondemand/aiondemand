# Authentication

To authenticate with AI-on-Demand, you need an account.
First navigate to [the web portal](https://aiod.eu/) and click `login`, you can choose
to use any authentication service and an account will be created automatically.

## Authentication Flow Example

Initiate the authentication process by calling `aiod.create_token`. Specifying 
`write_to_file=True` will ensure the obtained token is stored at `~/.aiod/token.toml`
and can be used in subsequent Python sessions.

```python title="Initiate Authentication"
import aiod
aiod.create_token(write_to_file=True)
```
The above command will output instructions to console on how to obtain a valid token, e.g.:

```bash title="Instructions in the Console"
Please authenticate using one of two methods:

  1. Navigate to https://auth.aiod.eu/aiod-auth/realms/aiod/device?user_code=ACBC-ARFZ
  2. Navigate to https://auth.aiod.eu/aiod-auth/realms/aiod/device and enter code ACBC-ARFZ

This workflow will automatically abort after 300 seconds.
```

This function will block until `timeout_seconds` have elapsed, or the
instructions have been followed successfully. After authentication, you can do authenticated
requests, such as getting information about the logged in user:

```python
aiod.get_current_user()
# returns: User(name='...', roles=('...', ...))
```

## Authentication Reference
::: aiod.authentication
    options:
      heading_level: 3
      show_signature: false
      toc_label: "Authentication Reference"
