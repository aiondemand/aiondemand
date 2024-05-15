from pathlib import Path
import configparser


config_file = Path(__file__).parent / "config.ini"
config = configparser.ConfigParser()
config.read(config_file)


def get_api_base_url() -> str:
    return config["api"]["base_url"]


def set_api_base_url(base_url: str):
    config["api"]["base_url"] = base_url
    write_config_file()


def get_api_schema_latest_version() -> str:
    return config["api"]["schema_latest_version"]


def get_keycloak_server_url() -> str:
    return config["keycloak"]["server_url"]


def get_keycloak_realm() -> str:
    return config["keycloak"]["realm"]


def get_keycloak_client_id() -> str:
    return config["keycloak"]["client_id"]


def set_authentication_server(server_url: str):
    config["keycloak"]["server_url"] = server_url
    write_config_file()


def show_config() -> dict[str, str]:
    config_dict = {}
    for section in config.sections():
        for key, item in config.items(section):
            config_dict[key] = item
    return config_dict


def write_config_file():
    with open(config_file, "w") as f:
        config.write(f)
