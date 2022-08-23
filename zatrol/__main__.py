import uvicorn

from . import create_app


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "zatrol:create_app",
        factory=True,
        debug=True,
        reload=True,
        env_file=".env",
    )


if __name__ == "__main__":
    main()
