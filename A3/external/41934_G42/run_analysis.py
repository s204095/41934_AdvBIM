import ifcopenshell
from rules.utils import window_type_label, categorize_window
from rules.analysis import analyze_ifc
from collections import Counter

# -----------------------------
# CLAIMED WINDOWS DATABASE
# -----------------------------
CLAIMED_WINDOWS_DB = [
    {
        "name": "Window set: 2 x Udskifte fast vindue af træ, 1.188 x 1.188 mm, 3 lags; "
                "1 x Udskifte vendevindue af træ, 1.188 x 1.188, 3 lags",
        "width_mm": 1188,
        "height_mm": 1188,
        "material": "Wood",
        "count": 330,
        "units_per_window": 3,
        "price_per_window": 18005.60
    },
    # Add more claimed windows here if needed
]

# -----------------------------
# WINDOW PRICE DATABASE BY AREA
# -----------------------------
WINDOW_PRICE_DB = {
    "small": {"min_area": 0, "max_area": 1.5, "price_per_m2": 4000},
    "medium": {"min_area": 1.5, "max_area": 3.0, "price_per_m2": 6100},
    "large": {"min_area": 3.0, "max_area": float("inf"), "price_per_m2": 9000},
}

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def build_claimed_type_counts(claimed_windows, categorize_window):
    """
    Precompute claimed window counts by category.
    
    Parameters:
        claimed_windows (list): List of claimed window dicts
        categorize_window (function): Function to categorize window area
    
    Returns:
        Counter: Number of claimed windows per category
    """
    counts = Counter()
    for cw in claimed_windows:
        area = (cw["width_mm"] / 1000) * (cw["height_mm"] / 1000) * cw.get("units_per_window", 1)
        category = categorize_window(area)
        counts[category] += cw["count"]
    return counts


def main():
    # -----------------------------
    # OPEN IFC MODEL
    # -----------------------------
    model = ifcopenshell.open(r"C:\Users\MGS\Downloads\25-16-D-ARCH.ifc")

    # -----------------------------
    # ANALYZE WINDOWS
    # -----------------------------
    windows, type_counts, total_area, total_estimated_cost, match_results = analyze_ifc(model, CLAIMED_WINDOWS_DB)

    # -----------------------------
    # COMPUTE CLAIMED TOTALS
    # -----------------------------
    claimed_total_windows = sum(cw["count"] for cw in CLAIMED_WINDOWS_DB)
    claimed_total_area = sum(
        (cw["width_mm"]/1000) * (cw["height_mm"]/1000) * cw.get("units_per_window", 1) * cw["count"]
        for cw in CLAIMED_WINDOWS_DB
    )
    claimed_total_cost = sum(cw["count"] * cw["price_per_window"] for cw in CLAIMED_WINDOWS_DB)
    claimed_type_counts = build_claimed_type_counts(CLAIMED_WINDOWS_DB, categorize_window)

    # -----------------------------
    # SUMMARY OUTPUT
    # -----------------------------
    print("\n--- SUMMARY ---")
    print(f"IFC total windows: {len(windows)}")
    print(f"Claimed in report: {claimed_total_windows}")
    print("----------")
    print(f"IFC total cost: {total_estimated_cost:,.0f} DKK")
    print(f"Claimed total cost: {claimed_total_cost:,.0f} DKK")
    print("----------")
    print(f"IFC total window area: {total_area:.2f} m²")
    print(f"Claimed total window area: {claimed_total_area:.2f} m²")
    print("----------\n")

    print("--- WINDOW TYPES IN IFC ---")
    for category in ["small", "medium", "large"]:
        print(f"{window_type_label(category):<20}: {type_counts.get(category, 0)} windows")

    print("\n--- CLAIMED WINDOW TYPES ---")
    for category in ["small", "medium", "large"]:
        print(f"{window_type_label(category):<20}: {claimed_type_counts.get(category, 0)} windows")

    print("\n--- CLAIMED WINDOW MATCH ---")
    for result in match_results:
        cw = result["window"]
        print(f"Claimed window: {cw['name']}, {cw['width_mm']} x {cw['height_mm']} mm, Material: {cw['material']}")
        print(f"Matching windows by size: {result['size_match']}")
        print(f"Matching windows by material: {result['material_match']}")
        print(f"Matching windows by size AND material: {result['both_match']}")
        print(f"Claimed in report: {cw['count']}\n")


if __name__ == "__main__":
    main()
