


cost_rates needs a conversion script in relation to the room type and weights 


import streamlit as st
import json
import pandas as pd
from pathlib import Path


'''

st.title("This is streamlit APP")
st.header("This is streamlit APP")
st.subheader("This is streamlit APP")
st.markdown("This is streamlit APP")
st.caption("This is streamlit APP caption")
st.write("This is streamlit APP")
st.write(123)


st.divider()

json_path = Path("data/A3_Tool.json")


st.title("IFC Pricing tool")


with json_path.open("r", encoding="utf-8") as f:data = json.load(f)

with st.expander("Raw JSON Data"):
    st.json(data)

scalars = {k: v for k, v in data.items() if not isinstance(v, dict)}

with st.expander("📐 Summary Values"):
    st.write(scalars)

# 3. Show space areas as a table

spaces = data["Area of spaces"]
spaces = dict(sorted(spaces.items(), key=lambda x: x[1], reverse=True))
spaces_df = (
    pd.DataFrame.from_dict(spaces, orient="index", columns=["Area (m²)"])
    .reset_index()
    .rename(columns={"index": "Space Type"})
)


with st.expander("📊 Area of Spaces (Detailed Breakdown)"):
    st.dataframe(spaces_df, use_container_width=True)






#################### CHARTS ####################

##Bar##
st.divider()
st.title("Charts")

st.bar_chart(spaces_df.set_index("Space Type"))



##Pie##

import altair as alt

pie_df = spaces_df.copy()

chart = (
    alt.Chart(pie_df)
    .mark_arc()
    .encode(
        theta=alt.Theta(field="Area (m²)", type="quantitative"),
        color=alt.Color(field="Space Type", type="nominal"),
        tooltip=["Space Type", "Area (m²)"]
    )
)

st.altair_chart(chart, use_container_width=10)

##Matplot##

import matplotlib.pyplot as plt

# Sort by area, largest first
bar_df = spaces_df.sort_values("Area (m²)", ascending=True)

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(bar_df["Space Type"], bar_df["Area (m²)"])
ax.set_xlabel("Area (m²)")
ax.set_ylabel("Space type")
ax.set_title("Area by Space Type")

st.pyplot(fig)

pie_df = spaces_df.sort_values("Area (m²)", ascending=False)

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    pie_df["Area (m²)"],
    labels=pie_df["Space Type"],
    autopct="%1.1f%%",
    startangle=90
)
ax.set_title("Space Area Distribution")

st.pyplot(fig)
'''