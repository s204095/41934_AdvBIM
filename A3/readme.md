# **A3 – About the Tool**

# **State the Problem / Claim the Tool Is Solving**
The tool visualizes and allocates estimated costs for each space in an IFC building model based on the spaces’ functions.  
This allows users to instantly see which room types drive the overall cost, without spreadsheets or manual classification.

# **Where the Problem Was Identified**
This need arises:
- during the tender/early planning phase where managers need fast and transparent cost estimates per room type,
- among BIM consultants wanting to link spatial data to cost drivers,
- in sustainability and performance analysis where identifying high-cost spaces supports improvement strategies.

(These needs reflect common industry workflows and the described use cases.)

# **Description of the Tool**
**Input:** IFC model + optional cost rates and allocation weights (CSV/JSON).  

**Process:**  
1. Extracts IfcSpace information (area, name/function, storey, etc.).  
2. Classifies rooms via customizable keyword matching (office, meeting room, lab…).  
3. Calculates costs based on area and functional usage patterns.  
4. Allocates shared operational costs using user-defined weighting factors.  
5. Generates a structured JSON report with cost breakdowns per room type and cost category.  

**UI/Output:** Streamlit web interface with interactive Altair charts and downloadable JSON report.  

**Principles:** Customizable, Automated, Transparent.

# **Instructions to Run the Tool**
1. Clone the repository.  
2. Run `setup.bat` to install dependencies.  
3. Launch the app:  
   `streamlit run app.py`  
4. Upload an IFC model (plus optional cost rate/weight files).  
5. View cost allocation results and download the JSON report.

# **Dependencies**
python, ifcopenshell, streamlit, pandas, altair, numpy, and standard libraries (json, csv, pathlib, tempfile).


# **Data format Requirements**
Please see requirement for JSON data format under data readme.md

# **Relevant ABD Stage**
- **Stages A–B:** conceptual and early schematic design — quick understanding of cost distribution.  
- **Stage C:** testing alternatives and “what-if” scenarios.  
- **Stage D:** QA and benchmarking during detailed design/tender.

# **Subjects That Might Use It**
- BIM / Digital Construction  
- Construction Economics / Cost Estimation  
- Project & Construction Management  
- Facility Management  
- Sustainability & Performance Analysis  
- Building Programming / Space Planning  

# **Required Model Information**
The IFC model must contain:
- IfcSpace entities for all relevant rooms  
- Identifiers for classification (Name, LongName, Description, or functional property sets)  
- Area values (IfcQuantityArea via BaseQuantities, or computed from geometry)  
- Storey/zone information (optional but useful)  
- External cost rates/weights (CSV/JSON) if using custom values
