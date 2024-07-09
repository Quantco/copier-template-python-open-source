import logging
import sys
from collections import namedtuple

Arguments = namedtuple("Arguments", ["script", "version", "stage"])

migrations: dict[str, list] = {}


def main(argv):
    logging.basicConfig(level=logging.INFO)

    args = Arguments._make(argv)
    migrations_current_version = migrations.get(args.version, [])

    logging.info(f"Running migrations for {args.version} in {args.stage} stage")

    for migration in migrations_current_version:
        if hasattr(migration, args.stage):
            getattr(migration, args.stage)()


if __name__ == "__main__":
    main(sys.argv)
