from pathlib import Path
import ifcopenshell
import ifcopenshell.util.element
import os

#Filename (.ifc assumed)
modelname = "25-08-D-ARCH"

#Load ifc model
try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Import functions
from A3 import A3_Tool

# A3
json = A3_Tool.output_to_json(model)