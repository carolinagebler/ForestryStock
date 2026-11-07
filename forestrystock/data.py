"""CSV ingestion and field validation."""

import csv
from pathlib import Path


class DataError(ValueError):
    """Raised when a record cannot be loaded or validated."""


SCHEMAS = {
    "stands.csv": ("stand_id", "management_unit", "region", "land_area_ha"),
    "harvest_events.csv": ("event_id", "unit_id", "executed_area_ha", "executed_on"),
    "harvest_lots.csv": ("lot_id", "event_id", "unit_id", "log_count",
                         "mean_log_length_m", "mean_butt_underbark_cm",
                         "mean_top_underbark_cm"),
    "boundary_logs.csv": ("record_id", "physical_log_id", "claimed_permit_id",
                          "measured_length_m", "butt_underbark_cm",
                          "top_underbark_cm", "measured_at", "duplicate_of"),
    "boundary_permits.csv": ("permit_id", "event_id", "stand_id",
                             "valid_from", "valid_to", "authorized_material"),
}


def read_table(directory: str | Path, filename: str) -> list[dict[str, str]]:
    """Read the named project table, reporting missing columns and invalid files."""
    if filename not in SCHEMAS:
        raise DataError(f"Unknown dataset: {filename}")
    path = Path(directory) / filename
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = set(SCHEMAS[filename]) - headers
            if missing:
                raise DataError(f"{filename}: missing columns: {', '.join(sorted(missing))}")
            records = list(reader)
    except OSError as exc:
        raise DataError(f"Cannot read {path}: {exc}") from exc
    if any(None in item for item in records):
        raise DataError(f"{filename}: inconsistent number of CSV fields")
    return records


def nonnegative_float(value: str, field: str) -> float:
    """Parse a finite non-negative numeric quantity."""
    from math import isfinite
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise DataError(f"Invalid {field}: {value!r}") from exc
    if not isfinite(result) or result < 0:
        raise DataError(f"Invalid {field}: {value!r}")
    return result
