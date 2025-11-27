# Assignment A2 – Cost Estimation Validation Tool

## A2a: Coding Confidence

**We as a group are confident coding in Python:**
**Total score: 7-8**

We are analysts within the focus area "Build", with a specific focus on cost estimation.

---

## A2b: Identify the Claim

**Selected building:** #2516

**Claim / issue to check:**
How realistic the claimed *cost estimation* of constructing the building is.

**Description of the claim:**
The report for building #2516 provides a cost estimate for various building elements (e.g., windows) including quantities for each building element. We want to verify whether the claimed quantities of each elements and their stated costs match what can be extracted from the actual BIM model (IFC). This allows us to validate whether the reported building cost is realistic and consistent with the projected BIM model.

**Justification for selection:**
Cost estimation is a central part of building design and construction. Wrong quantities and building element detection can result in incorrect cost estimation and therefore inflated/deflated cost estimations which can significantly impact budgets and decision-making. By creating a tool that can not only validate the claimed cost estimation but also creates it own cost estimation based on quantities from the IFC models more correct cost estimations can be made resulting in better decision-making and budgetting.

---

## A2c: Use Case

**How would you check this claim?**
By analyzing the IFC model with `ifcopenshell`, automatically extracting relevant elements (e.g., windows), and then calculating costs, the extracted values and produced cost estimates can be compared to the claimed quantities and cost estimations.

**When would this claim need to be checked?**

This claim should be checked during the **design phase**, when cost reports are prepared. It can also be valuable in the **planning phase**, before tendering, to ensure that the claimed numbers are realistic.


**What information does this claim rely on?**

* Quantities of building elements (e.g., number of windows, dimensions).
* Material properties (wood, aluminum, etc.).
* Claimed prices and assembly units (from the cost report).
* Market-based or database-based price per m².

**What phase?**

**Design and planning phase.**

**What BIM purpose is required?**

The purpose is to **analyze** the model to check the validity of claims and to **communicate** any mismatches identified between the model and the cost report.

**BIM use case:**

XX Use case?

---

## A2d: Scope the Use Case

*(Diagram will be created separately.)*

---

## A2e: Tool Idea

**Description:**
Our idea is to develop a tool that automatically validates cost estimation claims from BIM models. The tool reviews the IFC model, extracts relevant elements, calculates quantities, assigns estimated prices based on molio price data, and compares these against claimed costs in reports. It highlights mismatches in quantities, dimensions, or total costs. Compared to current manual methods, which rely heavily on qualified estimators and are both time-consuming and prone to human error, this tool provides a fast, consistent, and transparent way to verify cost reports directly against the model data.

**Business and societal value:**

* **Transparency:** Ensures that reported costs match actual model data, preventing overestimation.
* **Efficiency:** Automates a process that is otherwise manual and error-prone.
* **Trustworthiness:** Helps stakeholders verify that project costs are grounded in real data and quantities.
* **Educational value:** Demonstrates the potential of OpenBIM tools in cost validation for students and professionals.

---

## A2f: Information Requirements

**Information needed from IFC:**

We need to extract all relevant IfcBuildingElements along with geometry

* **IfcWindow** (and later IfcDoor, IfcWall, etc.)

  * `OverallHeight` (for dimensions)
  * `OverallWidth` (for dimensions)
  * `HasAssociations → RelatingMaterial` (for material type)
* Element counts
* Element geometry (to calculate areas, m²)

**Where is this in IFC?**

* `IfcWindow.OverallHeight` and `IfcWindow.OverallWidth` give element dimensions.
* `IfcRelAssociatesMaterial → IfcMaterial.Name` gives the material.

**Is it in the model?**

* Yes, these attributes are standard in IFC windows and are present in our Building #2516 model.

**Do you know how to get it in ifcOpenShell?**

* Yes. Using `model.by_type("IfcWindow")` we can iterate through windows and access OverallHeight and OverallWidth.
Materials can be accessed via HasAssociations.

