# A2 — Cost-Checking Use Case

## A2a. About Your Group
- **Group coding level (total):** 2  
- **Focus area:** Build  
- **Role:** Manager  

---

## A2b. Identify Claim

### Building
- **ID:** #2508  

### Claim
Data visualization - Cost estimation for structural elements, windows, and spaces.

### Purpose of Checking This Claim
The purpose of verifying this claim is to determine the costs associated with columns/beams, windows, and spaces. From a greater point of view, to verify the possibility of verifying and determining cost associated with any object digitally would be time saving.  

- **Columns/Beams:** quantity, material type, and dimensions  
- **Windows:** number, dimensions, and type  
- **Spaces:** classification and evaluation  

All elements as a general rule will use the **Molio price database** for cost estimation.  
Cost estimation is critical for financial feasibility — poor control can make a project unviable - during the tender phase, this can greatly help enhance the response time, increase productivity,efficiency and accuracy of a tender offer from GA's points of view. (given that the model and objects are correctly created) 

---

## A2c. Use Case

### How Would You Check This Claim?
1. Identify three cost-related claims from the report.  
2. Analysts each develop Python scripts to verify the claim them.  
3. Manager integrates all results into a single platform.  
4. Extract quantities using **ifcOpenShell**.  
5. Intergrate results with **Molio** price database.

### What Phase?
**Tender phase (Build focus area)**

At this stage, verified cost estimates ensure bids reflect accurate quantities and materials, reducing financial risk before construction begins.

### What Information Does This Claim Rely On?

See - Analyst groups.

### What BIM Purpose Is Required?
**Analyse** (extract and compute), then **Communicate** (report to stakeholders).

### Closest BIM Use Case
**Use Case 02 — Cost Estimation**

### BPMN Diagram

![](./flow.svg)
[View Flow_Diagram (file)](./flow.svg)


## A2d. Scope the Use Case
![](./scope.svg)
[View Scope (file)](./scope.svg)

## A2e. Tool Idea

### Overview
Python-based **cost-checking and validation tool** using ifcOpenShell.

### Core Function
Automatically extract defined quantities and materials from an IFC model, combine with Molio unit prices, and calculate total costs.

### Features
- Integrates results from multiple analysts, scripts  
- Visualises data and creates reports  
- Supports **OpenBIM** principles of interoperability, collaboration, and traceability

### Business Value
- Automates quantity take-offs and price calculations  
- Improves accuracy and efficiency  
- Enables stronger budget control  

### Societal Value
- Promotes transparency and sustainability through OpenBIM standards  

## A2f. Information Requirements

### Information to Extract
| Category | IFC Class | Data Needed |
|-----------|------------|--------------|
| Columns | `IfcColumn` | Quantity, material, dimensions |
| Beams | `IfcBeam` | Quantity, material, dimensions |
| Windows | `IfcWindow` | Quantity, dimensions, type |
| Spaces | `IfcSpace` | Classification, area, volume |
| walls | `IfcWall` | Classification, area|

### Is It in the Model?
YES

### Access via ifcOpenShell?
YES
