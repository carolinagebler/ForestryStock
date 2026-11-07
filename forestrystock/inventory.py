"""Portfolio area summaries for forest compartments and harvest operations."""

from collections import Counter
from pathlib import Path

from .data import DataError, nonnegative_float, read_table


def load_stands(directory: str | Path) -> dict[str, dict[str, str]]:
    """Index stand records and reject repeated identifiers."""
    result = {}
    for record in read_table(directory, "stands.csv"):
        stand_id = record["stand_id"].strip()
        if not stand_id or stand_id in result:
            raise DataError(f"Missing or duplicate stand ID: {stand_id!r}")
        nonnegative_float(record["land_area_ha"], "land_area_ha")
        result[stand_id] = record
    return result


def portfolio_summary(directory: str | Path) -> dict:
    """Return simple portfolio area totals; no timber-volume estimates."""
    stands = load_stands(directory)
    regions = Counter()
    area = 0.0
    for record in stands.values():
        hectares = nonnegative_float(record["land_area_ha"], "land_area_ha")
        regions[record["region"]] += hectares
        area += hectares
    return {"stand_count": len(stands),
            "total_area_ha": round(area, 3),
            "area_by_region_ha": {key: round(val, 3) for key, val in sorted(regions.items())}}


def harvest_area_summary(directory: str | Path) -> dict:
    """Summarize recorded execution areas, without estimating wood volumes."""
    stands = load_stands(directory)
    events = read_table(directory, "harvest_events.csv")
    ids = set()
    totals = Counter()
    for row in events:
        event_id = row["event_id"].strip()
        if not event_id or event_id in ids:
            raise DataError(f"Missing or duplicate event ID: {event_id!r}")
        ids.add(event_id)
        unit = row["unit_id"].strip()
        if not unit.startswith("HU-") or unit[3:] not in stands:
            raise DataError(f"Event {event_id} references unknown stand: {unit!r}")
        totals[unit[3:]] += nonnegative_float(row["executed_area_ha"], "executed_area_ha")
    return {"event_count": len(events), "stand_count": len(totals),
            "executed_area_ha": round(sum(totals.values()), 3)}
