import textwrap
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import tomlkit
from typing import Any, Callable, TypeAlias
import logging

logger = logging.getLogger(__file__)
AttributeObserver: TypeAlias = Callable[[str, Any, Any], None]


@dataclass
class Config:
    """Configuration for which servers and versions to use in connections.

    Notes
    -----
    For most users, there is generally no reason to modify these values other
    than `version`.
    For developers, it may be useful to connect to a test server or local instance
    by changing the `api_server` and `auth_server` addresses.

    Attributes
    ----------
    version: str
        The version prefix to use.
    api_server: str
        The URL of the metadata catalogue REST API.
    auth_server: str
        The authentication server to connect to.
    realm: str
        The realm in which the client matching the `client_id` resides.
    client_id: str
        The client ID used for authentication.

    """

    api_server: str = "https://api.aiod.eu/"
    version: str = "v2"
    auth_server: str = "https://auth.aiod.eu/aiod-auth/"
    realm: str = "aiod"
    client_id: str = "aiod-sdk"

    _observers: dict[str, set[AttributeObserver]] = field(
        default_factory=lambda: defaultdict(set),
        repr=False,
    )

    def subscribe(self, attribute: str, on_change: AttributeObserver) -> None:
        """Register a callback to be notified if the value of the `attribute` changes."""
        if on_change not in self._observers[attribute]:
            self._observers[attribute].add(on_change)

    def _store_to_file(self, attribute: str) -> None:
        if attribute not in dir(self):
            raise AttributeError("Cannot store ")
        user_config = tomlkit.loads(_user_config_file.read_text())
        if value := getattr(self, attribute):
            user_config[attribute] = value
        else:
            del user_config[attribute]

        _user_config_file.write_text(tomlkit.dumps(user_config))

    def __setattr__(self, key, value) -> None:
        old_value = getattr(self, key, None)
        super().__setattr__(key, value)

        if hasattr(self, "_observers"):
            for observer in self._observers[key]:
                observer(key, old_value, value)

    def _use_localhost(self, version: str = "latest"):
        """Set server URLs to localhost services. Convenience for developers."""
        self.version = version if version != "latest" else ""
        self.auth_server = "http://localhost/aiod-auth/"
        self.api_server = "http://localhost/"


def load_configuration(file: Path) -> Config:
    """Load a configuration from file.

    Parameters
    ----------
    file
        The TOML file that defines the configuration to load.

    Returns
    -------
    :
        The loaded configuration.

    """
    try:
        _user_config = tomlkit.loads(file.read_text())
    except tomlkit.exceptions.ParseError as e:
        _add_decode_error_note(file, e)
        raise

    global config
    for key, value in _user_config.items():
        setattr(config, key, value)
    return config


def _add_decode_error_note(file: Path, e: tomlkit.exceptions.ParseError) -> None:
    # Lines are 1-indexed and columns are 0-indexed
    e.add_note(
        textwrap.dedent(
            f"""
                Error reading configuration at {str(file)!r}: {e}
                File {str(file)!r}, line {e.line}:
                {file.read_text().splitlines()[e.line - 1]}
                {"^".rjust(e.col + 1)}
                """
        )
    )


config = Config()  # Modified through `load_configuration`
_user_config_file = Path("~/.aiod/config.toml").expanduser()
if _user_config_file.exists() and _user_config_file.is_file():
    load_configuration(_user_config_file)
    logger.info(f"Loaded configuration from {_user_config_file}: {config}.")
else:
    logger.info(
        f"No configuration file detected, using default configuration: {config}."
    )
