# Authentication

To authenticate with AI-on-Demand, you need an account.
First navigate to [the web portal](https://aiod.eu/) and click `login`, you can choose
to use any authentication service and an account will be created automatically.

!!! danger "Never code your keys into a script"

    There is *never* a reason you should include your refresh token or client secret
    in a script directly. If you do, you may end up accidentally sharing your secrets
    when you share it with a colleague or in a public repository.
    
    Instead, you can use the built-in functionality to write or
    read tokens from file. Alternatively, you can use solutions such as 
    [`python-dotenv`](https://pypi.org/project/python-dotenv/) to use `.env` files 
    which can be easily overriden with environment variables.

## User Authentication Flow Example

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


## Bot Authentication Flow Example
In some rare cases, you may want to have a dedicated bot account. 
This is not for regular users, but may be granted to organisations to, for example:

 - Allow the creation of a connector which automatically syncs metadata from their platforms to AI-on-Demand (such as the OpenML connector)
 - The development of AI-on-Demand internal services which integrate through the REST API and need to perform certain authenticated requests.

???- question "Do I need this?"

    If you need to ask, then the answer is probably no. Use the user login flow described above.

If you want to obtain a `client_id` and `client_secret`, please reach out with a motivation on why you need it, 
what you will use it for, and why the user authentication flow is not sufficient.
With a `client_id` and `client_secret`, you can use that to authenticate as follows:

```toml title="secret.toml"
client_secret = "S2zo0zW6QMy8ffcqCozYbHkj0JajcWtQ"
```

```python
from pathlib import Path
import aiod

aiod.config.client_id = CLIENT_ID
token = aiod.authentication.Token.from_file(Path("secret.toml"))
# or:
# token = aiod.authentication.Token(client_secret=...)
aiod.authentication.set_token(token)
```

## Authentication Reference
::: aiod.authentication
    options:
      heading_level: 3
      show_signature: false
      toc_label: "Authentication Reference"
