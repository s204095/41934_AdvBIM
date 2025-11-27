# BIManalyst group 48
## Focus area: 
BUILD
## Claim: 
Amount and size of meeting rooms against requirements
## Report: 
2025 Group 8, Client report, page 2 (vs. general requirements from project brief)

## Script description: (Rules / SpaceRequirement.py)
This script checks a certain room type (name is case sensitive) against a provided requirement amount.

Example with meeting rooms:

Step 1: Search for and list rooms named 'Meeting room'

Step 2: Look up and list spaces with the name 'Meeting room'

Step 3: Compare amount of rooms against requirement (in this case, 12 meeting rooms are necessary)

### How to use:
See main.py for concrete example.
Model should be loaded before use.
1. from rules import SpaceRequirement
2. SpaceRequirement.check_space_requirement(model, string(name of room type), integer(required amount of rooms))

Based on amount and requirement, the script will print a statement. e.g. "There are 6 Meeting room in the model which is less than the required 12"
