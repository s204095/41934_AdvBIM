import ifcopenshell
import ifcopenshell.util.element
import numpy as np

# Function
def get_area_of_spaces(model):
    spaces = model.by_type("IfcSpace")
    meeting_room = []
    areas = []

    for space in spaces:
        if space.LongName == 'Meeting room':
            meeting_room.append(int(space.Name))
            qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
            sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
            areas.append(int(sqrm))
        else:
            continue
    return areas

def check_area_in_intervals(model, req_1, req_2):
    areas = get_area_of_spaces(model)
    #print(areas)

    list_1 = []
    list_2 = []
    list_3 = []

    for area in areas:
        if req_1[0] <= area < req_1[1]:
            list_1.append(area)
        elif req_2[0] <= area:
            list_2.append(area)
        else:
            list_3.append(area)
    
    areas_req_1 = len(list_1)
    areas_req_2 = len(list_2)
    areas_outside_req = len(list_3)

    return areas_req_1, areas_req_2, areas_outside_req


# requirements is list with lists [[num_rooms, num_peep],[num_rooms,num_peep],...,...]
def check_area(model, requirements):  
    areas = get_area_of_spaces(model)

    area_requirements = []
    list_dict = {}
    used_indices = set()

    for req in requirements:
        total_area = req[1]*2
        area_requirements.append(total_area)
    for required_area in area_requirements:
        list_dict[required_area] = []
        for i, area in enumerate(areas):
            if area >= required_area and i not in used_indices:
                list_dict[required_area].append(area)
                used_indices.add(i)
            else:
                continue
    
    return list_dict











