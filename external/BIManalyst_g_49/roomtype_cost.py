import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


# =======================================================
# CONFIG LOADING FUNCTIONS
# =======================================================

def load_room_types(config_dir: str | Path) -> List[str]:
    """Load list of room types from room_types.json."""
    config_dir = Path(config_dir)
    with open(config_dir / "room_types.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_space_keywords(config_dir: str | Path) -> Dict[str, List[str]]:
    """Load mapping: room_type -> [keywords] from space_keywords.json."""
    config_dir = Path(config_dir)
    with open(config_dir / "space_keywords.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_cost_rates(config_dir: str | Path) -> Dict[str, float]:
    """Load mapping: cost_group -> price_per_m2 from cost_rates.json."""
    config_dir = Path(config_dir)
    with open(config_dir / "cost_rates.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_weights_matrix(config_dir: str | Path, filename: str) -> Dict[str, Dict[str, float]]:
    """
    Load full weight matrix from JSON.

    Expected structure:
    {
      "ROOM_TYPE": {
        "COST_GROUP": weight,
        ...
      },
      ...
    }
    """
    config_dir = Path(config_dir)
    with open(config_dir / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# =======================================================
# CLASSIFICATION FUNCTIONS
# =======================================================

def _normalize(text: str) -> str:
    """Lowercase a string and remove most punctuation."""
    t = text.lower()
    t = re.sub(r"[^a-zæøå0-9]+", " ", t)
    return t.strip()


def classify_space_name(
    name: str,
    room_types: List[str],
    space_keywords: Dict[str, List[str]],
) -> str:
    """
    Classify a single space name into a room type using keyword matching.

    Returns:
      room_type string or "UNCLASSIFIED".
    """
    if not name:
        return "UNCLASSIFIED"

    norm = _normalize(name)
    hits: List[str] = []

    for rt in room_types:
        for kw in space_keywords.get(rt, []):
            if kw in norm:
                hits.append(rt)
                break

    if not hits:
        if "room" in norm or "rum" in norm:
            # simple fallback
            return "OFFICE" if "OFFICE" in room_types else "UNCLASSIFIED"
        return "UNCLASSIFIED"

    return hits[0]


def classify_all_spaces(
    areas_spaces: Dict[str, float],
    room_types: List[str],
    space_keywords: Dict[str, List[str]],
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Classify all spaces and aggregate area per room type.

    Returns:
      (area_by_roomtype, unclassified_spaces)
    """
    area_by_roomtype: Dict[str, float] = defaultdict(float)
    unclassified: Dict[str, float] = {}

    for raw_name, area in areas_spaces.items():
        rt = classify_space_name(raw_name, room_types, space_keywords)
        if rt == "UNCLASSIFIED":
            unclassified[raw_name] = float(area)
        else:
            area_by_roomtype[rt] += float(area)

    return area_by_roomtype, unclassified


# =======================================================
# COST ALLOCATION FUNCTIONS
# =======================================================

def allocate_costs(
    area_by_roomtype: Dict[str, float],
    total_area: float,
    room_types: List[str],
    cost_rates: Dict[str, float],
    weights: Dict[str, Dict[str, float]],
) -> Dict:
    """
    Allocate cost from cost groups to room types.

    total_area:
      basis for cost_rates (usually sum of all space areas).

    Returns dict with:
      - total_cost
      - total_unit_price
      - per_room_type
      - per_cost_group
    """
    total_cost = 0.0
    room_costs = {rt: 0.0 for rt in room_types}
    per_group: Dict[str, Dict] = {}

    for cost_group, rate in cost_rates.items():
        group_total = float(rate) * float(total_area)
        total_cost += group_total

        # weighted demand per room
        demand: Dict[str, float] = {}
        for rt in room_types:
            area = float(area_by_roomtype.get(rt, 0.0))
            w = float(weights.get(rt, {}).get(cost_group, 1.0))
            demand[rt] = area * w

        sum_demand = sum(demand.values()) or 1.0

        allocation_rt: Dict[str, Dict] = {}
        for rt in room_types:
            share = demand[rt] / sum_demand
            allocated = group_total * share
            room_costs[rt] += allocated
            allocation_rt[rt] = {
                "share": share,
                "allocated_cost": allocated,
            }

        per_group[cost_group] = {
            "rate_per_m2": rate,
            "total_cost": group_total,
            "allocation": allocation_rt,
        }

    total_unit_price = total_cost / total_area if total_area > 0 else 0.0

    per_room_type: Dict[str, Dict] = {}
    for rt in room_types:
        area = float(area_by_roomtype.get(rt, 0.0))
        rcost = room_costs[rt]
        unit = rcost / area if area > 0 else 0.0
        per_room_type[rt] = {
            "area": area,
            "allocated_cost": rcost,
            "unit_price": unit,
        }
    print("Cost Allocation Completed")
    return {
        "total_cost": total_cost,
        "total_unit_price": total_unit_price,
        "per_room_type": per_room_type,
        "per_cost_group": per_group,
    }


# =======================================================
# HIGH-LEVEL PIPELINE
# =======================================================

def process_json(
    input_path: str | Path,
    output_path: str | Path,
    config_dir: str | Path = "data",
    weights_override_path: str | None = None,
) -> None:
    """
    Full pipeline:
      1) Load config (room types, keywords, cost rates, weights)
      2) Read input JSON and get "Area of spaces"
      3) Classify spaces and aggregate area per room type
      4) Compute total area and allocate costs
      5) Write summary JSON to output_path
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    config_dir = Path(config_dir)

    # 1) Load config
    room_types = load_room_types(config_dir)
    space_keywords = load_space_keywords(config_dir)
    cost_rates = load_cost_rates(config_dir)

    # default full weights file (complete matrix)
    default_weights_file = "weights_default.json"
    weights_file = weights_override_path or default_weights_file
    weights = load_weights_matrix(config_dir, weights_file)


    # 2) Read input JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    areas_spaces: Dict[str, float] = data.get("Area of spaces", {})

    # 3) Classify spaces
    area_by_roomtype, unclassified = classify_all_spaces(
        areas_spaces,
        room_types,
        space_keywords,
    )

    # 4) Compute total area, allocate costs
    total_area = sum(areas_spaces.values())
    allocation = allocate_costs(
        area_by_roomtype=area_by_roomtype,
        total_area=total_area,
        room_types=room_types,
        cost_rates=cost_rates,
        weights=weights,
    )

    summary = {
        "total_area_basis": total_area,
        "calculated_total_cost": allocation["total_cost"],
        "calculated_unit_price": allocation["total_unit_price"],
        "per_room_type": allocation["per_room_type"],
        "per_cost_group": allocation["per_cost_group"],
        "unclassified_spaces": unclassified,
        "weights_source": weights_file,
    }

    # 5) Write output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)


# =======================================================
# CLI ENTRY POINT
# =======================================================

def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments for CLI use."""
    parser = argparse.ArgumentParser(
        description="Allocate building cost to room types from space areas."
    )
    parser.add_argument("--input", required=True, help="Path to input JSON.")
    parser.add_argument("--output", required=True, help="Path to output JSON.")
    parser.add_argument(
        "--config-dir",
        default="data",
        help="Directory with config JSON files (room_types, keywords, cost_rates, weights).",
    )
    parser.add_argument(
        "--weights",
        default=None,
        help="Optional custom weights JSON filename (inside config-dir). "
             "Must contain full matrix room_type -> cost_group -> weight. "
             "If omitted, weights_default.json is used.",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry: read args, run process_json."""
    args = _parse_args()
    process_json(
        input_path=args.input,
        output_path=args.output,
        config_dir=args.config_dir,
        weights_override_path=args.weights,
    )


if __name__ == "__main__":
    main()
