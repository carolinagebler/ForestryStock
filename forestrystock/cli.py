"""Command-line utilities for forestry records."""

import argparse
import json
import sys
from pathlib import Path

from .data import DataError
from .inventory import portfolio_summary, harvest_area_summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="forestrystock")
    parser.add_argument("command", choices=["summary", "harvest-area"])
    parser.add_argument("--data", type=Path, default=Path("data"), help="CSV input directory")
    args = parser.parse_args(argv)
    try:
        result = portfolio_summary(args.data) if args.command == "summary" else harvest_area_summary(args.data)
    except DataError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
