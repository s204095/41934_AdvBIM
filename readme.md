# OpenBIM Cost Allocation & Data visualisation Tool
**🏢 Overview**

***A web-based flexible application that Visualizes data - the specific example in automatically Estimates and allocates building costs (electricity, cleaning, maintenance, etc.) to different room types based on IFC model data, Locally***

## 🚀 What It Does
A localhost web interface that provides a place where users tailor and assemble the specific tools relevant to their domain, whether that is economics, structural analysis, construction management, design, or other disciplines. 

    - in the specific proof of concept example, we processes IFC data, classifies spaces, and distributes costs using adjustable weights, providing fast and transparent insights for BIM-based planning, analysis and cost estimation.

Steps 

- Upload IFC models and automatically extract space information

- Classify rooms using customizable keyword matching (office, lab, meeting room, etc.)

- Calculate operational costs based on area and usage patterns

- Allocate costs fairly using customizable weights and rates

Generate reports in json format with cost breakdowns per room type and cost category

## 💡 Key Features

- Web Interface - Easy-to-use Streamlit web app

- Customizable - Upload your own cost rates and allocation weights / customize your own tools by intergrating other data extraction scripts. 

- Automated - No manual data entry required

- Transparent - Clear cost allocation methodology

## 🎯 Use Cases

- Facility/Project Managers - costs estimation during tender phase

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


## Troubleshooting

    When cloning the repository, the submodules inside the external folder may appear empty. Make sure to pull the submodules after cloning, so the required files are actually downloaded before you run the tool. 
