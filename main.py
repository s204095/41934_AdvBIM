import json
from pathlib import Path
import tempfile
import ifcopenshell
import streamlit as st
import pandas as pd
import altair as alt

# Import your submodules
from external.BIManalyst_g_48.A3 import A3_Tool        # submodule for area extraction 
from external.BIManalyst_g_49 import roomtype_cost as rtc  # submodule of cost estimation




# Mini IDS

def check_spaces_exist(model):
    """Mini IDS: Check if model has spaces"""
    spaces = model.by_type("IfcSpace")
    return len(spaces) > 0, len(spaces)

def mini_ids_check(model):
    """Run basic space existence check"""
    has_spaces, space_count = check_spaces_exist(model)
    
    st.subheader("🔍 Quick Model Check")
    
    if has_spaces:
        st.success(f"✅ Model OK: {space_count} spaces found")
        return True
    else:
        st.error("❌ No spaces found - cost allocation won't work")
        st.info("Spaces are required for area calculations")
        return False









# Increase max file size
st.set_page_config(page_title="OpenBIM 🧰", layout="wide")





# Define paths
DATA_DIR = Path("data")
CUSTOM_DATA_DIR = DATA_DIR / "custom_data"
CUSTOM_DATA_DIR.mkdir(exist_ok=True)

# --- Upload Widget ---
st.header("Upload config files to override defaults")

col1, col2 = st.columns(2)
with col1:
    custom_weights = st.file_uploader("Upload custom weights JSON (optional)", type=["json"])
with col2: 
    custom_rates = st.file_uploader("Upload custom cost rates JSON (optional)", type=["json"])

# Track if custom files were uploaded
custom_files_uploaded = False

# Save uploaded config files to custom_data
if custom_weights is not None:
    weights_path = CUSTOM_DATA_DIR / "custom_weights.json"
    with open(weights_path, "wb") as f:
        f.write(custom_weights.getvalue())
    st.success("✅ Custom weights saved")
    custom_files_uploaded = True

if custom_rates is not None:
    rates_path = CUSTOM_DATA_DIR / "cost_rates.json"
    with open(rates_path, "wb") as f:
        f.write(custom_rates.getvalue())
    st.success("✅ Custom cost rates saved")
    custom_files_uploaded = True

# Show current custom files
st.subheader("Current Custom Files")

custom_files = list(CUSTOM_DATA_DIR.glob("*.json"))
if custom_files:
    for file in custom_files:
        st.write(f"• {file.name} ({(file.stat().st_size / 1024):.1f} KB)")
    
    if st.button("🗑️ Clear Custom Files"):
        for file in custom_files:
            file.unlink()
        st.success("Custom files cleared!")
        st.experimental_rerun()
else:
    st.info("No custom configuration files uploaded.")

st.divider()

st.header("Upload IFC model")
uploaded_ifc = st.file_uploader(
    "Upload IFC file",
    type=["ifc"],
    help="Select an IFC model to continue.",
)

# --- Condition that triggers ONLY when the user uploads a file ---
if uploaded_ifc is not None:
    
    # Save IFC file
    ifc_path = Path("output/uploaded.ifc")
    ifc_path.parent.mkdir(exist_ok=True)
    with open(ifc_path, "wb") as f:
        f.write(uploaded_ifc.getbuffer())

    model = ifcopenshell.open(ifc_path)
        # === MINI IDS CHECK === 
    if not mini_ids_check(model):
        st.stop()  # Stop if no spaces
    
    st.success("IFC file successfully uploaded. - running background scripts.")

    # Determine which config to use based on actual file presence
    custom_weights_exist = (CUSTOM_DATA_DIR / "custom_weights.json").exists()
    custom_rates_exist = (CUSTOM_DATA_DIR / "cost_rates.json").exists()
    
    # Use custom_data directory if ANY custom files exist
    if custom_weights_exist or custom_rates_exist:
        config_dir_to_use = CUSTOM_DATA_DIR
        st.info("🎯 Using CUSTOM configuration files")
        
        # Determine which weights file to use
        if custom_weights_exist:
            weights_file_to_use = "custom_weights.json"
            st.success("✓ Using custom weights")
        else:
            weights_file_to_use = None  # Will use default weights from custom_data (if exists) or fallback
            st.info("ℹ️ Using default weights (no custom weights uploaded)")
            
        if custom_rates_exist:
            st.success("✓ Using custom cost rates")
        else:
            st.info("ℹ️ Using default cost rates (no custom rates uploaded)")
            
    else:
        config_dir_to_use = DATA_DIR
        weights_file_to_use = None
        st.info("📁 Using DEFAULT configuration files")

    # Put analyst code here ----------------------------------------------------------------------
    A3_Tool.output_to_json(model)
    st.success("Space Extraction completed.")

    # Debug information
    st.subheader("🔍 Configuration Debug Info")
    st.write(f"**Config directory:** `{config_dir_to_use}`")
    st.write(f"**Weights file:** `{weights_file_to_use}`")
    
    # Show files that will be used
    st.write("**Files to be used:**")
    for file_type in ["room_types.json", "space_keywords.json", "cost_rates.json"]:
        file_path = config_dir_to_use / file_type
        if file_path.exists():
            st.write(f"• ✅ {file_type}")
        else:
            st.write(f"• ❌ {file_type} (missing)")
    
    weights_path = config_dir_to_use / (weights_file_to_use or "weights_default.json")
    if weights_path.exists():
        st.write(f"• ✅ {weights_path.name} (weights)")
    else:
        st.write(f"• ❌ {weights_path.name} (weights file missing)")

    
    # Run cost estimation with appropriate config
    
    try:
        rtc.process_json(
            "data/A3_Tool.json",  # This input file path stays the same
            "output/cost.json",
            config_dir=str(config_dir_to_use),
            weights_override_path=weights_file_to_use
        )
        
        success_message = "Cost Estimation: CUSTOM configuration completed!" if (custom_weights_exist or custom_rates_exist) else "Cost Estimation: DEFAULT configuration completed."
        st.success(success_message)

        # Display results if available
        cost_output_path = Path("output/cost.json")
        if cost_output_path.exists():
            with open(cost_output_path, "r") as f:
                results = json.load(f)
            
            # Display summary metrics
            st.header("📊 Cost Allocation Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Area", f"{results.get('total_area_basis', 0):,.2f} m²")
            with col2:
                st.metric("Total Cost", f"${results.get('calculated_total_cost', 0):,.2f}")
            with col3:
                st.metric("Unit Price", f"${results.get('calculated_unit_price', 0):,.2f}/m²")
            
            # Show configuration source
            st.write(f"**Configuration source:** {results.get('weights_source', 'unknown')}")
            st.write(f"**Config directory used:** {results.get('config_directory_used', 'unknown')}")
            
            # Verify if custom files were actually used
            if "custom" in results.get('weights_source', '') or "custom_data" in results.get('config_directory_used', ''):
                st.success("✅ CONFIRMED: Custom files were used in calculation")
            else:
                st.warning("⚠️ DEFAULT files were used - custom files may not have been applied")
                
    except Exception as e:
        st.error(f"❌ Error during cost allocation: {str(e)}")
        st.info("Check that all required configuration files exist in the selected directory.")
        















# ---------------- Tabs for visualization ----------------
st.title("OpenBIM Tools 🧰")



tab_areas,tab_cost,T3,T4 = st.tabs(["Area distribution (A3_Tool.json)","Cost overview (cost.json)","Tool3","Tool4" ])





# ================== TAB 1: cost.json ==================
with tab_cost:
    st.header("🏗️ Analyst_49 Cost overview")

    cost_path = Path("output/cost.json")

    if not cost_path.exists():
        st.warning("`output/cost.json` not found. Is the cost estimation step completed?")
    else:
        with open(cost_path, "r", encoding="utf-8") as f:
            cost_data = json.load(f)

        # Top-level KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Total area (m²)", f"{cost_data.get('Total summed area', 0):,.2f}")
        col2.metric("Total cost (kr)", f"{cost_data.get('calculated_total_cost', 0):,.0f}")
        col3.metric("Avg unit price (kr/m²)", f"{cost_data.get('calculated_unit_price', 0):,.0f}")

        st.caption(f"Weights source: {cost_data.get('weights_source', 'unknown')}")

        # Per room type table + bar chart
        st.subheader("Per room type")
        per_room = cost_data.get("per_room_type", {})
        df_room = pd.DataFrame.from_dict(per_room, orient="index")
        df_room.index.name = "Room type"

        if not df_room.empty:
            df_room_sorted = df_room.sort_values("unit_price", ascending=False)
            st.dataframe(
                df_room_sorted.style.format({
                    "area": "{:,.2f}",
                    "allocated_cost": "{:,.0f}",
                    "unit_price": "{:,.0f}",
                })
            )
            st.bar_chart(df_room_sorted["unit_price"])

            # ---------------------------------------------------------
            # ✅ INSERT ALTAR PIE CHART HERE (cost distribution)
            # ---------------------------------------------------------
            import altair as alt

            st.subheader("Cost distribution (pie)")
            df_room_reset = df_room_sorted.reset_index().rename(columns={"index": "Room type"})

            pie_cost = (
                alt.Chart(df_room_reset)
                .mark_arc()
                .encode(
                    theta=alt.Theta(field="allocated_cost", type="quantitative"),
                    color=alt.Color(field="Room type", type="nominal"),
                    tooltip=[
                        alt.Tooltip("Room type:N"),
                        alt.Tooltip("allocated_cost:Q", format=",.0f"),
                        alt.Tooltip("unit_price:Q", format=",.0f"),
                    ],
                )
            )

            st.altair_chart(pie_cost, use_container_width=True)
            # ---------------------------------------------------------

        else:
            st.info("No room-type data found in cost.json.")


# ================== TAB 2: A3_Tool.json ==================
with tab_areas:
    st.header("Area distribution from Analyst_48")

    a3_path = Path("data/A3_Tool.json")

    if not a3_path.exists():
        st.warning("`data/A3_Tool.json` not found. Run the area extraction first.")
    else:
        with open(a3_path, "r", encoding="utf-8") as f:
            a3_data = json.load(f)

        areas = a3_data.get("Area of spaces", {})

        if areas:
            df_areas = (
                pd.DataFrame(list(areas.items()), columns=["Space name", "Area (m²)"])
                .sort_values("Area (m²)", ascending=False)
            )

            st.dataframe(df_areas.style.format({"Area (m²)": "{:,.2f}"}))
            st.bar_chart(df_areas.set_index("Space name")["Area (m²)"])

            # ---------------------------------------------------------
            # ✅ INSERT ALTAR PIE CHART HERE (area distribution)
            # ---------------------------------------------------------
            import altair as alt

            st.subheader("Area distribution (pie)")
            pie_area = (
                alt.Chart(df_areas)
                .mark_arc()
                .encode(
                    theta=alt.Theta(field="Area (m²)", type="quantitative"),
                    color=alt.Color(field="Space name", type="nominal"),
                    tooltip=[
                        alt.Tooltip("Space name:N"),
                        alt.Tooltip("Area (m²):Q", format=",.2f"),
                    ],
                )
            )

            st.altair_chart(pie_area, use_container_width=True)
            # ---------------------------------------------------------

        else:
            st.info("No 'Area of spaces' found in A3_Tool.json.")


            
            

        