import os, json
import ifcopenshell
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

for path in [project_root, os.path.join(project_root, "external")]:
    if path not in sys.path:
        sys.path.append(path)   

# Analyst group imports here
from external.BIManalyst_g_48.rules import SpaceRequirement


def _ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)



def get_project_overview(model, output_path="data/project_overview.json"):
    proj  = (model.by_type("IfcProject") or [None])[0]
    site  = (model.by_type("IfcSite") or [None])[0]
    bldg  = (model.by_type("IfcBuilding") or [None])[0]

    # header
    hdr = model.wrapped_data.header
    file_name = hdr.file_name
    file_desc = hdr.file_description

    data = {
        "file": {
            "schema": model.schema,
            "name": getattr(file_name, "name", None),
            "time_stamp": getattr(file_name, "time_stamp", None),
            "author": (file_name.author[0] if getattr(file_name, "author", None) else None),
            "organization": (file_name.organization[0] if getattr(file_name, "organization", None) else None),
            "description": (file_desc.description[0] if getattr(file_desc, "description", None) else None),
        },
        "project": {"name": getattr(proj, "Name", None), "global_id": getattr(proj, "GlobalId", None)},
        "site":    {"name": getattr(site, "Name", None), "global_id": getattr(site, "GlobalId", None)},
        "building":{"name": getattr(bldg, "Name", None), "global_id": getattr(bldg, "GlobalId", None)},
    }

    _ensure_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data




def get_element_counts(model, output_path="data/element_counts.json"):
    TYPES = ["IfcWall", "IfcWallStandardCase", "IfcSlab", "IfcBeam", "IfcColumn", "IfcDoor", "IfcWindow"]
    counts = {t: len(model.by_type(t)) for t in TYPES}
    # merge standard case walls
    if counts.get("IfcWallStandardCase"):
        counts["IfcWall"] = counts.get("IfcWall", 0) + counts["IfcWallStandardCase"]
        del counts["IfcWallStandardCase"]

    data = {"counts": counts, "total_elements": sum(counts.values())}
    _ensure_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data




def get_ftf_heights(model, output_path="data/ftf_heights.json"):
    storeys = model.by_type("IfcBuildingStorey")
    rows = []
    total = 0.0

    for s in storeys:
        elev = getattr(s, "Elevation", 0.0) or 0.0
        rows.append({"Name": getattr(s, "Name", None), "Elevation": float(elev), "GlobalId": s.GlobalId})

    rows.sort(key=lambda x: x["Elevation"])

    heights = []
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        ftf = b["Elevation"] - a["Elevation"]
        heights.append({"From": a["Name"], "To": b["Name"], "Height": round(ftf, 3)})
        total += abs(ftf)

    data = {"Storeys": rows, "FloorToFloorHeights": heights, "TotalBuildingHeight_m": round(total, 3)}

    _ensure_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data
