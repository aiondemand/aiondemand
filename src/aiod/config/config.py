import pathlib
import tomllib

with open(pathlib.Path(__file__).parent / "config.toml", "rb") as fh:
    CONFIG = tomllib.load(fh)

KEYCLOAK_CONFIG = CONFIG.get("keycloak", {})
