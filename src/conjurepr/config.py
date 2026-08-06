"""Configuration loading for the Phase 2 service."""

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 8765


@dataclass(frozen=True)
class PathsConfig:
    jobs: Path = Path("./runs")
    cache: Path = Path("./cache")
    logs: Path = Path("./logs")
    state: Path = Path("./state")


@dataclass(frozen=True)
class Config:
    server: ServerConfig = ServerConfig()
    paths: PathsConfig = PathsConfig()


def load_config(path: str | Path | None = None) -> Config:
    """Load the server settings from TOML, or use safe local defaults."""

    if path is None:
        return Config()

    config_path = Path(path).expanduser()
    with config_path.open("rb") as config_file:
        raw = tomllib.load(config_file)

    server = raw.get("server", {})
    paths = raw.get("paths", {})

    def configured_path(name: str, default: str) -> Path:
        return Path(paths.get(name, default)).expanduser()

    return Config(
        server=ServerConfig(
            host=str(server.get("host", "127.0.0.1")),
            port=int(server.get("port", 8765)),
        ),
        paths=PathsConfig(
            jobs=configured_path("jobs", "./runs"),
            cache=configured_path("cache", "./cache"),
            logs=configured_path("logs", "./logs"),
            state=configured_path("state", "./state"),
        ),
    )
