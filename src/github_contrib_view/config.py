"""Set up the Configuration file functionality."""

from simple_toml_settings import TOMLSettings


class Settings(TOMLSettings):
    """Define the settings class."""

    username: str
    token: str
    ascii: bool = False
    summary: bool = True


settings = Settings.get_instance(
    "ghcview",
    xdg_config=True,
)
