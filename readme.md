# OpenBIM Cost Allocation Tool
**🏢 Overview**

***A web-based application that automatically calculates and allocates building operational costs (electricity, cleaning, maintenance, etc.) to different room types based on IFC model data.***

## 🚀 What It Does
- Upload IFC models and automatically extract space information

- Classify rooms using customizable keyword matching (office, lab, meeting room, etc.)

- Calculate operational costs based on area and usage patterns

- Allocate costs fairly using customizable weights and rates

Generate reports in json format with cost breakdowns per room type and cost category

## 💡 Key Features

- Web Interface - Easy-to-use Streamlit web app

- Customizable - Upload your own cost rates and allocation weights

- Automated - No manual data entry required

- Transparent - Clear cost allocation methodology

## 🎯 Use Cases

- Facility/Project Managers - Understand and distribute operational costs

- BIM Consultants - Provide added value services to clients

- Sustainability Analysis - Identify high-cost areas for improvement

## ⚡ Quick Start - Tutorial

1. Clone repository. 
2. run setup.bat

3. Upload IFC model



4. View instant cost allocation results



## 🛠️ Dependencies


- python
- json
- pathlib
- tempfile
- ifcopenshell
- streamlit as st
- pandas as pd
- altair
- numpy
- csv
