import ifcopenshell
import ifcopenshell.util.element
import json
import os
import csv
import shutil

def total_area_and_number(model):
    # Extract all spaces from the IFC model
    spaces = model.by_type("IfcSpace") 
    Area_sum = []

    # Iterates through every space found in the model
    for space in spaces:
        # Retrieve only quantity sets for the current space
        qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
        if 'Qto_SpaceBaseQuantities' in qtos:
            sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
            Area_sum.append(sqrm)
        else:
            print('Qto_SpaceBaseQuantities is missing for space:', space)

    # Returns two values:
    # 1) The total area
    # 2) The total number of spaces in the model
    return round(sum(Area_sum), 1), len(Area_sum)

def get_area_by_space_types(model):
    # Extract all spaces from the IFC model
    spaces = model.by_type("IfcSpace")
    space_list = []
    area_by_type = {}

    # Create a list of all spaces
    for space in spaces:
        space_list.append(space.LongName)
    # Change the list to only contain each space type once
    space_types = list(dict.fromkeys(space_list))

    # Iterate through each type of space
    for type in space_types:
        # Create list to sum total area for each space type
        area_by_type[type] = []
        for space in spaces:
            if space.LongName == type:
                qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
                if 'Qto_SpaceBaseQuantities' in qtos:
                    sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
                    # Add space type with corresponding area to the dictionary initiated in the top
                    area_by_type[type].append(sqrm)
                else:
                    print('Qto_SpaceBaseQuantities is missing for space:', space)
        # sum the list for the current space type
        area_by_type[type] = round(sum(area_by_type[type]),2)

    # Returns one value:
    # 1) A dictionary with each type of space and the corresponding summed area
    return area_by_type

def interior_walls_area(model):
    # Extract all walls from the IFC model
    walls = model.by_type("IfcWall")
    area_sum = 0.0

    # Iterate through each wall
    for wall in walls:
        wall_type = wall.ObjectType
        wall_name = wall.Name
        # Goes through the walls and picks out all interior walls
        if wall_type and "Interior".lower() in wall_type.lower() or wall_name and "Interior".lower() in wall_name.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            # for all spaces with the defined quantity set, get length area and volume
            if 'Qto_WallBaseQuantities' in qtos:
                length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                sidearea = qtos['Qto_WallBaseQuantities'].get('NetSideArea',0)
                volume = qtos['Qto_WallBaseQuantities'].get('NetVolume',0)
                # Calculate floor area under the wall and sum it together
                if sidearea > 0.0:
                    width = volume / sidearea
                    area = width * length * 10**-3
                    area_sum += area
            else:
                print('Qto_WallBaseQuantities is missing for wall:', wall_name, wall_type)
    
    # Returns one value:
    # 1) The summed floorarea covered by interior walls
    return round(area_sum, 2)

def exterior_walls_area(model):
    # Extract all walls from the IFC model
    walls = model.by_type("IfcWall")
    area_sum = 0.0

    # Iterate through each wall
    for wall in walls:
        wall_type = wall.ObjectType
        wall_name = wall.Name
        # Goes through the walls and picks out all exterior walls
        if wall_type and "Exterior".lower() in wall_type.lower() or wall_name and "Exterior".lower() in wall_name.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            # for all spaces with the defined quantity set, get length area and volume
            if 'Qto_WallBaseQuantities' in qtos:
                length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                sidearea = qtos['Qto_WallBaseQuantities'].get('NetSideArea',0)
                volume = qtos['Qto_WallBaseQuantities'].get('NetVolume',0)
                # Calculate floor area under the wall and sum it together
                if sidearea > 0.0:
                    width = volume / sidearea
                    area = width * length * 10**-3
                    area_sum += area
            else: 
                print('Qto_WallBaseQuantities is missing for wall:', wall_name, wall_type)

    # Returns one value:
    # 1) The summed floorarea covered by exterior walls              
    return round(area_sum, 2)

def curtain_walls_area(model):
    # Extract all walls from the IFC model
    walls = model.by_type("IfcCurtainWall")
    area_sum = 0.0

    # Iterate through each wall
    for wall in walls:
        wall_type = wall.ObjectType
        wall_name = wall.Name
        # Goes through the walls and picks out all interior walls
        if wall_type and "Curtain".lower() in wall_type.lower() or wall_name and "Curtain".lower() in wall_name.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            # for all spaces with the defined quantity set, get length area and volume
            if 'Qto_CurtainWallQuantities' in qtos:
                length = qtos['Qto_CurtainWallQuantities'].get('Length',0)
                # Calculate floor area under the wall and sum it together
                area = 150 * length *10**-6
                area_sum += area
            else: 
                print('Qto_WallBaseQuantities is missing for wall:', wall_name, wall_type)

    # Returns one value:
    # 1) The summed floorarea covered by curtainwalls              
    return round(area_sum, 2)

def columns_area(model):
    columns = model.by_type('IfcColumn')
    area_sum = 0.0

    for column in columns:
        psets = ifcopenshell.util.element.get_psets(column, qtos_only=False)
        if 'Dimensions' in psets:
            length = psets['Dimensions'].get('Depth',0)
            width = psets['Dimensions'].get('Width',0)
            area = length * width * 10**-6
            area_sum += area
        else:
            print('Dimensions is missing for column: ', column)

    # Returns one value:
    # 1) The summed floorarea covered by columns
    return round(area_sum, 2)

def copy_csv_files_to_folder(src_folder):
    # Name of the output folder where CSV files will be copied
    folder_name = 'Output'
    # construct the full path to the destination folder
    dest_folder = os.path.join(src_folder, folder_name)
    # Create the destination folder if it doesn't already exist
    os.makedirs(dest_folder, exist_ok=True)
    
    # Find all CSV files in the source folder
    csv_files = [f for f in os.listdir(src_folder) if f.endswith('.csv') and os.path.isfile(os.path.join(src_folder, f))]
    copied_files = []
    # Loop over each CSV file found in the source folder
    for csv_file in csv_files:
        # Build the full source path and destination path for the file
        src_file = os.path.join(src_folder, csv_file)
        dest_file = os.path.join(dest_folder, csv_file)
        # Copy the CSV file to the destination folder
        shutil.copy2(src_file, dest_file)
        # Record the new file's path in the copied_files list
        copied_files.append(dest_file)
    
    # Print information about the copy destination
    print('Copied:', len(copied_files), '.csv files to folder:', dest_folder)

    # Returns two values:
    # 1) copied_files: a list of paths to the copied CSV files
    # 2) dest_folder: the path to the folder where files were copied
    return copied_files, dest_folder

def aggregate_price_values(csv_files):
    # Initialize an empty list to store all price values extracted from CSV files
    price_values = []

    # Loop over the list of CSV file paths
    for file_path in csv_files:
        # open the current CSV file for reading
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            # Iterate over each row in the CSv file
            for row in csv_reader:
                # Retrieve the value in the 'Pris' column and clean the formatting:
                # - Remove '.' and replace ',' with '.'
                price_str = row['Pris'].strip().replace('.', '').replace(',', '.')
                # If the cleaned string is not empty, convert to float an add to the list
                try:
                    price_values.append(float(price_str)) if price_str else price_values.append(0.0)
                # If conversion fails, append 0.0 as fallback
                except ValueError:
                    price_values.append(0.0)
    # Caculate the som of all extracted price values
    total_price = round(sum(price_values), 4)

    # Returns one value:
    # 1) The summed price pr. sqrm from csv-file 
    return total_price

def area_output_to_json(model, file_path, output_filename):
    # Define all informations from other functions
    spaces_area = get_area_by_space_types(model)
    total_area_number_of_spaces = total_area_and_number(model)
    walls_area_int = interior_walls_area(model)
    walls_area_ext = exterior_walls_area(model)
    curtainwalls_area = curtain_walls_area(model)
    columns_total_area = columns_area(model)
    gross_floor_area = round(total_area_number_of_spaces[0] + walls_area_int + walls_area_ext + curtainwalls_area + columns_total_area, 2) 

    # File handling: Copy and read CSV files
    csv_files, folder_path = copy_csv_files_to_folder(file_path)

    # Create a dictionary with the information
    output_data = {
        "Area of spaces": spaces_area,
        "Total area of spaces": total_area_number_of_spaces[0],
        "Total number of spaces": total_area_number_of_spaces[1],
        "Area of interior walls": walls_area_int,
        "Area of exterior walls": walls_area_ext,
        "Area of curtain walls": curtainwalls_area,
        "Area of columns": columns_total_area,
        "Total summed area": gross_floor_area
    }

    output_path = os.path.join(folder_path, output_filename)
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(output_data, json_file, indent=4)
    print(f"JSON file saved to {output_path}")

    # Creates one file:
    # 1) .json file with area data

def price_output_to_json(model, file_path, output_filename):
    # Define all informations from other functions
    spaces_area = get_area_by_space_types(model)
    total_area_number_of_spaces = total_area_and_number(model)
    walls_area_int = interior_walls_area(model)
    walls_area_ext = exterior_walls_area(model)
    curtainwalls_area = curtain_walls_area(model)
    columns_total_area = columns_area(model)
    gross_floor_area = round(total_area_number_of_spaces[0] + walls_area_int + walls_area_ext + curtainwalls_area + columns_total_area, 2) 

    # File handling: Copy and read CSV files
    csv_files, folder_path = copy_csv_files_to_folder(file_path)
    price_values = aggregate_price_values(csv_files)

    # Total price
    total_price = gross_floor_area * price_values

    # Find how much of the GFA each type of space consumes
    percentages_by_space = {spacetype: round(area / gross_floor_area, 4) for spacetype, area in spaces_area.items()}
    
    # Calculate price based on percentages
    price_pr_spacetype = {spacetype: round(total_price * percentage,4) for spacetype, percentage in percentages_by_space.items()}

    # Create a dictionary with the information
    output_data = {
        "Area of spaces": spaces_area,
        "Weight by spacetype": percentages_by_space,
        "Price calculated based on Weighted area": price_pr_spacetype,
        "Price pr. sqrm": price_values,
        "Estimated price": total_price
    }
        
    output_path = os.path.join(folder_path, output_filename)
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(output_data, json_file, indent=4)
    print(f"JSON file saved to {output_path}")

    # Creates one file:
    # 1) .json file with price data