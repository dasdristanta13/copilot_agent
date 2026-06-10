"""Migration helper script."""

import sys

import alembic.config


def main() -> None:
    """Run migration command."""
    # Run alembic with the arguments passed to the script
    alembic_args = sys.argv[1:]
    alembic.config.main(argv=alembic_args)


if __name__ == "__main__":
    main()
