from dataclasses import dataclass


@dataclass
class Config:
    api_base_url: str
    version: str
    auth_server_url: str
    realm: str
    client_id: str
    access_token: str | None = None
    refresh_token: str | None = None


config = Config(
    api_base_url="https://api.aiod.eu/",
    version="v1",
    auth_server_url="https://auth.aiod.eu/aiod-auth/",
    realm="aiod",
    client_id="aiod-sdk",
)
