from pathlib import Path
import ifcopenshell
import ifcopenshell.util.element
import os

#Filename (.ifc assumed)
modelname = "25-08-D-ARCH"

#Load ifc model
try:
    dir_path = Path(__file__).parent
    parent_path = dir_path.parent
    sibling_folder = parent_path / 'model'
    model_url = sibling_folder / '25-08-D-ARCH.ifc'
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Import functions
from A3_Tool import area_output_to_json
from A3_Tool import price_output_to_json

# A3
area = area_output_to_json(model, os.getcwd() + '/ADV_BIM/A3', 'A3_Output_area')
price = price_output_to_json(model, os.getcwd() + '/ADV_BIM/A3', 'A3_Output_price')