import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

for path in [project_root, os.path.join(project_root, "external")]:
    if path not in sys.path:
        sys.path.append(path)   

import ifcopenshell
from external.BIManalyst_g_48.rules import SpaceRequirement
from external.BIManalyst_g_46 import main


def check_space(model):
    name = input("Enter space name: ----Caps sensitive---- ")
    num = int(input("Enter required number: "))
    result = SpaceRequirement.check_space_requirement(model, name, num)
    

def list_column_types(model):
    types = main.get_column_type_names(model)
    print("Column types:", types)

def main_menu():
    file_path = input("Enter IFC file path: ").strip()
    try:
        model = ifcopenshell.open(file_path)
    except Exception as e:
        print("Error opening file:", e)
        return

    functions = {
        "1": ("Check space requirement", check_space),
        "2": ("List column types", list_column_types),
        "q": ("Quit", None)
    }

    while True:
        print("\nAvailable functions:")
        for key, (desc, _) in functions.items():
            print(f"{key}. {desc}")

        choice = input("Select function: ").strip().lower()

        if choice == "q":
            print("Exiting program...")
            break
        elif choice in functions:
            func = functions[choice][1]
            if func:
                func(model)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()





#model = ifcopenshell.open("C:/Users/feizh/Downloads/25-08-D-ARCH.ifc")
#name = "Meeting room"
#num = 12


#SpaceResult = SpaceRequirement.check_space_requirement(model,name,num)


