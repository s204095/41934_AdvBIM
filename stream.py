import json
from pathlib import Path
import tempfile
import ifcopenshell
import streamlit as st





# Import your submodules
from external.BIManalyst_g_48.A3 import A3_Tool        # submodule for area extraction 
from  external.BIManalyst_g_49 import roomtype_cost as rtc  # submodule of cost estimation

#Increase max file size
st.set_page_config(page_title="OpenBIM 🧰", layout="wide")
st.session_state["MAX_FILE_SIZE"] = 1024 * 1024 * 1024  # 1 GB

# --- Upload Widget ---
uploaded_ifc = st.file_uploader(
    "Upload IFC file",
    type=["ifc"],
    help="Select an IFC model to continue.",
)


    # --- Optional: custom weights JSON ---
uploaded_weights = st.file_uploader(
        "Optional: custom weights JSON",
        type=["json"],
        key="weights",
        help="Format: { 'ROOM_TYPE': { 'COST_GROUP': weight, ... }, ... }",
    )

    # --- Optional: custom cost rates JSON ---
uploaded_cost_rates = st.file_uploader(
        "Optional: custom cost rates JSON",
        type=["json"],
        key="cost_rates",
        help="Format: { 'Cost group code': rate_per_m2, ... } "
             "e.g. { '05.36.90 Ventilation': 1364.17, ... }",
    )



# --- Condition that triggers ONLY when the user uploads a file ---
if uploaded_ifc is not None:

    st.success("IFC file successfully uploaded – running scripts.")

    # 1) Save IFC to disk
    ifc_path = Path("output/uploaded.ifc")
    ifc_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ifc_path, "wb") as f:
        f.write(uploaded_ifc.getbuffer())

    # 2) Open IFC model
    model = ifcopenshell.open(ifc_path)

    # 3) Run space extraction (A3_Tool writes its own JSON, e.g. output/A3_Tool.json)
    A3_Tool.output_to_json(model)
    st.success("Space extraction completed.")

    # 4) Handle optional external cost rates & weights
    config_dir = Path("data")
    config_dir.mkdir(parents=True, exist_ok=True)

    # 4a) Custom cost rates → overwrite data/cost_rates.json
    if uploaded_cost_rates is not None:
        cost_rates_path = config_dir / "cost_rates.json"
        with open(cost_rates_path, "wb") as f:
            f.write(uploaded_cost_rates.getbuffer())
        st.info(f"Using custom cost rates from `{cost_rates_path}`")

    # 4b) Custom weights → save as data/custom_weights.json
    weights_override_filename = None
    if uploaded_weights is not None:
        weights_override_filename = "custom_weights.json"
        weights_path = config_dir / weights_override_filename
        with open(weights_path, "wb") as f:
            f.write(uploaded_weights.getbuffer())
        st.info(f"Using custom weights from `{weights_path}`")
    else:
        # None → rtc will use its default weights file
        weights_override_filename = None

    # 5) Run cost estimation
    rtc.process_json(
        input_path="data/A3_Tool.json",
        output_path="output/cost.json",
        config_dir=config_dir,
        weights_override_path=weights_override_filename,
    )
    st.success("Cost estimation completed (default or custom weights).")


st.title("OpenBIM Tools 🧰")

tab_cost, tab_other = st.tabs(["IFC-Cost-Estimation", "Other (coming later)"])