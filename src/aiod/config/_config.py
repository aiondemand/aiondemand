from dataclasses import dataclass


@dataclass
class Config:
    api_base_url: str
    version: str


config = Config(
  api_base_url="https://api.aiod.eu/",
  version="v1",
)
