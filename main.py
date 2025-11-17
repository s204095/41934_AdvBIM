import json
from pathlib import Path
import tempfile
import ifcopenshell
import streamlit as st
import pandas as pd
import altair as alt






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



# --- Condition that triggers ONLY when the user uploads a file ---
if uploaded_ifc is not None:
    

    st.success("IFC file successfully uploaded. - running background scripts.")

    # Example: Save it to disk (optional)
    ifc_path = Path("output/uploaded.ifc")
    ifc_path.parent.mkdir(exist_ok=True)
    with open(ifc_path, "wb") as f:
        f.write(uploaded_ifc.getbuffer())

    model = ifcopenshell.open(ifc_path)


    # Put your next actions here
    A3_Tool.output_to_json(model)
    st.success("Space Extraction completed.")

    rtc.process_json("data/A3_Tool.json","output/cost.json")
    st.success("Cost Estimation:Defult weights completed.")

        

st.title("OpenBIM Tools 🧰")

# ---------------- Tabs for visualization ----------------
tab_cost, tab_areas = st.tabs(["Cost overview (cost.json)", "Area distribution (A3_Tool.json)"])

# ================== TAB 1: cost.json ==================
with tab_cost:
    st.header("🏗️ Cost overview from roomtype_cost")

    cost_path = Path("output/cost.json")

    if not cost_path.exists():
        st.warning("`output/cost.json` not found. Run the cost estimation pipeline first.")
    else:
        with open(cost_path, "r", encoding="utf-8") as f:
            cost_data = json.load(f)

        # Top-level KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Total area (m²)", f"{cost_data.get('total_area_basis', 0):,.2f}")
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
    st.header("📐 Area distribution from A3_Tool")

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


            
            

        