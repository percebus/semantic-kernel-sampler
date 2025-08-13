"""load_dotenv files for the application."""

from dotenv import load_dotenv


def load_dotenv_files() -> None:
    """Load environment variables from .env* files."""
    _env_files = [
        ".env",  # Global
        ".env.local",
        ".env.ai.gpt.4o.local",
    ]

    for env_file in _env_files:
        print(f"Loading {env_file}...")  # TODO use logger
        if env_file:
            print(f"Loading {env_file}...")  # TODO use logger
            load_dotenv(env_file, override=True, verbose=True)
        else:
            print(f"Warning: {env_file} does not exist. Skipping.")  # TODO use logger
            continue
