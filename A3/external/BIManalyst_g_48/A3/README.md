# A3: Tool

Group 48, BUILD Analyst

## About the tool

Group 48 has developed a simple tool that, for a given ifc architectural model, returns a list of area types, areas and total area, including floor area occupied by walls.


The aim of the tool is to serve as a convenient way to check whether certain area targets are met, such as '3000 sqm of office area', or a '500 sqm lobby' etc, or simply to check on how the area is distributed on rooms, hallways and so on, as well as providing way to roughly calculate a price based on these areas.

All the tool needs to run is a loaded .ifc model and a price list in .csv format. When run, the output data will be saved as a local .json file.

## Advanced Building Design

This tool can be used as soon as areas have been defined in a BIM model, which roughly translates into stage B, but can also be used for documentation in stages C and D.

The tool should be useful to:
- ARCH as a form of self-monitoring,  
- MEP for ventilation calculations and
- PM as a way to document area compliance and approximate price.

### Necessary information:

In order for the program to run optimally, the .ifc model must meet the following criteria:
- All floor areas are defined and named. (IfcSpace)
- All interior and exterior walls include 'Interior' or 'Exterior' in the name. (IfcWall)
- Dimensions are documented in specific quantity sets ({'Length'(mm), 'NetSideArea'(m2), 'NetVolume'(m3)} in 'Qto_WallBaseQuantities' & {'NetFloorArea'} in 'Qto_SpaceBaseQuantities'). This should be the case by default.

### Known issues:

- some special characters (e.g. é) will be output as a typecode (e.g. \u00e9)
- In the test model, quantity sets were not available for columns. Therefore, 'Dimensions' are used, which is Revit based.
