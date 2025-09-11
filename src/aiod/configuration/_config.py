import textwrap
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re
import tomllib
import tomlkit
from typing import Any, Callable, TypeAlias
import logging

logger = logging.getLogger(__file__)
AttributeObserver: TypeAlias = Callable[[str, Any, Any], None]


@dataclass
class Config:
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
        if on_change not in self._observers[attribute]:
            self._observers[attribute].add(on_change)

    def store_to_file(self, attribute: str) -> None:
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


def load_configuration(file: Path) -> Config:
    try:
        _user_config = tomllib.loads(file.read_text())
    except tomllib.TOMLDecodeError as e:
        _add_decode_error_note(file, e)
        raise

    global config
    for key, value in _user_config.items():
        setattr(config, key, value)
    return config


def _add_decode_error_note(file: Path, e: tomllib.TOMLDecodeError) -> None:
    error_format = r"[\w\s]+ \(at line (\d+), column (\d+)\)"
    if not (match := re.match(error_format, e.args[0])):
        return

    raw_line_no, raw_column_no = match.groups()
    line_no, column_no = int(raw_line_no) - 1, int(raw_column_no) - 1
    e.add_note(
        textwrap.dedent(
            f"""
                Error reading configuration at {str(file)!r}: {e}
                File {str(file)!r}, line {raw_line_no}:
                {file.read_text().splitlines()[line_no]}
                {"^".rjust(column_no)}
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
