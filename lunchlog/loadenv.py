import os
import shutil
from django.core.management.utils import get_random_secret_key


def write_dot_env_file(root: str, env_file: str, mode: str) -> None:
    settings = get_settings()
    shutil.copyfile(f"{root}/.env-example", f"{root}/.env")

    with open(env_file, mode) as f:
        for k, v in settings.items():
            f.write(f"{k.upper()}={v}\n")


def get_settings() -> dict:
    return {
        "SECRET_KEY": get_random_secret_key(),
        "DATABASE_URL": "postgres://postgres:postgres@db:5432/postgres",
        "ALLOWED_HOSTS": "*",
    }


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(root, ".env")

    if not os.path.isfile(env_file):
        write_dot_env_file(root, env_file, "w")
    else:
        write_dot_env_file(root, env_file, "a")


if __name__ == "__main__":
    main()
