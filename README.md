# ForestryStock

Python command-line tools for compartment and harvesting records on a simulated eucalyptus estate.

## Requirements

Python 3.10 or newer. The current application has no third-party dependencies.

## Run

From the project directory:

```sh
python -m forestrystock summary --data data
python -m forestrystock harvest-area --data data
python -m unittest discover -s tests -v
```

The commands print JSON to standard output. Data errors are reported to standard error, with exit code 2.

## Input records

- `stands.csv`: compartment identifiers, locations, area, planting and site details.
- `harvest_events.csv`: dated harvesting operations and executed area.
- `harvest_lots.csv`: grouped physical log measurements for harvesting events.
- `boundary_logs.csv`: measurements of logs recorded at estate boundaries.
- `boundary_permits.csv`: movement authorizations for estate-boundary material.

These are simulated forestry records; they are not measurements from a production estate. Input CSV files are treated as immutable.

## Current functionality

- Summarizes compartments and area by region.
- Validates identifiers and numerical areas in stand and harvesting-event records.
- Reports the executed harvesting area and event count.

Physical harvest volume accounting and boundary movement reconciliation are not implemented yet.

## Code layout

- `forestrystock/data.py`: CSV schema checking and numeric field validation.
- `forestrystock/inventory.py`: stand register and harvest-area summaries.
- `forestrystock/cli.py`: command-line interface.
- `tests/`: automated tests.

## License

MIT License. Copyright (c) 2026 Carolina Gebler Crovador. See [LICENSE](LICENSE).

## Data use

The included CSVs contain synthetic examples for software testing and
reproducibility. They are not real operational, financial, geospatial,
or personal records. These example datasets are included under the same MIT
license as the code.
