import argparse
import os

import dotenv


def load_env(filename: str) -> None:
    filepath = dotenv.find_dotenv(filename)
    if not filepath:
        print(f"Couldn't find .env file {filename!r}")
        return
    print(f"Found .env file: {filepath!r}")
    dotenv.load_dotenv(filepath, override=True)


def init_env(filenames: list[str]) -> None:
    for file in filenames:
        load_env(file)


def run_as_server() -> None:
    from . import wsgi

    app = wsgi()
    app.run(port=os.getenv("PORT", 6000))


def run_interactive() -> None:
    from . import init

    init()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="db_update")
    parser.add_argument(
        "env",
        action="store",
        default=[],
        nargs="*",
        help="additional .env file names to load, values will be overriden in the specified order",
    )
    parser.add_argument(
        "-it",
        "--interactive",
        action="store_true",
        help="initialize everything but don't run the server",
    )
    args = parser.parse_args()

    init_env(args.env)
    if args.interactive:
        run_interactive()
    else:
        run_as_server()
