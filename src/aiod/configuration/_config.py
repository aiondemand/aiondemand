from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, TypeAlias


AttributeObserver: TypeAlias = Callable[[str, Any, Any], None]


@dataclass
class Config:
    api_base_url: str
    version: str
    auth_server_url: str
    realm: str
    client_id: str
    access_token: str | None = None
    refresh_token: str | None = None

    _observers: dict[str, set[AttributeObserver]] = field(default_factory=lambda: defaultdict(set))

    def subscribe(self, attribute: str, on_change: AttributeObserver):
        if on_change not in self._observers[attribute]:
            self._observers[attribute].add(on_change)

    def __setattr__(self, key, value):
        old_value = getattr(self, key, None)
        super().__setattr__(key, value)

        if hasattr(self, "_observers"):
            for observer in self._observers[key]:
                observer(key, old_value, value)


config = Config(
    api_base_url="https://api.aiod.eu/",
    version="v1",
    auth_server_url="https://auth.aiod.eu/aiod-auth/",
    realm="aiod",
    client_id="aiod-sdk",
)
