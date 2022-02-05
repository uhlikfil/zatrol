import argparse

import dotenv

from zatrol.config import Config


def load_env(filename: str):
    filepath = dotenv.find_dotenv(filename)
    if not filepath:
        print(f"Couldn't find .env file {filename!r}")
        return
    print(f"Found .env file: {filepath!r}")
    dotenv.load_dotenv(filepath, override=True)


def init_env(filenames: list[str]):
    env_files = ["00-prod.env"]
    env_files.extend(filenames)
    for file in env_files:
        load_env(file)


def run_as_server():
    from . import wsgi

    app = wsgi()
    app.run(port=Config.server.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="db_update")
    parser.add_argument(
        "env",
        action="store",
        default=[],
        nargs="*",
        help="additional .env file names to load, values will be overriden in the specified order",
    )
    args = parser.parse_args()

    init_env(args.env)
    run_as_server()
