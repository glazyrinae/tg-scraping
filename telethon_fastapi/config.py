from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class Config:
    db: DatabaseConfig
    api_id: str
    api_hash: str
    session_path: str
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DatabaseConfig(database_url=env("DATABASE_URL")),
        api_id=env("API_ID"),
        api_hash=env("API_HASH"),
        session_path=env("SESSION_PATH"),
        debug=env.bool("DEBUG", default=False),
    )
