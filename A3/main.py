import os, json, tempfile
import pandas as pd
import streamlit as st
import ifcopenshell
import streamlit.web.bootstrap
import streamlit.config
streamlit.config.set_option("server.maxUploadSize", 1024)

# ---- your tools (each returns dict and writes JSON) ----
from rules.tools import get_ftf_heights, get_project_overview, get_element_counts

st.set_page_config(page_title="IFC Tools – Batch Runner", layout="wide")
st.title("🏗️ IFC Tools – Batch Runner")

# ensure data folder
DATA_DIR = "rules/data"
os.makedirs(DATA_DIR, exist_ok=True)



# ---- upload IFC ----
uploaded = st.file_uploader("Upload IFC", type=["ifc"])
if not uploaded:
    st.info("Upload an IFC to run all tools.")
    st.stop()

# save to temp for ifcopenshell
with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as tmp:
    tmp.write(uploaded.getbuffer())
    tmp_path = tmp.name

# open IFC
try:
    model = ifcopenshell.open(tmp_path)
    st.success(f"Loaded: {uploaded.name}")
except Exception as e:
    st.error(f"Failed to open IFC: {e}")
    st.stop()

# ---- register tools (name, function, output file) ----
TOOLS = [
    ("Project Overview", get_project_overview, f"{DATA_DIR}/project_overview.json"),
    ("Element Counts",  get_element_counts,   f"{DATA_DIR}/element_counts.json"),
    ("Floor-to-Floor",  get_ftf_heights,     f"{DATA_DIR}/ftf_heights.json"),
]

# ---- run all tools ----
results = []

status = st.empty()

for name, func, out_path in TOOLS:
    try:
        status.info(f"Running: {name} …")
        data = func(model, output_path=out_path)   # each tool writes JSON
        results.append((name, data, out_path))
    except Exception as e:
        results.append((name, {"error": str(e)}, out_path))

status.empty()
st.success("All tools executed.")



# ---- pretty display (tabs) ----
tabs = st.tabs([n for n, _, _ in results])
for tab, (name, data, out_path) in zip(tabs, results):
    with tab:
        st.subheader(name)
        if "error" in data:
            st.error(data["error"])
            continue

        # JSON pretty view
        
        #st.json(data)

        # Contextual “pretty” bits
        if name == "Floor-to-Floor" and isinstance(data, dict):
            st.metric("Total Building Height (m)", data.get("TotalBuildingHeight_m", "—"))
            st.markdown("**Storeys**")
            st.dataframe(data.get("Storeys", []), use_container_width=True)
            st.markdown("**Floor-to-Floor Heights**")
            st.dataframe(data.get("FloorToFloorHeights", []), use_container_width=True)

        if name == "Element Counts" and isinstance(data, dict):
            counts = data.get("counts", {})
            if counts:
                st.bar_chart(counts)

        # Download
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                payload = f.read().encode("utf-8")
            st.download_button(
                f"⬇️ Download {os.path.basename(out_path)}",
                data=payload,
                file_name=os.path.basename(out_path),
                mime="application/json",
            )
        except Exception:
            st.info("File saved to server; download not available.")
